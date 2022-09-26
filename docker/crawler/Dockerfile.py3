FROM python:3.6
MAINTAINER Madison Bahmer <madison.bahmer@istresearch.com>
ARG CACHEBUST=1
# os setup
RUN apt-get update && apt-get -y install \
  python3-lxml \
  build-essential \
  libssl-dev \
  libffi-dev \
  python-dev \
  libxml2-dev \
  libxslt1-dev \
  && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/src/crawler
RUN mkdir -p /usr/src/crawler/logs
WORKDIR /usr/src/crawler

# install requirements
COPY utils /usr/src/utils
COPY crawler/requirements.txt /usr/src/crawler/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/src/utils

# move codebase over
COPY crawler /usr/src/crawler
RUN mkdir -p /usr/src/crawler/logs
RUN touch /usr/src/crawler/logs/sc_crawler.log
# override settings via localsettings.py
COPY docker/crawler/settings.py /usr/src/crawler/crawling/localsettings.py

# copy testing script into container
COPY docker/run_docker_tests.sh /usr/src/crawler/run_docker_tests.sh

# set up environment variables
ENV SQL_CON   'mysql+pymysql://usr:rootpass@mysql/db'
ENV MONGO_CON  mongodb://devroot:devroot@mongo:27017
ENV DB_NAME  int-parser
ENV QUEUE_HITS  200
ENV MONGO_DB_DATA_PATH ~/db/mongo
ENV SQL_DB_DATA_PATH ~/db/sql
ENV PARSER_REPORT_LOCATION ~/condo-reports
ENV SC_LOG_STDOUT False
ENV PYTHONPATH /usr/src/crawler

# ENV SCHEDULER_IP_ENABLED False
ENV SC_LOG_LEVEL DEBUG
ENV REDIS_PASSWORD YQV!myz_grv7grn@pzn

# run the spider

CMD ["python", "./crawling/spiders/startSpiders.py"]