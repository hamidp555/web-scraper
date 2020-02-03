FROM python:3.8.0-alpine
LABEL maintainer="hamid.poursepanj"

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && apk add --no-cache --virtual .build-deps gcc musl-dev openssl-dev python3-dev libffi-dev  \
    && apk add \
    curl \
    bash \
    libxslt-dev \
    libxml2-dev \
    && curl -Lo /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64 \
    && chmod +x /usr/local/bin/dumb-init \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY scraperapp scraperapp/
COPY ./scrapy.cfg .
COPY ./crawl_config.yaml .
COPY ./run.py .
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]

CMD [ "./entrypoint.sh"]
