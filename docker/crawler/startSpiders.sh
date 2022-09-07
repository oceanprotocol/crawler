#!/bin/bash
mkdir -p logs && touch logs/sc_crawler.log

cd crawling/spiders
for i in `find . -type f -name "spider*"` ; do
    scrapy runspider "$i" &
done

tail -f /usr/src/app/logs/sc_crawler.log

