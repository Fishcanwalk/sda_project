from flask import Blueprint, render_template
import json
from flask import request, jsonify  # type: ignore
import datetime

from webapp.web.utils.acl import roles_required
from ...models import sensors

module = Blueprint("sensors", __name__, url_prefix="/sensors")


@module.route("/")
@roles_required("user", "admin")
def index():
    # Get latest readings from all sensor types to check if they're active
    latest_temp = sensors.TemperatureSensor.objects.order_by("-timestamp").first()
    latest_humidity = sensors.HumiditySensor.objects.order_by("-timestamp").first()
    latest_light = sensors.LightSensor.objects.order_by("-timestamp").first()
    latest_rain = sensors.RainSensor.objects.order_by("-timestamp").first()
    latest_smoke = sensors.SmokeSensor.objects.order_by("-timestamp").first()
    
    # Check if data is recent (within last 5 minutes)
    now = datetime.datetime.now()
    threshold = datetime.timedelta(minutes=5)
    
    sensors_status = {
        "temperature": {
            "active": latest_temp and (now - latest_temp.timestamp) < threshold,
            "last_update": latest_temp.timestamp if latest_temp else None,
            "value": latest_temp.value if latest_temp else None,
        },
        "humidity": {
            "active": latest_humidity and (now - latest_humidity.timestamp) < threshold,
            "last_update": latest_humidity.timestamp if latest_humidity else None,
            "value": latest_humidity.value if latest_humidity else None,
        },
        "light": {
            "active": latest_light and (now - latest_light.timestamp) < threshold,
            "last_update": latest_light.timestamp if latest_light else None,
            "value": latest_light.value if latest_light else None,
        },
        "rain": {
            "active": latest_rain and (now - latest_rain.timestamp) < threshold,
            "last_update": latest_rain.timestamp if latest_rain else None,
            "value": latest_rain.value if latest_rain else None,
        },
        "smoke": {
            "active": latest_smoke and (now - latest_smoke.timestamp) < threshold,
            "last_update": latest_smoke.timestamp if latest_smoke else None,
            "value": latest_smoke.value if latest_smoke else None,
        },
    }
    
    return render_template("/sensors/index.html", sensors_status=sensors_status)

@module.route("/view")
@roles_required("user", "admin")
def view():
    return render_template("/sensors/view.html")


@module.route("/temperature/latest")
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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
@roles_required("user", "admin")
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

@module.route("/smoke/latest")
@roles_required("user", "admin")
def smoke_latest():
    latest = sensors.SmokeSensor.objects.order_by("-timestamp").first()
    if not latest:
        return jsonify({"error": "No data"}), 404

    day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
    recent = sensors.SmokeSensor.objects.filter(timestamp__gte=day_ago)
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

@module.route("/smoke/history")
@roles_required("user", "admin")
def smoke_history():
    from flask import request

    hours = int(request.args.get("hours", 24))
    time_ago = datetime.datetime.now() - datetime.timedelta(hours=hours)

    readings = (
        sensors.SmokeSensor.objects.filter(timestamp__gte=time_ago)
        .order_by("timestamp")
        .limit(100)
    )

    return jsonify(
        [{"value": r.value, "timestamp": r.timestamp.isoformat()} for r in readings]
    )
