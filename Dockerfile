FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app
COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt
COPY ["configs.yaml", "Makefile", "./"]
COPY src/ src/