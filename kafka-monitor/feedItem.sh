#!/bin/bash
URL="https://www.evomag.ro/tv-multimedia-televizoare-led/allview/"
APP_ID="testapp"
CRAWL_ID=$(date +%s)
SPIDER_ID="get_load"

curl localhost:5343/feed -H "content-type:application/json" -d "{ \"url\": \""$URL"\", \"appid\":\""$APP_ID"\", \"crawlid\":\""$CRAWL_ID"\", \"spiderid\":\""$SPIDER_ID"\"}"
