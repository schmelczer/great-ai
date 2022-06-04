FROM python:3.10.4-slim-bullseye

ENV ENVIRONMENT production

ARG ENTRYPOINT main.py

WORKDIR /app

RUN apt-get update &&\
    apt-get install curl -y &&\
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir en-core-web-sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.3.0/en_core_web_sm-3.3.0-py3-none-any.whl
COPY great_ai great_ai
RUN pip install --no-cache-dir ./great_ai

# COPY requirements.txt ./
# RUN pip install --no-cache-dir --requirement requirements.txt

COPY . .
RUN rm -rf great_ai

EXPOSE 6060

HEALTHCHECK --interval=60s --timeout=60s --start-period=90s --retries=5 CMD [ "curl", "--fail", "http://localhost:6060/health" ]

CMD ["great_ai", "$ENTRYPOINT"]
