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
WORKDIR /usr/src/crawler

# install requirements
COPY utils /usr/src/utils
COPY crawler/requirements.txt /usr/src/crawler/
RUN pip install --no-cache-dir -r requirements.txt