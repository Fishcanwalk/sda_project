import json
import os
from google.cloud import pubsub_v1
from pymongo import MongoClient
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keycredentials.json"
project_id = "sda-project-486506"
subscription_id = "sensor-data-topic-sub"

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["iotdb"]
collection = db["sensors"]


def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))

        result = collection.insert_one(data)
        print(
            f"✅ Received & Saved: {data['device_id'] if 'device_id' in data else 'Unknown'} | MongoID: {result.inserted_id}"
        )

        message.ack()

    except Exception as e:
        print(f"❌ Error: {e}")


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"Listening for messages on {subscription_id}...")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

with subscriber:
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
