#!/usr/bin/env python3
# filepath: scripts/seed_sensor_data.py
"""
Script to generate sensor data for testing
Usage:
    python scripts/seed_sensor_data.py              # Generate 100 records per sensor
    python scripts/seed_sensor_data.py -c 500       # Generate 500 records per sensor
    python scripts/seed_sensor_data.py --clear      # Clear existing data first
    python scripts/seed_sensor_data.py --rain-only  # Generate only rain sensor data
"""
import sys
import os
import random
import datetime
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from webapp.models import sensors
import mongoengine as me


def connect_db():
    """Connect to MongoDB"""
    load_dotenv()
    db_name = os.getenv("MONGODB_DB", "iotdb")
    db_host = os.getenv("MONGODB_HOST", "localhost")
    db_port = int(os.getenv("MONGODB_PORT", 27017))

    me.connect(db_name, host=db_host, port=db_port)
    print(f"✓ Connected to MongoDB: {db_host}:{db_port}/{db_name}")


def generate_timestamps(count=100, hours_back=None):
    """
    Generate timestamps
    Args:
        count: number of timestamps to generate
        hours_back: if None, spread over 'count' hours; if set, spread over this many hours
    """
    now = datetime.datetime.now()
    if hours_back is None:
        hours_back = count

    timestamps = []
    for i in range(count):
        # Distribute evenly over the time range
        hours_offset = (i / count) * hours_back
        ts = now - datetime.timedelta(hours=hours_offset)
        timestamps.append(ts)

    return timestamps


def seed_rain_sensors(count=100):
    """
    Generate rain sensor data
    Realistic range: 0-50mm per reading
    """
    print(f"\n📊 Generating {count} rain sensor records...")
    timestamps = generate_timestamps(count)

    created = 0
    for i, ts in enumerate(timestamps):
        # Rain is often 0, with occasional spikes
        if random.random() < 0.7:  # 70% chance of no rain
            value = 0.0
        else:
            value = round(random.uniform(0.1, 50), 2)

        rain = sensors.RainSensor(
            title=f"Rain Sensor Node-{i % 5 + 1}",  # Simulate 5 nodes
            value=value,
            timestamp=ts,
        )
        rain.save()
        created += 1

    print(f"✓ Created {created} rain sensor records")
    return created


def seed_temperature_sensors(count=100):
    """
    Generate temperature sensor data
    Realistic range: 15-40°C with daily pattern
    """
    print(f"\n🌡️  Generating {count} temperature sensor records...")
    timestamps = generate_timestamps(count)

    created = 0
    for i, ts in enumerate(timestamps):
        # Simulate daily temperature pattern
        hour = ts.hour

        # Base temperature varies by time of day
        if 6 <= hour < 12:  # Morning
            base_temp = random.uniform(20, 28)
        elif 12 <= hour < 18:  # Afternoon (hottest)
            base_temp = random.uniform(28, 40)
        elif 18 <= hour < 22:  # Evening
            base_temp = random.uniform(22, 30)
        else:  # Night (coolest)
            base_temp = random.uniform(15, 25)

        value = round(base_temp + random.uniform(-2, 2), 2)

        temp = sensors.TemperatureSensor(
            title=f"Temperature Sensor Node-{i % 5 + 1}", value=value, timestamp=ts
        )
        temp.save()
        created += 1

    print(f"✓ Created {created} temperature sensor records")
    return created


def seed_light_sensors(count=100):
    """
    Generate light sensor data
    Realistic range: 0-10000 lux with day/night pattern
    """
    print(f"\n💡 Generating {count} light sensor records...")
    timestamps = generate_timestamps(count)

    created = 0
    for i, ts in enumerate(timestamps):
        hour = ts.hour

        # Simulate day/night light pattern
        if 6 <= hour < 18:  # Daytime
            value = round(random.uniform(1000, 10000), 2)
        elif 5 <= hour < 6 or 18 <= hour < 19:  # Dawn/Dusk
            value = round(random.uniform(100, 1000), 2)
        else:  # Night
            value = round(random.uniform(0, 100), 2)

        light = sensors.LightSensor(
            title=f"Light Sensor Node-{i % 5 + 1}", value=value, timestamp=ts
        )
        light.save()
        created += 1

    print(f"✓ Created {created} light sensor records")
    return created


def seed_humidity_sensors(count=100):
    """
    Generate humidity sensor data
    Realistic range: 20-100%
    """
    print(f"\n💧 Generating {count} humidity sensor records...")
    timestamps = generate_timestamps(count)

    created = 0
    for i, ts in enumerate(timestamps):
        # Higher humidity at night, lower during hot afternoon
        hour = ts.hour

        if 6 <= hour < 12:  # Morning
            base_humidity = random.uniform(60, 80)
        elif 12 <= hour < 18:  # Afternoon (driest)
            base_humidity = random.uniform(40, 60)
        else:  # Night/Evening (most humid)
            base_humidity = random.uniform(70, 95)

        value = round(base_humidity + random.uniform(-5, 5), 2)
        value = max(20, min(100, value))  # Clamp to 20-100

        humidity = sensors.HumiditySensor(
            title=f"Humidity Sensor Node-{i % 5 + 1}", value=value, timestamp=ts
        )
        humidity.save()
        created += 1

    print(f"✓ Created {created} humidity sensor records")
    return created


def clear_all_sensors():
    """Clear all sensor data from all collections"""
    print("\n🗑️  Clearing all sensor data...")

    rain_count = sensors.RainSensor.objects.delete()
    temp_count = sensors.TemperatureSensor.objects.delete()
    light_count = sensors.LightSensor.objects.delete()
    humidity_count = sensors.HumiditySensor.objects.delete()

    total = rain_count + temp_count + light_count + humidity_count
    print(f"✓ Cleared {total} total records")
    print(f"  - Rain: {rain_count}")
    print(f"  - Temperature: {temp_count}")
    print(f"  - Light: {light_count}")
    print(f"  - Humidity: {humidity_count}")


def show_stats():
    """Show statistics of generated data"""
    print("\n📈 Current Data Statistics:")
    print(f"  Rain sensors:        {sensors.RainSensor.objects.count():>6} records")
    print(
        f"  Temperature sensors: {sensors.TemperatureSensor.objects.count():>6} records"
    )
    print(f"  Light sensors:       {sensors.LightSensor.objects.count():>6} records")
    print(f"  Humidity sensors:    {sensors.HumiditySensor.objects.count():>6} records")

    # Show latest record from each
    print("\n📋 Latest Records:")

    latest_rain = sensors.RainSensor.objects.order_by("-timestamp").first()
    if latest_rain:
        print(
            f"  Rain:        {latest_rain.value:>6.2f} mm    @ {latest_rain.timestamp}"
        )

    latest_temp = sensors.TemperatureSensor.objects.order_by("-timestamp").first()
    if latest_temp:
        print(
            f"  Temperature: {latest_temp.value:>6.2f} °C   @ {latest_temp.timestamp}"
        )

    latest_light = sensors.LightSensor.objects.order_by("-timestamp").first()
    if latest_light:
        print(
            f"  Light:       {latest_light.value:>6.2f} lux  @ {latest_light.timestamp}"
        )

    latest_humidity = sensors.HumiditySensor.objects.order_by("-timestamp").first()
    if latest_humidity:
        print(
            f"  Humidity:    {latest_humidity.value:>6.2f} %    @ {latest_humidity.timestamp}"
        )


def main():
    """Main function with argument parsing"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate sensor data for testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/seed_sensor_data.py                    # Generate 100 records per sensor
  python scripts/seed_sensor_data.py -c 500             # Generate 500 records per sensor
  python scripts/seed_sensor_data.py --clear            # Clear existing data first
  python scripts/seed_sensor_data.py --rain-only -c 200 # Generate only rain data
  python scripts/seed_sensor_data.py --stats            # Show current statistics
        """,
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=100,
        help="Number of records per sensor type (default: 100)",
    )
    parser.add_argument(
        "--clear", action="store_true", help="Clear existing data before generating"
    )
    parser.add_argument(
        "--rain-only", action="store_true", help="Generate only rain sensor data"
    )
    parser.add_argument(
        "--temp-only", action="store_true", help="Generate only temperature sensor data"
    )
    parser.add_argument(
        "--light-only", action="store_true", help="Generate only light sensor data"
    )
    parser.add_argument(
        "--humidity-only",
        action="store_true",
        help="Generate only humidity sensor data",
    )
    parser.add_argument("--stats", action="store_true", help="Show statistics and exit")

    args = parser.parse_args()

    # Connect to database
    connect_db()

    # Show stats and exit if requested
    if args.stats:
        show_stats()
        return

    # Clear data if requested
    if args.clear:
        clear_all_sensors()

    # Generate data based on flags
    total_created = 0

    if args.rain_only:
        total_created += seed_rain_sensors(args.count)
    elif args.temp_only:
        total_created += seed_temperature_sensors(args.count)
    elif args.light_only:
        total_created += seed_light_sensors(args.count)
    elif args.humidity_only:
        total_created += seed_humidity_sensors(args.count)
    else:
        # Generate all sensor types
        total_created += seed_rain_sensors(args.count)
        total_created += seed_temperature_sensors(args.count)
        total_created += seed_light_sensors(args.count)
        total_created += seed_humidity_sensors(args.count)

    print(f"\n✅ Successfully generated {total_created} total records!")

    # Show final statistics
    show_stats()


if __name__ == "__main__":
    main()
