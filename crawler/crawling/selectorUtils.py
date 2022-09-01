from bs4 import BeautifulSoup
from crawling.mongo.models.CrawlerConfig import SelectorsValue


def getElements(soup, config: SelectorsValue):
    if config.type == "jsSelector":
            return selectNrElement(config, soup.select(config.value))
    elif config.type == "soup":

        return selectNrElement(config, selectSoupElement(config, soup))
    else:
        return None


def selectSoupElement(config: SelectorsValue, obj:BeautifulSoup):

    if config.value:
        print(config.classValue)
        if config.classValue:
            return obj.find_all(config.value, {"class": config.classValue})
        elif config.titleValue:
            return obj.find_all(config.value, {"title": config.titleValue})
        else:
            return obj.find_all(config.value)

def selectNrElement(config: SelectorsValue, obj):

    if config.getFirstElement:

        return selectFinalElement(config, obj[0])
    return selectFinalElement(config, obj)

def selectFinalElement(config: SelectorsValue, obj):
    result = {
        None: lambda x: x,
        'href': lambda x: x["href"],
        'a.href': lambda x: x.a["href"],
        'text': lambda x: x.text
    }[config.selectElement]
    return result(obj)
