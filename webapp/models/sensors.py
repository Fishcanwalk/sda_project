import mongoengine as me
import datetime


class Sensor(me.Document):
    """Base sensor model - stores all sensor types in one collection"""

    title = me.StringField(required=True)
    value = me.FloatField(required=True)
    timestamp = me.DateTimeField(required=True, default=datetime.datetime.now)
    sensor_type = me.StringField(
        required=True, choices=["rain", "temperature", "light", "humidity"]
    )

    meta = {"collection": "sensors"}  # ใช้ collection เดียว แยกด้วย sensor_type


# หรือถ้าต้องการแยก collection จริงๆ ให้สร้าง 4 classes:


class RainSensor(me.Document):
    title = me.StringField(required=True)
    value = me.BooleanField(required=False)
    timestamp = me.DateTimeField(required=True, default=datetime.datetime.now)

    meta = {"collection": "rain_sensor"}


class TemperatureSensor(me.Document):
    title = me.StringField(required=True)
    value = me.FloatField(required=True)  # celsius
    timestamp = me.DateTimeField(required=True, default=datetime.datetime.now)

    meta = {"collection": "temp_sensor"}


class LightSensor(me.Document):
    title = me.StringField(required=True)
    value = me.BooleanField(required=False)
    timestamp = me.DateTimeField(required=True, default=datetime.datetime.now)

    meta = {"collection": "light_sensor"}


class HumiditySensor(me.Document):
    title = me.StringField(required=True)
    value = me.FloatField(required=True)  # percent
    timestamp = me.DateTimeField(required=True, default=datetime.datetime.now)

    meta = {"collection": "humidity_sensor"}
    

class SmokeSensor(me.Document):
    title = me.StringField(required=True)
    value = me.FloatField(required=True)  # ppm
    timestamp = me.DateTimeField(required=True, default=datetime.datetime.now)

    meta = {"collection": "smoke_sensor"}
