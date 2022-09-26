from __future__ import absolute_import

from pathlib import Path

from scrapy.spiders import Spider, Request



class GetLoad(Spider):
    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem
    c = 0

    def __init__(self, *args, **kwargs):
        super(GetLoad, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request("http://www.example.com/1.html", self.parse)
        yield Request("http://www.example.com/2.html", self.parse)
        yield Request("http://www.example.com/3.html", self.parse)

    def parse(self, response):

        for href in response.xpath("//a/@href").getall():
            yield Request(response.urljoin(href), self.parse)
