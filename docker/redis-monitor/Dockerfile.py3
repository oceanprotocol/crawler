FROM python:3.6
MAINTAINER Madison Bahmer <madison.bahmer@istresearch.com>

# os setup
RUN apt-get update
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY utils /usr/src/utils
COPY redis-monitor/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/src/utils

# ENV
ENV LOG_STDOUT False
ENV LOG_LEVEL DEBUG
ENV STATS_PLUGINS True
ENV REDIS_PASSWORD YQV!myz_grv7grn@pzn

# move codebase over
COPY redis-monitor /usr/src/app

# override settings via localsettings.py
COPY docker/redis-monitor/settings.py /usr/src/app/localsettings.py
COPY docker/redis-monitor/run.sh /usr/src/app/run.sh
# copy testing script into container
COPY docker/run_docker_tests.sh /usr/src/app/run_docker_tests.sh

# set up environment variables

# run command
CMD ["sh", "run.sh"]