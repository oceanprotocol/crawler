from __future__ import absolute_import
from bs4 import BeautifulSoup


from crawling.spiders.redis_spider import RedisSpider

class GetCondos(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "getCondos"

    def __init__(self, *args, **kwargs):
        super(GetCondos, self).__init__(*args, **kwargs)

    def parse(self, response):
        self._logger.debug("crawled url {}".format(response.request.url))
        soup = BeautifulSoup(response.text, 'lxml')
        numb = soup.find_all("div", class_="info")
        for ccc in range(1,2):
            self._logger.debug(ccc.find_all("div", class_="title")[0].a["href"])
        yield {}

