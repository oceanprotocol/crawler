#!/bin/bash
mkdir -p logs && touch logs/sc_crawler.log
#scrapy runspider crawling/spiders/load/get_load.py &
#scrapy runspider crawling/spiders/load/load_test.py &
#scrapy runspider crawling/spiders/load/load_test.py &
#scrapy runspider crawling/spiders/load/load_test.py &
#scrapy runspider crawling/spiders/load/load_test.py &
#scrapy runspider crawling/spiders/load/load_test.py &
#nohup sh -c 'scrapy runspider crawling/spiders/buzzfeed/get_feed_data.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/sportisimo/get_pages.py > result2.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/sportisimo/get_products.py > result3.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/sportisimo/get_product_details.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/bayut/get_pages.py > result.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/bayut/get_condos.py > result2.txt' &
#nohup sh -c 'scrapy runspider crawling/spiders/bayut/get_condo_details.py > result3.txt' &

scrapy runspider crawling/spiders/bayut/get_pages.py &
scrapy runspider crawling/spiders/bayut/get_condos.py &
scrapy runspider crawling/spiders/bayut/get_condo_details.py &
tail -f logs/sc_crawler.log
