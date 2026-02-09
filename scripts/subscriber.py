import json
import os
import datetime
from google.cloud import pubsub_v1
from pymongo import MongoClient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./keycredentials.json"
project_id = "sda-project-486506"
subscription_id = "sensor-data-sub"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(MONGO_URI)
db = client["iotdb"]


def callback(message):
    try:
        raw_data = json.loads(message.data.decode("utf-8"))
        ts = datetime.datetime.fromtimestamp(
            raw_data.get("timestamp", datetime.datetime.now().timestamp())
        )

        db["temp_sensor"].insert_one(
            {
                "title": "Temperature Reading",
                "value": float(raw_data.get("temperature", 0)),
                "timestamp": ts,
            }
        )

        # Humidity Sensor
        db["humidity_sensor"].insert_one(
            {
                "title": "Humidity Reading",
                "value": float(raw_data.get("humidity", 0)),
                "timestamp": ts,
            }
        )

        # Light Sensor (Boolean)
        db["light_sensor"].insert_one(
            {
                "title": "Light Status",
                "value": bool(raw_data.get("is_dark")),  # บันทึกเป็น Boolean
                "timestamp": ts,
            }
        )

        # Rain Sensor (Boolean)
        db["rain_sensor"].insert_one(
            {
                "title": "Rain Status",
                "value": bool(raw_data.get("is_raining")),  # บันทึกเป็น Boolean
                "timestamp": ts,
            }
        )
        db["smoke_sensor"].insert_one(
            {
                "title": "Smoke Status",
                "value": bool(raw_data.get("is_smoke")),
                "timestamp": ts,
            }
        )
        message.ack()
    except Exception as e:
        print(f"❌ Error during transformation/save: {e}")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"Listening for messages on {subscription_id} and routing to 4 collections...")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

with subscriber:
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
