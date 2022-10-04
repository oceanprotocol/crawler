import os
import signal
import time
from flask import Flask, Response, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pygtail import Pygtail

from crawling.db.jpa.all_models import SpiderInfoData
from crawling.db.repository import Repository
from crawling.mongo.models.SpiderStartConfig import SpiderStartConfig
from crawling.mongo.mongoClient import mongoClient
import secrets
from crawling.db.mysqlClient import db_session
from subprocess import Popen
from os import kill

app = Flask(__name__, static_folder="static/", template_folder="static/")

executors = {"default": ThreadPoolExecutor(16), "processpool": ProcessPoolExecutor(4)}

sched = BackgroundScheduler(timezone="Asia/Seoul", executors=executors)


# #
# #
#
currentSpiders = {}
#
def find_files(filename, search_path):
    result = []

    # Wlaking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result


def killSpiderProc(spiderName):
    pid = getRandomSpiderPid(spiderName)
    kill(pid, signal.SIGTERM)
    currentSpiders[spiderName].remove(pid)
    return "A spider of type %s was killed" % spiderName


#
def spawnSpiderProc(spiderName):
    file = find_files(str(spiderName + ".py"), os.getcwd())
    if len(file) > 0:
        pid = Popen(["scrapy", "runspider", file[0]]).pid
        addSpiderPid(spiderName, pid)
        return "A spider of type %s was spawned" % spiderName
    return "No spider with name %s" % spiderName


def startSpiders():
    config = SpiderStartConfig(**mongoClient["spider-config"].find_one())

    for spider in config.spiders:
        for x in range(spider.no):
            print("Deploying spider %s" % spider.name)
            time.sleep(0.2)
            spawnSpiderProc(spider.name)


def getRandomSpiderPid(spiderName):
    if spiderName in currentSpiders and len(currentSpiders[spiderName]) > 0:
        return secrets.choice(currentSpiders[spiderName])
    raise Exception("No running spiders")


def addSpiderPid(spiderName, pid):
    if spiderName in currentSpiders:
        currentSpiders[spiderName].append(pid)
    else:
        currentSpiders[spiderName] = [pid]


def flask_logger():
    """creates logging information"""
    with open("/usr/src/crawler/logs/sc_crawler.log") as log_info:
        for i in range(25):
            data = log_info.read()
            yield data.encode()
            time.sleep(1)
        # Create empty job.log, old logging will be deleted
        # open("/usr/src/crawler/logs/sc_crawler.log", "w").close()


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
def getSpiders():
    return currentSpiders


@app.route("/<spiderName>", methods=["PUT"])
def spawnSpider(spiderName):
    return spawnSpiderProc(spiderName)


@app.route("/<spiderName>", methods=["DELETE"])
def killSpider(spiderName):
    return killSpiderProc(spiderName)


@app.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")


def job():
    config = SpiderStartConfig(**mongoClient["spider-config"].find_one())
    for spider in config.spiders:
        count = (
            db_session.query(SpiderInfoData.id)
            .filter_by(spiderName=spider.name)
            .count()
        )
        if count > spider.maxErrorsPermitted:
            print("ERROR")


sched.add_job(job, "interval", seconds=30)

if __name__ == "__main__":
    repo = Repository(db_session, SpiderInfoData)
    repo.permanentDeleteAll()
    db_session.commit()
    startSpiders()
    print("START")
    sched.start()
    app.run(host="0.0.0.0", port=105)
