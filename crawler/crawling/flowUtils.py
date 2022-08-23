from typing import List


from crawling.db.models.CrawlerConfig import Spider


def getNextSpider(currentStep: str, flow: List[Spider]):
    print(flow)
    currentIndex = flow.index(currentStep)
    print(currentIndex)

    if len(flow) > currentIndex + 1:
        return flow[currentIndex + 1].value
    return None

