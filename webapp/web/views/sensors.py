from flask import Blueprint, render_template
import json
from flask import request, jsonify  # type: ignore

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
