from flask import Blueprint, render_template
import json
from flask import request, jsonify  # type: ignore
import datetime
from ...models import sensors

module = Blueprint("sensors", __name__, url_prefix="/sensors")


@module.route("/")
def index():
    return render_template("/sensors/index.html")


@module.route("/view")
def view():
    return render_template("/sensors/view.html")


@module.route("/update-sensor", methods=["POST"])
def update_sensor():
    # 1. รับข้อมูล JSON ที่ส่งมาจาก Pi
    print("555555555555555555555555555555555")
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    # 2. ดึงค่าแต่ละตัวออกมา (ตัวอย่าง: รับค่า temp และ device_id)
    device_id = data.get("device_id")
    temp = data.get("temperature")

    # 3. นำไปใช้งาน (เช่น Print ดู หรือบันทึกลงฐานข้อมูล)
    print(f"Received from {device_id}: {temp} C")

    return (
        jsonify({"status": "success", "message": f"Data received for {device_id}"}),
        200,
    )


@module.route("/temperature/latest")
def temperature_latest():
    """Get latest temperature reading with stats"""
    latest = sensors.TemperatureSensor.objects.order_by("-timestamp").first()
    if not latest:
        return jsonify({"error": "No data"}), 404

    # Get min/max from last 24 hours
    day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
    recent = sensors.TemperatureSensor.objects.filter(timestamp__gte=day_ago)

    values = [s.value for s in recent]

    return jsonify(
        {
            "value": latest.value,
            "timestamp": latest.timestamp.isoformat(),
            "title": latest.title,
            "min": min(values) if values else latest.value,
            "max": max(values) if values else latest.value,
        }
    )


@module.route("/temperature/history")
def temperature_history():
    """Get temperature history for last N hours"""
    from flask import request

    hours = int(request.args.get("hours", 24))

    time_ago = datetime.datetime.now() - datetime.timedelta(hours=hours)
    readings = (
        sensors.TemperatureSensor.objects.filter(timestamp__gte=time_ago)
        .order_by("timestamp")
        .limit(100)
    )

    return jsonify(
        [{"value": r.value, "timestamp": r.timestamp.isoformat()} for r in readings]
    )


@module.route("/humidity/latest")
def humidity_latest():
    latest = sensors.HumiditySensor.objects.order_by("-timestamp").first()
    if not latest:
        return jsonify({"error": "No data"}), 404

    day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
    recent = sensors.HumiditySensor.objects.filter(timestamp__gte=day_ago)
    values = [s.value for s in recent]

    return jsonify(
        {
            "value": latest.value,
            "timestamp": latest.timestamp.isoformat(),
            "title": latest.title,
            "min": min(values) if values else latest.value,
            "max": max(values) if values else latest.value,
        }
    )


@module.route("/humidity/history")
def humidity_history():
    from flask import request

    hours = int(request.args.get("hours", 24))
    time_ago = datetime.datetime.now() - datetime.timedelta(hours=hours)

    readings = (
        sensors.HumiditySensor.objects.filter(timestamp__gte=time_ago)
        .order_by("timestamp")
        .limit(100)
    )

    return jsonify(
        [{"value": r.value, "timestamp": r.timestamp.isoformat()} for r in readings]
    )


@module.route("/light/latest")
def light_latest():
    latest = sensors.LightSensor.objects.order_by("-timestamp").first()
    if not latest:
        return jsonify({"error": "No data"}), 404

    day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
    recent = sensors.LightSensor.objects.filter(timestamp__gte=day_ago)
    values = [s.value for s in recent]

    return jsonify(
        {
            "value": latest.value,
            "timestamp": latest.timestamp.isoformat(),
            "title": latest.title,
            "min": min(values) if values else latest.value,
            "max": max(values) if values else latest.value,
        }
    )


@module.route("/light/history")
def light_history():
    from flask import request

    hours = int(request.args.get("hours", 24))
    time_ago = datetime.datetime.now() - datetime.timedelta(hours=hours)

    readings = (
        sensors.LightSensor.objects.filter(timestamp__gte=time_ago)
        .order_by("timestamp")
        .limit(100)
    )

    return jsonify(
        [{"value": r.value, "timestamp": r.timestamp.isoformat()} for r in readings]
    )


@module.route("/rain/latest")
def rain_latest():
    latest = sensors.RainSensor.objects.order_by("-timestamp").first()
    if not latest:
        return jsonify({"error": "No data"}), 404

    # Calculate today's total rainfall
    today_start = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    today_readings = sensors.RainSensor.objects.filter(timestamp__gte=today_start)
    total_today = sum(r.value for r in today_readings)

    day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
    recent = sensors.RainSensor.objects.filter(timestamp__gte=day_ago)
    values = [s.value for s in recent]

    return jsonify(
        {
            "value": latest.value,
            "timestamp": latest.timestamp.isoformat(),
            "title": latest.title,
            "total_today": total_today,
            "min": min(values) if values else 0,
            "max": max(values) if values else latest.value,
        }
    )


@module.route("/rain/history")
def rain_history():
    from flask import request

    hours = int(request.args.get("hours", 24))
    time_ago = datetime.datetime.now() - datetime.timedelta(hours=hours)

    readings = (
        sensors.RainSensor.objects.filter(timestamp__gte=time_ago)
        .order_by("timestamp")
        .limit(100)
    )

    return jsonify(
        [{"value": r.value, "timestamp": r.timestamp.isoformat()} for r in readings]
    )
