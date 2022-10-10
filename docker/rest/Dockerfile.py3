FROM python:3.6
MAINTAINER Madison Bahmer <madison.bahmer@istresearch.com>

# os setup
RUN apt-get update
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY utils /usr/src/utils
COPY rest/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/src/utils

# move codebase over
COPY rest /usr/src/app

# override settings via localsettings.py
COPY docker/rest/settings.py /usr/src/app/localsettings.py

COPY docker/rest/run.sh /usr/src/app/run.sh

# set up environment variables

# run command
CMD ["sh", "run.sh"]