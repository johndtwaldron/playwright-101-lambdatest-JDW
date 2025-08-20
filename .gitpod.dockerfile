FROM python:3.10-slim
# python 3 13 0 ?
# Optional cleanup and pip install speed-up
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace