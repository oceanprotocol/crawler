FROM python:3.6
MAINTAINER Madison Bahmer <madison.bahmer@istresearch.com>

# os setup
RUN apt-get update
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# move codebase over and install requirements
COPY utils /usr/src/app
RUN pip install .
RUN pip install nose
ENV REDIS_PASSWORD YQV!myz_grv7grn@pzn


# set up environment variables

# run command
CMD ["ping", "localhost"]