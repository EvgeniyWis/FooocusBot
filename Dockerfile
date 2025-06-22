FROM python:3.12-alpine
LABEL maintainer="macalistervadim"

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    libxml2-dev \
    libxslt-dev \
    libpq-dev \
    git \
    curl \
    docker-cli

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt
    
RUN mkdir /app
WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app

CMD ["python", "bot/RunBot.py"]



