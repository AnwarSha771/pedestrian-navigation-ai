"""
Flask Server for Receiving Android Sensor Data
Integrates with wearable navigation system
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
import sqlite3
import threading
from pathlib import Path

app = Flask(__name__)

# Database setup
DB_PATH = Path("mobile_data") / "sensor_data.db"
DB_PATH.parent.mkdir(exist_ok=True)

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        timestamp BIGINT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        speed REAL,
        bearing REAL,
        accuracy REAL,
        ax REAL,
        ay REAL,
        az REAL,
        gx REAL,
        gy REAL,
        gz REAL,
        mx REAL,
        my REAL,
        mz REAL,
        battery INTEGER,
        received_at TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/report', methods=['POST'])
def report_sensor_data():
    """Receive sensor data from Android app"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Handle batch upload
        if 'events' in data:
            events = data['events']
            batch_size = data.get('batch_size', len(events))
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for event in events:
                cursor.execute('''
                INSERT INTO sensor_events (
                    device_id, timestamp, latitude, longitude, altitude,
                    speed, bearing, accuracy, ax, ay, az, gx, gy, gz,
                    mx, my, mz, battery, received_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event.get('device_id'),
                    event.get('timestamp'),
                    event.get('lat'),
                    event.get('lon'),
                    event.get('altitude'),
                    event.get('speed'),
                    event.get('bearing'),
                    event.get('accuracy'),
                    event.get('ax'),
                    event.get('ay'),
                    event.get('az'),
                    event.get('gx'),
                    event.get('gy'),
                    event.get('gz'),
                    event.get('mx'),
                    event.get('my'),
                    event.get('mz'),
                    event.get('battery'),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
            print(f"✓ Received batch of {batch_size} events from {data.get('device_type', 'unknown')}")
            
            return jsonify({
                "status": "success",
                "events_received": batch_size,
                "message": "Data stored successfully"
            }), 200
        
        # Handle single event
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO sensor_events (
                device_id, timestamp, latitude, longitude, altitude,
                speed, bearing, accuracy, ax, ay, az, gx, gy, gz,
                mx, my, mz, battery, received_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('device_id'),
                data.get('timestamp'),
                data.get('lat'),
                data.get('lon'),
                data.get('altitude'),
                data.get('speed'),
                data.get('bearing'),
                data.get('accuracy'),
                data.get('ax'),
                data.get('ay'),
                data.get('az'),
                data.get('gx'),
                data.get('gy'),
                data.get('gz'),
                data.get('mx'),
                data.get('my'),
                data.get('mz'),
                data.get('battery'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✓ Received event from device {data.get('device_id', 'unknown')}")
            
            return jsonify({
                "status": "success",
                "message": "Event stored successfully"
            }), 200
    
    except Exception as e:
        print(f"✗ Error processing sensor data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about collected data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM sensor_events')
        total_events = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT device_id) FROM sensor_events')
        total_devices = cursor.fetchone()[0]
        
        cursor.execute('SELECT received_at FROM sensor_events ORDER BY id DESC LIMIT 1')
        last_event = cursor.fetchone()
        last_event_time = last_event[0] if last_event else None
        
        conn.close()
        
        return jsonify({
            "total_events": total_events,
            "total_devices": total_devices,
            "last_event_time": last_event_time
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "pedestrian-nav-server"}), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Pedestrian Navigation - Mobile Data Server")
    print("="*60)
    print(f"📊 Database: {DB_PATH}")
    print("🌐 Starting Flask server on http://0.0.0.0:5000")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
