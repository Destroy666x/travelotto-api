FROM python:3.7.1
 
WORKDIR /api
 
ENV PYTHONUNBUFFERED 1
ENV PIPENV_USE_SYSTEM 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    vim \
    git \
    htop \
    libgdal-dev \
    python-numpy \
    && apt-get purge -y --auto-remove \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install pipenv

COPY entrypoint.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
