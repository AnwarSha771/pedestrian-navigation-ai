# 📱 Mobile Deployment - Complete Code Package

**All commands and code to deploy on your OnePlus 11R**

---

## 🎯 Quick Deploy (Copy-Paste Ready)

### **Phase 1: Install Termux Apps**

#### Step 1: Download & Install F-Droid
```
Open browser → https://f-droid.org/
Download F-Droid.apk
Install APK (allow unknown sources)
```

#### Step 2: Install Termux from F-Droid
```
Open F-Droid app
Search: "Termux"
Install: com.termux (main app)
```

#### Step 3: Install Termux:API
```
In F-Droid
Search: "Termux:API"
Install: com.termux.api
```

---

### **Phase 2: Termux Setup Commands**

Open Termux app and paste these commands one by one:

#### Command 1: Grant Storage Access
```bash
termux-setup-storage
```
**Action:** Tap "Allow" when popup appears

---

#### Command 2: Update Packages
```bash
pkg update -y && pkg upgrade -y
```
**Wait:** 2-3 minutes

---

#### Command 3: Install Essential Tools
```bash
pkg install wget git python -y
```
**Wait:** 1-2 minutes

---

#### Command 4: Download Setup Script
```bash
cd ~
wget https://raw.githubusercontent.com/AnwarSha771/pedestrian-navigation-ai/main/termux/setup_termux.sh
```

---

#### Command 5: Run Automated Setup
```bash
bash setup_termux.sh
```
**Wait:** 15-20 minutes ☕  
**This installs:** Python packages, PyTorch, OpenCV, YOLOv8

---

### **Phase 3: Get Project Code**

#### Command 6: Clone Repository
```bash
cd ~
git clone https://github.com/AnwarSha771/pedestrian-navigation-ai.git
```

---

#### Command 7: Enter Project Directory
```bash
cd pedestrian-navigation-ai
```

---

#### Command 8: Verify Files
```bash
ls -la
```

**You should see:**
- termux_main.py
- termux/ folder
- src/ folder
- config.py
- yolov8n.pt (AI model)

---

### **Phase 4: Test Camera**

#### Command 9: Test Camera Access
```bash
bash termux/test_camera.sh
```

**Expected output:**
```
✅ Camera works!
Photo saved as test_photo.jpg
```

**If fails:** Go to Android Settings → Apps → Termux:API → Permissions → Camera → Allow

---

### **Phase 5: Run Detection**

#### Command 10: Single Photo Test
```bash
python termux_main.py --mode single
```

**Expected output:**
```
📱 TERMUX PEDESTRIAN NAVIGATION SYSTEM
🔧 Initializing AI components...
✅ System initialized!
📸 Taking single photo...
⚠️  [PERSON] near - right (threat: 70/100)
💾 Saved: ~/storage/pictures/detection_152034.jpg
```

---

#### Command 11: Continuous Detection (1 minute)
```bash
python termux_main.py --mode continuous --duration 60
```

**What happens:**
- Takes photos every 0.1 seconds
- Detects hazards in real-time
- Saves frames every 5 seconds
- Prints warnings to terminal

**To stop:** Press Ctrl + C (or Volume Down + C)

---

#### Command 12: Long Session (1 hour)
```bash
python termux_main.py --mode continuous --duration 3600
```

---

### **Phase 6: View Results**

#### Command 13: List Saved Photos
```bash
ls -lh ~/storage/pictures/detection_*.jpg
ls -lh ~/storage/pictures/nav_*.jpg
```

#### Command 14: Open in Gallery
```bash
termux-open ~/storage/pictures/
```
Or just open your **Gallery app** and look for `detection_*.jpg`

---

## 🎮 All Available Commands

### Detection Modes

#### Single Shot (Quick Scan)
```bash
python termux_main.py --mode single
```

#### Continuous 30 seconds (Test)
```bash
python termux_main.py --mode continuous --duration 30
```

#### Continuous 5 minutes (Short Walk)
```bash
python termux_main.py --mode continuous --duration 300
```

#### Continuous 1 hour (Real Navigation)
```bash
python termux_main.py --mode continuous --duration 3600
```

#### Test with Video File (No Camera)
```bash
python termux_main.py --video ~/storage/downloads/test.mp4 --duration 30
```

---

### System Commands

#### Check Configuration
```bash
python termux/config_termux.py
```

#### View Logs
```bash
cat ~/pedestrian-navigation-ai/logs/termux_nav_*.log
```

#### Check Battery Status
```bash
termux-battery-status
```

#### Check Storage
```bash
df -h ~/storage/pictures
```

#### List Installed Packages
```bash
pip list | grep -E "torch|opencv|ultralytics"
```

#### Check Camera Info
```bash
termux-camera-info
```

#### Take Manual Photo
```bash
termux-camera-photo -c 0 test.jpg
```

---

### Maintenance Commands

#### Update Project from GitHub
```bash
cd ~/pedestrian-navigation-ai
git pull origin main
```

#### Reinstall Dependencies
```bash
pip install --upgrade ultralytics opencv-python-headless torch torchvision
```

#### Clear Cache (Free Space)
```bash
pip cache purge
```

#### Delete Old Photos
```bash
rm ~/storage/pictures/detection_*.jpg
rm ~/storage/pictures/nav_*.jpg
```

#### Clean Temp Files
```bash
rm -rf /data/data/com.termux/files/usr/tmp/termux_nav/*
```

---

## ⚙️ Configuration Code

### Basic Configuration File

Create: `~/pedestrian-navigation-ai/my_config.py`

```python
"""Custom configuration for your OnePlus 11R"""

# Resolution (lower = faster, higher = better quality)
FRAME_WIDTH = 320   # Options: 160, 240, 320, 416
FRAME_HEIGHT = 240  # Options: 120, 180, 240, 320

# Frame rate (lower = saves battery)
TARGET_FPS = 10     # Options: 5, 8, 10, 15

# Detection confidence (higher = fewer false positives)
CONFIDENCE_THRESHOLD = 0.5  # Range: 0.3 to 0.7

# Auto-save interval (seconds)
SAVE_INTERVAL = 5   # How often to save frames

# Battery saver (auto-reduces quality when low battery)
BATTERY_SAVER_MODE = True
LOW_BATTERY_THRESHOLD = 20  # Activate at 20% battery

# Enable/disable detection types
ENABLE_YOLO = True          # Main object detection
ENABLE_STAIRS = True        # Stairs detection (custom CV)
ENABLE_POTHOLES = True      # Pothole detection (custom CV)
ENABLE_SIDEWALK = False     # Sidewalk detection (slow on mobile)

# Camera settings
CAMERA_ID = 0  # 0 = back camera, 1 = front camera
```

---

### Performance Profiles

#### High Performance (Fast phone, good battery)
```python
FRAME_WIDTH = 416
FRAME_HEIGHT = 416
TARGET_FPS = 15
ENABLE_ALL = True
```

#### Balanced (Default - Recommended)
```python
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
TARGET_FPS = 10
ENABLE_YOLO = True
ENABLE_STAIRS = True
ENABLE_POTHOLES = True
```

#### Battery Saver (Low power, longer runtime)
```python
FRAME_WIDTH = 240
FRAME_HEIGHT = 180
TARGET_FPS = 5
ENABLE_YOLO = True
ENABLE_STAIRS = False
ENABLE_POTHOLES = False
```

#### Ultra Low Power (8+ hour runtime)
```python
FRAME_WIDTH = 160
FRAME_HEIGHT = 120
TARGET_FPS = 3
ENABLE_YOLO = True  # Only YOLO, no custom CV
ENABLE_STAIRS = False
ENABLE_POTHOLES = False
FRAME_SKIP = 2  # Process every 3rd frame
```

---

## 🔧 Custom Scripts

### Script 1: Quick Start Script

Create: `~/pedestrian-navigation-ai/quick_start.sh`

```bash
#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Quick Start - Pedestrian Navigation"
echo ""

# Test camera
echo "1. Testing camera..."
termux-camera-photo -c 0 test.jpg 2>/dev/null
if [ -f "test.jpg" ]; then
    echo "✅ Camera OK"
    rm test.jpg
else
    echo "❌ Camera failed - check permissions"
    exit 1
fi

# Check battery
echo ""
echo "2. Checking battery..."
battery=$(termux-battery-status | grep -oP '"percentage":\s*\K\d+')
echo "🔋 Battery: ${battery}%"

if [ $battery -lt 30 ]; then
    echo "⚠️  Low battery! Recommend charging first."
    echo "Continue anyway? (y/n)"
    read answer
    if [ "$answer" != "y" ]; then
        exit 0
    fi
fi

# Start detection
echo ""
echo "3. Starting detection..."
echo "Mode: Continuous, Duration: 5 minutes"
echo ""
cd ~/pedestrian-navigation-ai
python termux_main.py --mode continuous --duration 300

echo ""
echo "✅ Session complete!"
echo "View photos in Gallery app"
```

**Make executable:**
```bash
chmod +x ~/pedestrian-navigation-ai/quick_start.sh
```

**Run:**
```bash
bash ~/pedestrian-navigation-ai/quick_start.sh
```

---

### Script 2: Battery Monitor

Create: `~/pedestrian-navigation-ai/battery_monitor.sh`

```bash
#!/data/data/com.termux/files/usr/bin/bash

echo "🔋 Battery Monitor"
echo ""

while true; do
    battery=$(termux-battery-status | grep -oP '"percentage":\s*\K\d+')
    status=$(termux-battery-status | grep -oP '"status":\s*"\K[^"]+')
    temp=$(termux-battery-status | grep -oP '"temperature":\s*\K[\d.]+')
    
    echo "$(date +%H:%M:%S) | Battery: ${battery}% | Status: ${status} | Temp: ${temp}°C"
    
    if [ $battery -lt 15 ]; then
        termux-notification --title "Low Battery" --content "Only ${battery}% remaining!"
    fi
    
    sleep 60  # Check every minute
done
```

**Run in background:**
```bash
bash ~/pedestrian-navigation-ai/battery_monitor.sh &
```

---

### Script 3: Auto-Upload to Server (Optional)

Create: `~/pedestrian-navigation-ai/auto_upload.py`

```python
"""Auto-upload detections to your server"""
import os
import time
import requests
from pathlib import Path

SERVER_URL = "http://your-server.com/api/upload"  # Change this
API_KEY = "your-api-key"  # Change this
UPLOAD_DIR = Path.home() / "storage" / "pictures"
CHECK_INTERVAL = 60  # seconds

def upload_file(filepath):
    """Upload single file to server"""
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Bearer {API_KEY}'}
            response = requests.post(SERVER_URL, files=files, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Uploaded: {filepath.name}")
                return True
            else:
                print(f"❌ Upload failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main upload loop"""
    print("📡 Auto-Upload Service Started")
    print(f"Watching: {UPLOAD_DIR}")
    print(f"Server: {SERVER_URL}")
    print("")
    
    uploaded_files = set()
    
    while True:
        # Find detection images
        detection_files = list(UPLOAD_DIR.glob("detection_*.jpg"))
        nav_files = list(UPLOAD_DIR.glob("nav_*.jpg"))
        all_files = detection_files + nav_files
        
        # Upload new files
        for filepath in all_files:
            if filepath not in uploaded_files:
                if upload_file(filepath):
                    uploaded_files.add(filepath)
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
```

**Install requirements:**
```bash
pip install requests
```

**Run:**
```bash
python ~/pedestrian-navigation-ai/auto_upload.py &
```

---

## 📊 Real-World Usage Examples

### Example 1: Morning Commute (20 minutes)

```bash
# Navigate to project
cd ~/pedestrian-navigation-ai

# Start detection
python termux_main.py --mode continuous --duration 1200

# Put phone in chest pocket (camera facing out)
# Walk normally
# Check terminal occasionally for warnings
# System auto-saves frames every 5 seconds

# After arriving, check results:
ls -lh ~/storage/pictures/nav_*.jpg
```

---

### Example 2: Indoor Navigation Test (2 minutes)

```bash
cd ~/pedestrian-navigation-ai

# Quick 2-minute test
python termux_main.py --mode continuous --duration 120

# Walk around your room/house
# Check what it detects (furniture, doors, people)
```

---

### Example 3: Outdoor Safety Check

```bash
cd ~/pedestrian-navigation-ai

# Take single shots at different locations
python termux_main.py --mode single
# Walk 10 meters
python termux_main.py --mode single
# Walk to crossing
python termux_main.py --mode single

# Review all photos in Gallery
```

---

### Example 4: Full Day Navigation

```bash
# Morning: Check battery
termux-battery-status

# Start long session (4 hours = 14400 seconds)
cd ~/pedestrian-navigation-ai
python termux_main.py --mode continuous --duration 14400

# Enable wake lock (prevent sleep)
termux-wake-lock

# Go about your day
# Phone continuously monitors environment

# Evening: Stop and review
# Press Ctrl+C
termux-wake-unlock

# Count detections
ls ~/storage/pictures/nav_*.jpg | wc -l
```

---

## 🐛 Troubleshooting Code

### Check System Health

Create: `~/pedestrian-navigation-ai/check_health.py`

```python
"""System health checker"""
import subprocess
import sys
from pathlib import Path

def check_python():
    """Check Python version"""
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version OK")
        return True
    else:
        print("❌ Python too old (need 3.8+)")
        return False

def check_packages():
    """Check required packages"""
    required = ['torch', 'cv2', 'ultralytics', 'numpy', 'PIL']
    all_ok = True
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ {pkg} installed")
        except ImportError:
            print(f"❌ {pkg} missing")
            all_ok = False
    
    return all_ok

def check_camera():
    """Check camera access"""
    try:
        result = subprocess.run(
            ['termux-camera-info'],
            capture_output=True,
            timeout=3
        )
        if result.returncode == 0:
            print("✅ Camera access OK")
            return True
        else:
            print("❌ Camera access failed")
            return False
    except:
        print("❌ Termux:API not installed")
        return False

def check_storage():
    """Check storage space"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(Path.home())
        free_gb = free / (1024**3)
        print(f"💾 Free space: {free_gb:.1f} GB")
        if free_gb > 1:
            print("✅ Storage OK")
            return True
        else:
            print("⚠️  Low storage")
            return False
    except:
        return False

def check_model():
    """Check AI model"""
    model_path = Path.home() / "pedestrian-navigation-ai" / "yolov8n.pt"
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024**2)
        print(f"📦 Model: {size_mb:.1f} MB")
        print("✅ Model file OK")
        return True
    else:
        print("❌ Model file missing")
        return False

def main():
    print("🔍 System Health Check")
    print("="*50)
    
    checks = [
        ("Python", check_python),
        ("Packages", check_packages),
        ("Camera", check_camera),
        ("Storage", check_storage),
        ("Model", check_model),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed!")
        print("System ready to run.")
    else:
        print("❌ Some checks failed")
        print("Review errors above and fix issues.")

if __name__ == "__main__":
    main()
```

**Run:**
```bash
cd ~/pedestrian-navigation-ai
python check_health.py
```

---

## 📱 Complete Deployment Checklist

### Pre-Deployment ✓

- [ ] OnePlus 11R charged to 80%+
- [ ] 2 GB free storage available
- [ ] WiFi connected
- [ ] F-Droid installed
- [ ] Termux installed from F-Droid
- [ ] Termux:API installed from F-Droid

### Installation ✓

- [ ] Run: `termux-setup-storage`
- [ ] Run: `pkg update && pkg upgrade`
- [ ] Run: `bash setup_termux.sh`
- [ ] Wait 15-20 minutes
- [ ] Clone repository
- [ ] Test camera: `bash termux/test_camera.sh`

### Testing ✓

- [ ] Single shot works: `python termux_main.py --mode single`
- [ ] Photo saved to Gallery
- [ ] Detections visible in photo
- [ ] Terminal warnings show up
- [ ] Continuous mode runs: `--mode continuous --duration 30`

### Production Ready ✓

- [ ] Tested in safe indoor area
- [ ] Tested outdoors
- [ ] Battery life acceptable
- [ ] FPS > 5
- [ ] Photos auto-saving
- [ ] Comfortable mounting position found

---

## 🎯 Quick Reference Card

**Print this or save as screenshot:**

```
╔════════════════════════════════════════════╗
║  PEDESTRIAN NAVIGATION - QUICK COMMANDS   ║
╠════════════════════════════════════════════╣
║                                            ║
║  📍 Navigate to project:                   ║
║     cd ~/pedestrian-navigation-ai          ║
║                                            ║
║  📸 Single photo:                          ║
║     python termux_main.py --mode single    ║
║                                            ║
║  🎥 5 minutes continuous:                  ║
║     python termux_main.py --mode \         ║
║       continuous --duration 300            ║
║                                            ║
║  🛑 Stop detection:                        ║
║     Ctrl + C (Volume Down + C)             ║
║                                            ║
║  🔍 Test camera:                           ║
║     bash termux/test_camera.sh             ║
║                                            ║
║  🔋 Check battery:                         ║
║     termux-battery-status                  ║
║                                            ║
║  📊 View photos:                           ║
║     Open Gallery app                       ║
║     Or: termux-open ~/storage/pictures/    ║
║                                            ║
║  📝 Check logs:                            ║
║     cat logs/termux_nav_*.log              ║
║                                            ║
║  🔧 Health check:                          ║
║     python check_health.py                 ║
║                                            ║
╚════════════════════════════════════════════╝
```

---

## 🆘 Emergency Commands

### If Stuck in Loop
```bash
Ctrl + C  # or Volume Down + C
```

### If Termux Frozen
```bash
# Exit Termux
# Android Settings → Apps → Termux → Force Stop
# Reopen Termux
```

### If Out of Space
```bash
rm ~/storage/pictures/nav_*.jpg  # Delete old photos
pip cache purge                   # Clear pip cache
```

### If Camera Not Working
```bash
# 1. Check permissions
# Android Settings → Apps → Termux:API → Permissions → Camera → Allow

# 2. Test manually
termux-camera-photo test.jpg

# 3. Restart Termux
```

### If Too Slow
```bash
# Edit config
nano termux/config_termux.py
# Change: FRAME_WIDTH = 240, TARGET_FPS = 5

# Or use battery saver mode
# It auto-activates at 20% battery
```

---

## 📞 Support & Help

**Documentation:**
- Main README: `cat ~/pedestrian-navigation-ai/README.md`
- Termux Setup: `cat ~/pedestrian-navigation-ai/termux/TERMUX_SETUP.md`
- Quick Start: `cat ~/pedestrian-navigation-ai/termux/QUICKSTART.md`
- OnePlus Guide: `cat ~/pedestrian-navigation-ai/ONEPLUS_11R_GUIDE.md`

**GitHub:**
- Repository: https://github.com/AnwarSha771/pedestrian-navigation-ai
- Issues: https://github.com/AnwarSha771/pedestrian-navigation-ai/issues

**Logs Location:**
```bash
~/pedestrian-navigation-ai/logs/
```

---

**You now have everything needed to deploy on your OnePlus 11R! 🚀📱**

**Start with Phase 1 and follow the commands in order. Good luck! 🏆**
