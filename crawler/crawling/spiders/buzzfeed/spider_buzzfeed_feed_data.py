from __future__ import absolute_import

from pathlib import Path

from bs4 import BeautifulSoup


import re

from crawling.db.jpa.data import Data
from crawling.db.jpa.target import Target
from crawling.db.models.target_enum import TargetEnum
from crawling.db.mysql_client import db_session
from crawling.mongo.models.crawler_config import CrawlerConfig
from crawling.mongo.mongo_client import mongo_client
from crawling.spiders.redis_spider import RedisSpider

from crawling.db.models.news_info import NewsInfo
from crawling.db.repositories.repository import Repository
from crawling.http.api_request import APIRequest


class BuzzfeedGetSpider(RedisSpider):
    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

    def __init__(self, *args, **kwargs):
        super(BuzzfeedGetSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongo_client["config"].find_one(
                {"baseURL": re.findall("^https?:\/\/[^#?\/]+", response.request.url)[0]}
            )
        )
        if config is None:
            self._logger.info(
                "No config found. Please add one for url " + response.request.url
            )
            return

        api_request = APIRequest("https://www.buzzfeed.com")
        resp = api_request("GET", "/world.xml")

        soup = BeautifulSoup(resp.text, "lxml")
        articles = soup.findAll("item")

        target_repo = Repository(db_session, Target)
        data_repo = Repository(db_session, Data)
        target = target_repo.find_by_code(str(TargetEnum.BUZZFEED.value))

        for article in articles:
            news_info = NewsInfo()
            news_info.title = article.find("title").text
            news_info.link = article.link.next_sibling.replace("\n", "").replace(
                "\t", ""
            )
            news_info.description = article.find("description").text
            news_info.pubdate = article.find("pubdate").text

            data_repo.add(Data(info=news_info.__dict__, target=target))
            # db_session.commit()
