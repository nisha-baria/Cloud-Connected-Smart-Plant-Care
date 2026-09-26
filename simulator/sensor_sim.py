import time
import requests
import random

API_URL = "http://127.0.0.1:8000/api/sensors/data"
LATEST_URL = "http://127.0.0.1:8000/api/devices/PLANT-001/latest"
DEVICE_ID = "PLANT-001"

moisture = 55.0
temp = 27.0
humidity = 60.0
light = 70.0

print(f"Starting IoT Sensor Simulator for {DEVICE_ID}...")

while True:
    try:
        # Check current pump status from cloud backend
        resp = requests.get(LATEST_URL, timeout=3)
        if resp.status_code == 200:
            pump_on = resp.json().get("pump_status", False)
            if pump_on:
                moisture += 6.0  # Moisture increases when pump is on
                print("[PUMP ACTIVE] Water pump is on. Soil moisture increasing...")
            else:
                moisture -= 1.5  # Natural drying
        else:
            moisture -= 1.5

        # Fluctuate other sensors smoothly
        moisture = max(10.0, min(100.0, moisture))
        temp = round(temp + random.uniform(-0.3, 0.3), 1)
        humidity = round(humidity + random.uniform(-0.5, 0.5), 1)
        light = round(light + random.uniform(-1.0, 1.0), 1)

        payload = {
            "device_id": DEVICE_ID,
            "soil_moisture": round(moisture, 1),
            "temperature": temp,
            "humidity": humidity,
            "light_level": light
        }

        post_res = requests.post(API_URL, json=payload, timeout=3)
        print(f"Sent Reading: Soil: {payload['soil_moisture']}% | Temp: {temp}°C | Pump Triggered: {post_res.json().get('pump_triggered')}")

    except Exception as e:
        print(f"Connection Error: {e}")

    time.sleep(3)