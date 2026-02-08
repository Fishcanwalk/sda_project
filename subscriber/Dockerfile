FROM python:3.11-slim

WORKDIR /app

COPY scripts/subscriber.py /app/subscriber.py
COPY keycredentials.json /app/keycredentials.json

RUN pip install --no-cache-dir google-cloud-pubsub pymongo

CMD ["python", "subscriber.py"]