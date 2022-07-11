# syntax=docker/dockerfile:1.4
FROM python:3.10.4-slim-bullseye

LABEL org.opencontainers.image.title="GreatAI package wrapper image"
LABEL org.opencontainers.image.vendor="ScoutinScience B.V."
LABEL org.opencontainers.image.authors="andras@schmelczer.dev"
LABEL org.opencontainers.image.source="https://github.com/schmelczer/great-ai"

SHELL ["/bin/bash", "-c"]

ENV ENVIRONMENT=production

# curl is needed for the healthcheck
# build-essentials are needed for building packages
RUN DEBIAN_FRONTEND=noninteractive apt update &&\
	apt install curl build-essential -y &&\
	rm -rf /var/lib/apt/lists/*

WORKDIR /dependencies
COPY . great_ai
RUN python3 -m pip --no-cache-dir install --upgrade pip &&\
	pip install --no-cache-dir ./great_ai &&\
	rm -rf great_ai

HEALTHCHECK \
	--interval=30s \
	--timeout=180s  \
	--start-period=60s \
	--retries=5 \
	CMD [ "curl", "--fail", "http://localhost:6060/health" ]

WORKDIR /app
COPY <<EOF hello_world.py
from great_ai import GreatAI
\
@GreatAI.create
def hello_world(name: str) -> str:
	"""Learn more about GreatAI at https://great-ai.scoutinscience.com"""
	return f"Hello {name}!"
EOF

EXPOSE 6060
VOLUME /app

ENTRYPOINT ["/usr/local/bin/python3", "-m", "great_ai"]
CMD ["hello_world.py"]
