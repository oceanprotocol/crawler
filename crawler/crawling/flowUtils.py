from typing import List

from crawling.mongo.models.CrawlerConfig import Spider
from scrapy.http import Request

def getNextSpider(currentStep: str, flow: List[Spider]):
    print(flow)
    currentIndex = flow.index(currentStep)
    print(currentIndex)

    if len(flow) > currentIndex + 1:
        return flow[currentIndex + 1].value
    return None

def generateNextSpider(response, url: str, nextSpider: str):
    print(url)
    req = Request(url)
    for key in response.meta.keys():
        req.meta[key] = response.meta[key]
    req.meta['spiderid'] = nextSpider
    return req