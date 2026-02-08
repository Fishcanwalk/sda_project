# ใช้ Python Image
FROM python:3.11-slim

# ตั้งค่า Working Directory
WORKDIR /app

# ก๊อปปี้ไฟล์ที่จำเป็นเข้าไป
COPY scripts/subscriber.py .
COPY ./keycredentials.json .

# ติดตั้ง Library
RUN pip install --no-cache-dir google-cloud-pubsub pymongo

# สั่งให้รันสคริปต์
CMD ["python", "subscriber.py"]