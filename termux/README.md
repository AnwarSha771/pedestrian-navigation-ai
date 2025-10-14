# Termux Integration - README

Complete Android/Termux deployment for OnePlus 11R (and other Android devices).

## 📁 Files in this Directory

### 1. `setup_termux.sh` (Installation Script)
- Automated installation for Termux environment
- Installs Python, PyTorch, OpenCV, YOLOv8
- Downloads AI model (yolov8n.pt)
- Configures camera access via termux-api
- **Runtime:** 10-15 minutes
- **Usage:** `bash setup_termux.sh`

### 2. `TERMUX_SETUP.md` (Complete Guide)
- Full documentation for Termux deployment
- Step-by-step installation instructions
- Troubleshooting common issues
- Performance tuning for Android
- Battery optimization tips
- **Length:** Comprehensive 500+ line guide

### 3. `QUICKSTART.md` (3-Minute Guide)
- Fast installation path
- Basic commands
- Quick troubleshooting
- **Length:** Brief essential-only guide

### 4. `config_termux.py` (Mobile Configuration)
- Mobile-optimized settings
- Battery saver modes
- Resolution/FPS tuning
- Camera configuration
- Performance settings
- **Lines:** 300+ with helper functions

### 5. `test_camera.sh` (Camera Test)
- Tests termux-camera-photo command
- Verifies camera permissions
- Takes test photo
- **Usage:** `bash test_camera.sh`

## 🚀 Quick Start

1. **Install Apps:**
   - Termux from F-Droid
   - Termux:API from F-Droid

2. **Run Setup:**
   ```bash
   cd ~
   wget https://raw.githubusercontent.com/AnwarSha771/pedestrian-navigation-ai/main/termux/setup_termux.sh
   bash setup_termux.sh
   ```

3. **Get Code:**
   ```bash
   git clone https://github.com/AnwarSha771/pedestrian-navigation-ai.git
   cd pedestrian-navigation-ai
   ```

4. **Test:**
   ```bash
   python termux_main.py --mode single
   ```

## 📱 How It Works

### Architecture
```
Android Device (OnePlus 11R)
    │
    ├── Termux (Linux environment)
    │   ├── Python 3.11
    │   ├── PyTorch (CPU)
    │   └── OpenCV
    │
    ├── Termux:API (System bridge)
    │   └── termux-camera-photo
    │
    └── termux_main.py (Main application)
        ├── Captures frames via termux-api
        ├── Runs YOLOv8 detection
        ├── Custom CV (stairs/potholes)
        ├── Proximity estimation
        └── Saves to ~/storage/pictures/
```

### Data Flow
1. **Capture:** `termux-camera-photo` → temp JPG
2. **Load:** OpenCV reads JPG → NumPy array
3. **Resize:** 320x240 (mobile optimized)
4. **Detect:** YOLOv8 + Custom CV → Detections
5. **Analyze:** Proximity estimation → Threat scores
6. **Output:** Terminal warnings + Saved frames

### Performance (OnePlus 11R)
- **FPS:** 8-10 average
- **Latency:** 100-150ms per frame
- **Battery:** ~20% per hour
- **Resolution:** 320x240 (optimized)
- **Model:** YOLOv8-Nano (6 MB)

## 🔧 Configuration

### Edit Settings
```bash
nano ~/pedestrian-navigation-ai/termux/config_termux.py
```

### Key Settings:
```python
FRAME_WIDTH = 320          # Lower = faster
FRAME_HEIGHT = 240
TARGET_FPS = 10            # Adjust for your device
CONFIDENCE_THRESHOLD = 0.5 # Higher = fewer detections
BATTERY_SAVER_MODE = True  # Auto-adjust on low battery
```

## 📊 Comparison: Desktop vs Termux

| Feature | Desktop (Windows) | Termux (Android) |
|---------|------------------|------------------|
| Resolution | 640x480 | 320x240 |
| FPS | 30+ | 8-10 |
| Camera | OpenCV VideoCapture | termux-camera-photo |
| Audio | pyttsx3 TTS | Disabled |
| Display | GUI window | Saved frames |
| Battery | N/A | 4-5 hours |
| Portability | ❌ | ✅ |
| Setup Time | 5 min | 15 min |

## 🐛 Troubleshooting

### Camera Not Working
```bash
# Check termux-api
termux-camera-info

# Grant permissions
# Android Settings → Apps → Termux:API → Permissions → Camera
```

### Slow Performance
```python
# In config_termux.py:
FRAME_WIDTH = 240
FRAME_HEIGHT = 180
TARGET_FPS = 5
ENABLE_STAIRS = False
ENABLE_POTHOLES = False
```

### Out of Memory
```bash
# Clear cache
pip cache purge

# Close other apps
# Enable Android Performance Mode
```

### Module Not Found
```bash
cd ~/pedestrian-navigation-ai
pip install --upgrade ultralytics opencv-python-headless torch
```

## 📖 Documentation Hierarchy

1. **QUICKSTART.md** - Start here (3 min)
2. **TERMUX_SETUP.md** - Full guide (20 min)
3. **config_termux.py** - Advanced config
4. **../README.md** - Project overview

## 🎯 Use Cases

### 1. Walking Assistant
```bash
python termux_main.py --mode continuous --duration 3600
# Runs for 1 hour, real-time detection
```

### 2. Quick Scan
```bash
python termux_main.py --mode single
# Single photo analysis
```

### 3. Testing/Development
```bash
python termux_main.py --video ~/test.mp4 --duration 30
# Test with video file
```

## 🔋 Battery Life

### Normal Mode
- Resolution: 320x240
- FPS: 10
- All detections enabled
- **Runtime:** ~4-5 hours

### Battery Saver
- Resolution: 240x180
- FPS: 5
- Only YOLO detection
- **Runtime:** ~6-8 hours

### Activate Battery Saver:
```python
# In config_termux.py:
BATTERY_SAVER_MODE = True
LOW_BATTERY_THRESHOLD = 20  # Auto-activate at 20%
```

## 🌐 Remote Access (Optional)

### SSH into Phone
```bash
# On phone:
pkg install openssh
sshd

# On computer:
ssh u0_a123@192.168.1.100 -p 8022
```

### View Photos Remotely
```bash
scp -P 8022 u0_a123@192.168.1.100:~/storage/pictures/*.jpg ./
```

## 🎓 Tips for Best Results

1. **Lighting:** Daylight works best
2. **Stability:** Mount phone at chest level
3. **Angle:** Camera should face forward, slight downward tilt
4. **Battery:** Start with 80%+ charge
5. **Apps:** Close background apps
6. **Storage:** Keep 500 MB free space
7. **Updates:** Keep Termux packages updated

## 🆘 Support

### Check System Status
```bash
cd ~/pedestrian-navigation-ai
python -c "from termux.config_termux import print_config; print_config()"
```

### View Logs
```bash
cat ~/pedestrian-navigation-ai/logs/termux_nav_*.log
```

### Report Issues
- **GitHub:** https://github.com/AnwarSha771/pedestrian-navigation-ai/issues
- **Include:** Phone model, Android version, error logs

## 📈 Roadmap

- [ ] Add haptic feedback via termux-vibrate
- [ ] GPS location logging
- [ ] Cloud sync for detections
- [ ] Voice commands via termux-speech-to-text
- [ ] Background service mode
- [ ] Notification alerts
- [ ] Battery optimization profiles

## 🏆 Why Termux?

✅ **No Root Required** - Works on stock Android  
✅ **Full Python Stack** - PyTorch, OpenCV, YOLOv8  
✅ **Direct Camera Access** - Via termux-api  
✅ **Portable** - Runs entirely on phone  
✅ **Open Source** - Free and customizable  
✅ **Offline** - No internet after setup  
✅ **Hackathon Ready** - Impressive mobile demo!  

---

**Ready to deploy on your OnePlus 11R? Follow QUICKSTART.md! 🚀**
