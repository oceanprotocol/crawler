#!/bin/bash
mkdir -p logs && touch logs/sc_crawler.log && touch logs/pid.log

cd crawling/spiders
for i in `find . -type f -name "spider*"` ; do
    scrapy runspider "$i" &
    FOO_PID=$!
    echo -e $FOO_PID >> pid.log
    echo -e "\n" >> pid.log
done
#scrapy runspider .load/spider_load_test.py &
tail -f /usr/src/crawler/logs/sc_crawler.log

