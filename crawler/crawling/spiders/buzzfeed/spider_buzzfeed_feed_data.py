from __future__ import absolute_import

from pathlib import Path

from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider

from crawling.db.jpa.all_models import Client, Data
from crawling.db.models.newsInfo import NewsInfo
from crawling.db.mysqlClient import db_session
from crawling.db.repository import Repository
from crawling.http.api_request import APIRequest


class BuzzfeedGetSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = Path(__file__).stem
    def __init__(self,  *args, **kwargs):
        super(BuzzfeedGetSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))
        if config is None:
            self._logger.info("No config found. Please add one for url " + response.request.url)
            return


        api_request = APIRequest('https://www.buzzfeed.com')
        resp = api_request('GET', '/world.xml')

        soup = BeautifulSoup(resp.text, 'lxml')
        articles = soup.findAll('item')

        repoClient = Repository(db_session, Client)
        repo = Repository(db_session, Data)
        client = repoClient.find_by_code('BUZZFEED')


        for article in articles:
            newsInfo = NewsInfo()
            newsInfo.title = article.find('title').text
            newsInfo.link = article.link.next_sibling.replace('\n', '').replace('\t', '')
            newsInfo.description = article.find('description').text
            newsInfo.pubdate = article.find('pubdate').text

            repo.add(Data(info=newsInfo.__dict__, client=client))
            db_session.commit()

