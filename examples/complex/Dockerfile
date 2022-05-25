FROM python:3.8.12-slim-bullseye

ENV ENVIRONMENT production

WORKDIR /app

RUN apt-get update &&\
    apt-get install curl -y &&\
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir en-core-web-sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.3.0/en_core_web_sm-3.3.0-py3-none-any.whl
COPY sus sus
RUN pip install --no-cache-dir --use-feature=in-tree-build ./sus

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY . .
RUN rm -rf sus secrets

EXPOSE 5000

HEALTHCHECK --interval=60s --timeout=60s --start-period=90s --retries=5 CMD [ "curl", "--fail", "http://localhost:5000/health" ]

CMD ["uvicorn", "main:app", "--proxy-headers", "--backlog", "8196", "--timeout-keep-alive", "900", "--host", "0.0.0.0", "--port", "5000"]
