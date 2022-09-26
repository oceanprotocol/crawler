import os
import signal
import sys
import time
from flask import Flask

from crawling.exceptions.ParsingValuesException import ParsingValuesException
from crawling.mongo.models.SpiderStartConfig import SpiderStartConfig
from crawling.mongo.mongoClient import mongoClient

app = Flask(__name__)

from array import array
from itertools import count
import secrets

from subprocess import Popen
from os import kill

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


@app.route("/", methods=["GET"])
def getSpiders():
    return currentSpiders


@app.route("/<spiderName>", methods=["PUT"])
def spawnSpider(spiderName):
    return spawnSpiderProc(spiderName)


@app.route("/<spiderName>", methods=["DELETE"])
def killSpider(spiderName):
    return killSpiderProc(spiderName)


if __name__ == "__main__":
    startSpiders()
    print("START")
    app.run(host="0.0.0.0", port=105)
