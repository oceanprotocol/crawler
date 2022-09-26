from scrapy.http import Request


def generateNextSpider(response, url: str, nextSpider: str):
    req = Request(url)
    for key in response.meta.keys():
        req.meta[key] = response.meta[key]
    req.meta['spiderid'] = nextSpider
    return req