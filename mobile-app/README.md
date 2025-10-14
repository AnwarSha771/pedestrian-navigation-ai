# 📱 Android Mobile App Integration

## Overview
Complete Android application for collecting sensor data (GPS, accelerometer, gyroscope, magnetometer) and sending to the pedestrian navigation backend server.

---

## 📦 Files Included

```
mobile-app/
├── android/
│   ├── SensorUploadService.kt      # Background service for data collection
│   ├── MainActivity.kt              # Main UI activity
│   ├── AndroidManifest.xml          # Permissions and service declarations
│   ├── build.gradle                 # Dependencies and build config
│   └── activity_main.xml            # UI layout
├── server.py                        # Flask server to receive data
└── README.md                        # This file
```

---

## 🚀 Quick Start

### 1. Set Up Python Backend Server

**Install Flask:**
```powershell
cd C:\pedestrian-navigation-ai\mobile-app
pip install flask
```

**Start the server:**
```powershell
python server.py
```

**Output:**
```
============================================================
🚀 Pedestrian Navigation - Mobile Data Server
============================================================
📊 Database: mobile_data\sensor_data.db
🌐 Starting Flask server on http://0.0.0.0:5000
============================================================

 * Running on http://0.0.0.0:5000
```

**Find your IP address:**
```powershell
ipconfig | Select-String "IPv4"
```
Example: `192.168.1.100`

---

### 2. Set Up Android App

#### Option A: Using Android Studio

1. **Open Android Studio**
2. **Create New Project:**
   - Template: "Empty Activity"
   - Name: "PedestrianNav"
   - Package: `com.pedestriannav.wearable`
   - Language: Kotlin
   - Minimum SDK: 24 (Android 7.0)

3. **Copy Files:**
   - Copy `SensorUploadService.kt` → `app/src/main/java/com/pedestriannav/wearable/`
   - Copy `MainActivity.kt` → `app/src/main/java/com/pedestriannav/wearable/`
   - Copy `AndroidManifest.xml` → `app/src/main/`
   - Copy `build.gradle` content → `app/build.gradle`
   - Copy `activity_main.xml` → `app/src/main/res/layout/`

4. **Sync Gradle** (click "Sync Now" when prompted)

5. **Build & Run:**
   - Connect Android device via USB (enable USB debugging)
   - OR use Android Emulator
   - Click "Run" ▶️

#### Option B: Using APK (Pre-built)

If you have a pre-built APK:
```powershell
# Install via ADB
adb install app-release.apk
```

---

## 📱 Using the App

### First Launch

1. **Grant Permissions:**
   - Location (Fine & Coarse)
   - Background Location
   - Activity Recognition
   - Bluetooth (for wearables)

2. **Configure Server:**
   - Enter server URL: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

3. **Start Service:**
   - Click "Start Service"
   - You'll see a persistent notification: "Pedestrian Navigation Active"

4. **Walk Around:**
   - App collects GPS + sensor data automatically
   - Data sent to server every 5 seconds
   - Works in background

5. **Stop Service:**
   - Click "Stop Service" when done

---

## 🔧 Configuration

### Server Settings

Edit in app or via SharedPreferences:

| Setting | Default | Description |
|---------|---------|-------------|
| `server_url` | `http://192.168.1.100:5000` | Backend server address |
| `batch_size` | `10` | Events per upload batch |
| `sampling_rate` | `SENSOR_DELAY_NORMAL` | Sensor sampling frequency |

### Battery Optimization

The app automatically optimizes for battery life:

**Motion Detection:**
- Only records when movement detected (>0.5 m/s²)
- Skips redundant samples

**Adaptive Sampling:**
- Normal: 50 Hz (50 samples/sec)
- UI: 60 Hz
- Game: 200 Hz (high power)
- Fast: 1000 Hz (very high power)

**Batch Upload:**
- Accumulates 10 events before uploading
- Reduces network overhead

---

## 📊 Data Format

### Data Sent to Server

```json
{
  "events": [
    {
      "lat": 40.7589,
      "lon": -73.9851,
      "altitude": 10.5,
      "speed": 1.2,
      "bearing": 45.0,
      "accuracy": 5.0,
      "ax": 0.12,
      "ay": -0.05,
      "az": 9.81,
      "gx": 0.01,
      "gy": 0.02,
      "gz": 0.01,
      "mx": 25.5,
      "my": -10.2,
      "mz": 45.8,
      "timestamp": 1697291234567,
      "battery": 85,
      "device_id": "abc123-def456"
    }
  ],
  "batch_size": 10,
  "device_type": "android"
}
```

### Server Response

```json
{
  "status": "success",
  "events_received": 10,
  "message": "Data stored successfully"
}
```

---

## 🗄️ Database Schema

**SQLite Database:** `mobile_data/sensor_data.db`

**Table:** `sensor_events`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| device_id | TEXT | Unique device identifier |
| timestamp | BIGINT | Event timestamp (ms) |
| latitude | REAL | GPS latitude |
| longitude | REAL | GPS longitude |
| altitude | REAL | GPS altitude (meters) |
| speed | REAL | Movement speed (m/s) |
| bearing | REAL | Direction (degrees) |
| accuracy | REAL | GPS accuracy (meters) |
| ax, ay, az | REAL | Accelerometer (m/s²) |
| gx, gy, gz | REAL | Gyroscope (rad/s) |
| mx, my, mz | REAL | Magnetometer (μT) |
| battery | INTEGER | Battery level (%) |
| received_at | TEXT | Server receipt time |

---

## 🔌 API Endpoints

### POST /report
**Description:** Upload sensor data batch

**Request:**
```bash
curl -X POST http://localhost:5000/report \
  -H "Content-Type: application/json" \
  -d '{
    "events": [...],
    "batch_size": 10,
    "device_type": "android"
  }'
```

**Response:**
```json
{
  "status": "success",
  "events_received": 10,
  "message": "Data stored successfully"
}
```

### GET /stats
**Description:** Get collection statistics

**Request:**
```bash
curl http://localhost:5000/stats
```

**Response:**
```json
{
  "total_events": 1523,
  "total_devices": 2,
  "last_event_time": "2025-10-14T14:30:22"
}
```

### GET /health
**Description:** Health check

**Response:**
```json
{
  "status": "ok",
  "service": "pedestrian-nav-server"
}
```

---

## 🐛 Troubleshooting

### App Crashes on Start

**Cause:** Missing permissions in manifest  
**Solution:** Verify `AndroidManifest.xml` has all required permissions

### No Data Received on Server

**Cause:** Network connectivity  
**Solution:**
```powershell
# Check server is running
curl http://localhost:5000/health

# Check firewall allows port 5000
netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000

# Test from phone browser
# Open: http://YOUR_IP:5000/health
```

### Location Not Updating

**Cause:** GPS not enabled or permissions denied  
**Solution:**
- Enable Location in phone settings
- Grant "Allow all the time" for background location
- Test outdoors (GPS needs clear sky view)

### High Battery Drain

**Cause:** Too frequent sampling  
**Solution:**
```kotlin
// In SensorUploadService.kt
samplingRate = SensorManager.SENSOR_DELAY_UI  // Change to SENSOR_DELAY_NORMAL
locationUpdateInterval = 5000L  // Change from 1000L to 5000L
```

---

## 🔒 Security Best Practices

### Production Deployment

1. **Use HTTPS:**
   ```python
   # server.py with SSL
   app.run(host='0.0.0.0', port=5000, 
           ssl_context=('cert.pem', 'key.pem'))
   ```

2. **Add Authentication:**
   ```kotlin
   // Add API key header
   request.addHeader("X-API-Key", "your-secret-key")
   ```

3. **Rate Limiting:**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

4. **Data Encryption:**
   - Use TLS 1.2+
   - Encrypt sensitive data at rest

---

## 🚀 Advanced Features

### 1. Real-Time Streaming

Use WebSockets for live data:
```python
from flask_socketio import SocketIO

socketio = SocketIO(app)

@socketio.on('sensor_data')
def handle_sensor_data(data):
    # Process real-time
    socketio.emit('hazard_detected', {'type': 'pothole'})
```

### 2. Offline Mode

App caches data when offline:
```kotlin
// Data saved to: /data/data/com.pedestriannav.wearable/cache/sensor_data/
// Auto-uploads when connection restored
```

### 3. Integration with Wearable System

Combine with `wearable.py`:
```python
# wearable.py can query mobile database
import sqlite3
conn = sqlite3.connect('../mobile-app/mobile_data/sensor_data.db')
# Use GPS data for enhanced hazard detection
```

---

## 📈 Performance Metrics

**Typical Performance:**
- **GPS Update Rate:** 1 Hz (1 sample/sec)
- **Sensor Sample Rate:** 50 Hz (50 samples/sec)
- **Network Upload:** Every 5 seconds (10 events)
- **Battery Impact:** ~5% per hour (moderate)
- **Data Usage:** ~100 KB per hour

---

## 🎯 Next Steps

1. **Test the complete flow:**
   ```powershell
   # Terminal 1: Start server
   python server.py
   
   # Terminal 2: Check stats
   curl http://localhost:5000/stats
   ```

2. **Deploy to phone:**
   - Build APK in Android Studio
   - Install on device
   - Start service
   - Walk around

3. **Integrate with main system:**
   ```python
   # Use collected data in main.py
   python main.py --data-source mobile_db
   ```

4. **Visualize data:**
   ```python
   # Create dashboard with collected GPS tracks
   python visualize_tracks.py
   ```

---

## 📞 Support

**Common Issues:**
- Server not reachable → Check firewall
- High battery drain → Reduce sampling rate
- GPS inaccurate → Use outdoors, wait for GPS lock
- Data not saving → Check database permissions

**Testing Commands:**
```powershell
# View database
sqlite3 mobile_data\sensor_data.db
SELECT COUNT(*) FROM sensor_events;
SELECT * FROM sensor_events ORDER BY id DESC LIMIT 5;

# Monitor server logs
python server.py  # Watch terminal output
```

---

## ✅ Checklist

Before deploying to production:

- [ ] Server running on accessible IP
- [ ] Firewall configured (port 5000)
- [ ] Android app built and installed
- [ ] All permissions granted
- [ ] Server URL configured in app
- [ ] Test upload successful
- [ ] Battery optimization configured
- [ ] Database backup strategy
- [ ] SSL/HTTPS enabled (production)
- [ ] Error monitoring enabled

---

**Your Android integration is ready!** 📱🚀

Start the server and Android app to begin collecting sensor data for your pedestrian navigation system.
