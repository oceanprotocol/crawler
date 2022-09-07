#!/bin/bash
URL="https://www.sportisimo.com/running"
APP_ID="testapp"
CRAWL_ID=$(date +%s)
SPIDER_ID="sportisimo_pages"

curl localhost:5343/feed -H "content-type:application/json" -d "{ \"url\": \""$URL"\", \"appid\":\""$APP_ID"\", \"crawlid\":\""$CRAWL_ID"\", \"spiderid\":\""$SPIDER_ID"\"}"
