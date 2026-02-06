from flask import Blueprint, render_template, Flask, request, jsonify

module = Blueprint("data", __name__, url_prefix="/data")


@module.route("/api/sensor-data", methods=["POST"])
def receive_data():
    data = request.json  # This grabs the JSON sent by the Pi
    print(
        f"Received from {data['device_id']}: Temp={data['temperature']}°C, Dark={data['is_dark']}"
    )

    return jsonify({"status": "success", "message": "Data received"}), 200
