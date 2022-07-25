from __future__ import absolute_import
from bs4 import BeautifulSoup

from scrapy.http import Request
from crawling.spiders.redis_spider import RedisSpider


class GetCondosPage(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "getCondosPage"

    def __init__(self, *args, **kwargs):
        super(GetCondosPage, self).__init__(*args, **kwargs)

    def parse(self, response):
        self._logger.debug("crawled url {}".format(response.request.url))
        soup = BeautifulSoup(response.text, 'lxml')
        numb = soup.select(".pagination > li:nth-last-child(2) > a")[0].text
        for i in  range(1, int(numb)+1):
            self._logger.debug("sdad2")
            url = "https://emirates.estate/property/?tab=complex&n=" + str(i)+ "#objects"
            self._logger.debug("sdada")
            req = Request(url)

            for key in response.meta.keys():
                req.meta[key] = response.meta[key]
            req.meta['spiderid'] = 'getCondos'
            yield req

        # yield req

# https://emirates.estate/property/?tab=complex&n=8#objects
# https://emirates.estate/property/?tab=complex&n=8#objects