FROM python:3.10.4-slim-bullseye

LABEL org.opencontainers.image.title="GreatAI package wrapper container"
LABEL org.opencontainers.image.vendor="ScoutinScience B.V."
LABEL org.opencontainers.image.authors="andras@schmelczer.dev"
LABEL org.opencontainers.image.source="https://github.com/ScoutinScience/great_ai"

ENV ENVIRONMENT production
EXPOSE 6060

RUN DEBIAN_FRONTEND=noninteractive apt update &&\
    apt install curl -y &&\
    rm -rf /var/lib/apt/lists/*

COPY . great_ai
RUN pip3 install --no-cache-dir ./great_ai &&\
    rm -rf great_ai

RUN pip3 install --no-cache-dir en-core-web-sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.3.0/en_core_web_sm-3.3.0-py3-none-any.whl

HEALTHCHECK --interval=60s --timeout=60s --start-period=90s --retries=5 CMD [ "curl", "--fail", "http://localhost:6060/health" ]

WORKDIR /app
VOLUME /app

ENTRYPOINT ["/bin/sh", "python3", "-m", "great_ai"]
