from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import database

database.init_db()
app = FastAPI(title="Smart Plant Care Cloud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorPayload(BaseModel):
    device_id: str
    soil_moisture: float
    temperature: float
    humidity: float
    light_level: float

class ThresholdUpdate(BaseModel):
    moisture_threshold: float

@app.post("/api/sensors/data")
def receive_sensor_data(payload: SensorPayload):
    conn = database.get_connection()
    cursor = conn.cursor()
    now_str = datetime.utcnow().isoformat()
    
    # Reading save karo
    cursor.execute("""
    INSERT INTO readings (device_id, soil_moisture, temperature, humidity, light_level, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (payload.device_id, payload.soil_moisture, payload.temperature, payload.humidity, payload.light_level, now_str))
    
    # Threshold check karo
    cursor.execute("SELECT moisture_threshold, pump_status FROM devices WHERE device_id = ?", (payload.device_id,))
    row = cursor.fetchone()
    
    pump_action = False
    if row:
        threshold, current_pump = row[0], row[1]
        if payload.soil_moisture < threshold and current_pump == 0:
            cursor.execute("UPDATE devices SET pump_status = 1 WHERE device_id = ?", (payload.device_id,))
            cursor.execute("""
            INSERT INTO watering_events (device_id, trigger_type, moisture_level, timestamp)
            VALUES (?, 'AUTO', ?, ?)
            """, (payload.device_id, payload.soil_moisture, now_str))
            pump_action = True
        elif payload.soil_moisture >= threshold and current_pump == 1:
            cursor.execute("UPDATE devices SET pump_status = 0 WHERE device_id = ?", (payload.device_id,))
    
    cursor.execute("UPDATE devices SET last_seen = ? WHERE device_id = ?", (now_str, payload.device_id))
    conn.commit()
    conn.close()
    
    return {"status": "success", "pump_triggered": pump_action}

@app.get("/api/devices/{device_id}/latest")
def get_latest(device_id: str):
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT plant_name, moisture_threshold, pump_status, last_seen FROM devices WHERE device_id = ?", (device_id,))
    dev = cursor.fetchone()
    if not dev:
        conn.close()
        raise HTTPException(status_code=404, detail="Device not found")
        
    cursor.execute("""
    SELECT soil_moisture, temperature, humidity, light_level, timestamp
    FROM readings WHERE device_id = ? ORDER BY id DESC LIMIT 1
    """, (device_id,))
    reading = cursor.fetchone()
    conn.close()
    
    return {
        "device_id": device_id,
        "plant_name": dev[0],
        "threshold": dev[1],
        "pump_status": bool(dev[2]),
        "last_seen": dev[3],
        "reading": {
            "soil_moisture": reading[0] if reading else None,
            "temperature": reading[1] if reading else None,
            "humidity": reading[2] if reading else None,
            "light_level": reading[3] if reading else None,
            "timestamp": reading[4] if reading else None
        } if reading else None
    }

@app.get("/api/devices/{device_id}/history")
def get_history(device_id: str, limit: int = 15):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT soil_moisture, temperature, humidity, timestamp
    FROM readings WHERE device_id = ? ORDER BY id DESC LIMIT ?
    """, (device_id, limit))
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse kari ne chronological order ma apo
    rows.reverse()
    return {
        "device_id": device_id,
        "history": [
            {
                "soil_moisture": r[0],
                "temperature": r[1],
                "humidity": r[2],
                "timestamp": r[3]
            } for r in rows
        ]
    }

@app.post("/api/devices/{device_id}/water")
def manual_water(device_id: str):
    conn = database.get_connection()
    cursor = conn.cursor()
    now_str = datetime.utcnow().isoformat()
    cursor.execute("UPDATE devices SET pump_status = 1 WHERE device_id = ?", (device_id,))
    cursor.execute("""
    INSERT INTO watering_events (device_id, trigger_type, moisture_level, timestamp)
    VALUES (?, 'MANUAL', 0.0, ?)
    """, (device_id, now_str))
    conn.commit()
    conn.close()
    return {"status": "manual watering activated"}

@app.put("/api/devices/{device_id}/threshold")
def update_threshold(device_id: str, data: ThresholdUpdate):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE devices SET moisture_threshold = ? WHERE device_id = ?", (data.moisture_threshold, device_id))
    conn.commit()
    conn.close()
    return {"status": "threshold updated", "new_threshold": data.moisture_threshold}