import sqlite3
from datetime import datetime

DB_NAME = "plant_care.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Devices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        device_id TEXT PRIMARY KEY,
        plant_name TEXT,
        moisture_threshold REAL DEFAULT 30.0,
        pump_status INTEGER DEFAULT 0,
        last_seen TEXT
    )
    """)
    
    # Readings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        soil_moisture REAL,
        temperature REAL,
        humidity REAL,
        light_level REAL,
        timestamp TEXT
    )
    """)
    
    # Watering history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watering_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        trigger_type TEXT,
        moisture_level REAL,
        timestamp TEXT
    )
    """)
    
    # Seed initial device
    cursor.execute("""
    INSERT OR IGNORE INTO devices (device_id, plant_name, moisture_threshold, pump_status, last_seen)
    VALUES ('PLANT-001', 'Indoor Tomato', 30.0, 0, ?)
    """, (datetime.utcnow().isoformat(),))
    
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)