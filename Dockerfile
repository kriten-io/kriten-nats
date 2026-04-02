FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt responder.py /app
RUN apt-get update && pip3 install -r requirements.txt
ENTRYPOINT python responder.py
# docker buildx build --platform linux/amd64,linux/arm64 .