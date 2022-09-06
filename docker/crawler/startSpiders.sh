#!/bin/bash
touch result.txt
nohup sh -c 'scrapy runspider crawling/spiders/load/get_load.py > result2.txt' &
nohup sh -c 'scrapy runspider crawling/spiders/load/load_test.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/buzzfeed/get_feed_data.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/sportisimo/get_pages.py > result2.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/sportisimo/get_products.py > result3.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/sportisimo/get_product_details.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/bayut/get_pages.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/bayut/get_condos.py > result2.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/bayut/get_condo_details.py > result3.txt' &
tail -f result.txt