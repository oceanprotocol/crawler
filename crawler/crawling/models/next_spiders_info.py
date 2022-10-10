from typing import List


class NextSpidersInfo:
    nextSpider: str
    urls: List[str]
    timeoutTime: float

    def __init__(self, nextSpider, urls, timeoutTime=0):
        self.nextSpider = nextSpider
        self.urls = urls
        self.timeoutTime = timeoutTime
