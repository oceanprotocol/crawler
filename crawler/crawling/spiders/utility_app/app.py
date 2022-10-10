import os
import signal
import time

import yagmail
from flask import Flask, Response, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pygtail import Pygtail
from crawling.db.repositories.data_repository import DataRepository
from crawling.db.jpa.schemas import (
    app_schemas,
    paginate_schema,
)
from crawling.db.jpa.spider_audit_errors import SpiderAuditErrors
from crawling.db.mysql_client import db_session, db_initialization, db_model
from crawling.db.repositories.repository import Repository
from crawling.mongo.models.spider_start_config import SpiderStartConfig
from crawling.mongo.mongo_client import mongo_client
import secrets
from subprocess import Popen
from os import kill


app = Flask(__name__, static_folder="static/", template_folder="static/")
app.register_blueprint(app_schemas)

sched = BackgroundScheduler(
    executors={"default": ThreadPoolExecutor(16), "processpool": ProcessPoolExecutor(4)}
)

current_spiders = {}


def initialization():
    db_initialization()
    spider_audit_errors_repo = Repository(db_session, SpiderAuditErrors)
    spider_audit_errors_repo.permanentDeleteAll()
    sched.start()
    sched.add_job(alerts_job, "interval", seconds=30)


def find_files(filename, search_path):
    result = []

    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result


def kill_spider_proc(spiderName):
    pid = get_random_spider_pid(spiderName)
    kill(pid, signal.SIGTERM)
    current_spiders[spiderName].remove(pid)
    return "A spider of type %s was killed" % spiderName


#
def spawn_spider_proc(spiderName):
    file = find_files(str(spiderName + ".py"), os.getcwd())
    if len(file) > 0:
        pid = Popen(["scrapy", "runspider", file[0]]).pid
        add_spider_pid(spiderName, pid)
        return "A spider of type %s was spawned" % spiderName
    return "No spider with name %s" % spiderName


def start_spiders():
    config = SpiderStartConfig(**mongo_client["spider-config"].find_one())

    for spider in config.spiders:
        for x in range(spider.no):
            print("Deploying spider %s" % spider.name)
            time.sleep(0.2)
            spawn_spider_proc(spider.name)


def get_random_spider_pid(spider_name):
    if spider_name in current_spiders and len(current_spiders[spider_name]) > 0:
        return secrets.choice(current_spiders[spider_name])
    raise Exception("No running spiders")


def add_spider_pid(spider_name, pid):
    if spider_name in current_spiders:
        current_spiders[spider_name].append(pid)
    else:
        current_spiders[spider_name] = [pid]


def flask_logger():
    """creates logging information"""
    with open("/usr/src/crawler/logs/sc_crawler.log") as log_info:
        for i in range(25):
            data = log_info.read()
            yield data.encode()
            time.sleep(1)


@app.route("/log")
def progress_log():
    def generate():
        for line in Pygtail("/usr/src/crawler/logs/sc_crawler.log", every_n=1):
            yield "data:" + str(line) + "\n\n"
            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/progress")
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/spiders", methods=["GET"])
def get_spiders():
    return current_spiders


@app.route("/<spiderName>", methods=["PUT"])
def spawn_spider(spiderName):
    return spawn_spider_proc(spiderName)


@app.route("/<spiderName>", methods=["DELETE"])
def kill_spider(spiderName):
    return kill_spider_proc(spiderName)


@app.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")


def alerts_job():
    config = SpiderStartConfig(**mongo_client["spider-config"].find_one())
    for spider in config.spiders:
        count = (
            db_session.query(SpiderAuditErrors.id)
            .filter_by(spiderName=spider.name)
            .count()
        )
        if count > spider.maxErrorsPermitted:
            yag = yagmail.SMTP(
                os.getenv("FROM_EMAIL_ADDRESS", None),
                os.getenv("FROM_EMAIL_PASSWORD", None),
                host=os.getenv("SMTP"),
                port=int(os.getenv("SMTP_PORT")),
            )
            yag.send(os.getenv("TARGET_EMAIL_ADDRESS", None), "Errors Limit Breached", "Errors limit breached for %s" % spider.name)


@app.route("/data/<target>", methods=["GET"])
def data(target):
    data_repo = DataRepository(db_session)
    data = data_repo.get_all(
        target, int(request.args.get("page")), int(request.args.get("page_size"))
    )
    return jsonify(paginate_schema.dump(data))


if __name__ == "__main__":
    initialization()
    start_spiders()

    app.run(host="0.0.0.0", port=105)
