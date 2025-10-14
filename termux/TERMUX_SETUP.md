# 📱 Termux Setup Guide - OnePlus 11R

Complete guide to run Pedestrian Navigation AI directly on your OnePlus 11R using Termux.

---

## 🎯 Overview

This setup allows you to run the AI navigation system **directly on your phone** without needing a computer. The camera opens on your mobile device, and all processing happens locally.

**Tested on:** OnePlus 11R  
**OS Required:** Android 7.0+  
**Storage Needed:** ~2 GB  
**Time to Setup:** 15-20 minutes

---

## 📦 Step 1: Install Required Apps

### 1.1 Install Termux
- **Source:** F-Droid (NOT Google Play Store - it's outdated!)
- **Link:** https://f-droid.org/en/packages/com.termux/
- **Download:** `termux_0.118.0+github-debug_arm64-v8a.apk`

### 1.2 Install Termux:API
- **Source:** F-Droid
- **Link:** https://f-droid.org/en/packages/com.termux.api/
- **Download:** `termux-api_0.50+github-debug_universal.apk`

**Important:** Both apps MUST be from F-Droid, not Play Store!

---

## 🔧 Step 2: Initial Termux Setup

### 2.1 Grant Storage Permission
Open Termux and run:
```bash
termux-setup-storage
```
- Tap "Allow" when prompted
- This lets Termux access your photos/videos

### 2.2 Update Packages
```bash
pkg update -y && pkg upgrade -y
```
- Takes 2-3 minutes
- Downloads ~100 MB

---

## 🚀 Step 3: Automated Installation

### 3.1 Download Setup Script
```bash
cd ~
wget https://raw.githubusercontent.com/AnwarSha771/pedestrian-navigation-ai/main/termux/setup_termux.sh
```

### 3.2 Run Setup
```bash
bash setup_termux.sh
```

**What it does:**
- ✅ Installs Python 3.11
- ✅ Installs OpenCV, PyTorch, YOLOv8
- ✅ Downloads AI model (6 MB)
- ✅ Configures camera access
- ✅ Creates test scripts

**Time:** 10-15 minutes  
**Download:** ~800 MB

---

## 📥 Step 4: Get Project Code

### 4.1 Clone Repository
```bash
cd ~
git clone https://github.com/AnwarSha771/pedestrian-navigation-ai.git
cd pedestrian-navigation-ai
```

### 4.2 Verify Files
```bash
ls -la
```
You should see:
- `termux_main.py` ← Main Termux app
- `src/` ← AI modules
- `config.py` ← Settings
- `yolov8n.pt` ← AI model

---

## 📷 Step 5: Test Camera

### 5.1 Test Camera Access
```bash
cd ~/pedestrian-navigation-ai
bash termux/test_camera.sh
```

**Expected:**
```
Testing camera access...
✅ Camera works! Photo saved as test_photo.jpg
```

**Troubleshooting:**
- ❌ "Permission denied" → Run `termux-setup-storage` again
- ❌ "Command not found" → Install Termux:API app
- ❌ "Camera timeout" → Check camera permissions in Android settings

---

## 🏃 Step 6: Run Navigation System

### 6.1 Single Photo Mode (Test)
```bash
python termux_main.py --mode single
```

**What happens:**
1. Camera takes 1 photo
2. AI detects hazards (people, potholes, stairs)
3. Saves result to: `~/storage/pictures/detection_XXXXXX.jpg`

**Output example:**
```
📸 Taking single photo...
✅ Photo captured, processing...
⚠️  [POTHOLE] immediate - center (threat: 95/100)
💾 Saved: /storage/emulated/0/Pictures/detection_152034.jpg
```

### 6.2 Continuous Mode (Real Navigation)
```bash
python termux_main.py --mode continuous --duration 60
```

**What happens:**
1. Captures photos every 0.1 seconds (10 FPS)
2. Detects hazards in real-time
3. Prints warnings to terminal
4. Saves frames every 5 seconds
5. Runs for 60 seconds (or Ctrl+C to stop)

**Output example:**
```
⚡ Starting detection loop (60 seconds)...
⚠️  [PERSON] near - right (threat: 70/100)
⚠️  [STAIRS] immediate - center (threat: 87/100)
💾 Saved: nav_152145.jpg
⚠️  [POTHOLE] immediate - left (threat: 92/100)
💾 Saved: nav_152150.jpg
```

---

## 🎮 Usage Examples

### Example 1: Walking Assistant (5 minutes)
```bash
python termux_main.py --mode continuous --duration 300
```
- Runs for 5 minutes
- Detects obstacles while walking
- Saves photos every 5 seconds

### Example 2: Quick Scan (Single Shot)
```bash
python termux_main.py --mode single
```
- Takes 1 photo
- Analyzes hazards
- Quick check before crossing

### Example 3: Test with Video File
```bash
# First, download test video to ~/storage/downloads/test.mp4
python termux_main.py --video ~/storage/downloads/test.mp4 --duration 30
```
- Tests system without using camera
- Good for development

---

## 📊 Performance on OnePlus 11R

**Specs:**
- CPU: Snapdragon 8+ Gen 1
- RAM: 8/16 GB
- Resolution: 320x240 (optimized for mobile)
- Target FPS: 10

**Expected Performance:**
- Detection Speed: ~8-10 FPS
- Battery Usage: ~20% per hour
- Accuracy: Same as desktop version
- Latency: 100-150ms per frame

---

## 🔋 Battery Optimization Tips

### 1. Lower Resolution
Edit `termux_main.py`:
```python
self.frame_width = 240   # Lower from 320
self.frame_height = 180  # Lower from 240
```

### 2. Reduce FPS
```python
self.target_fps = 5  # Lower from 10
```

### 3. Use Power Saver Mode
```bash
# In Android settings:
Settings → Battery → Power Saving Mode → ON
```

### 4. Wake Lock (Keep Running)
```bash
termux-wake-lock
python termux_main.py --mode continuous --duration 3600
termux-wake-unlock
```

---

## 📂 File Locations

### Project Files
```
~/pedestrian-navigation-ai/
├── termux_main.py          ← Main app
├── src/                     ← AI modules
│   ├── detector.py
│   ├── proximity.py
│   └── utils.py
├── config.py                ← Settings
├── yolov8n.pt              ← AI model
└── termux/
    ├── setup_termux.sh      ← Install script
    └── TERMUX_SETUP.md      ← This guide
```

### Output Photos
```
~/storage/pictures/
├── detection_152034.jpg    ← Single shots
├── nav_152145.jpg          ← Continuous frames
└── nav_152150.jpg
```

### Logs
```
~/pedestrian-navigation-ai/logs/
└── termux_nav_YYYYMMDD.log
```

---

## 🐛 Troubleshooting

### Problem: "Module not found"
**Solution:**
```bash
cd ~/pedestrian-navigation-ai
python -c "import src.detector; print('✅ Modules OK')"
```
If fails: `pip install --upgrade ultralytics opencv-python-headless`

### Problem: Camera permission denied
**Solution:**
1. Android Settings → Apps → Termux:API → Permissions → Camera → Allow
2. Run: `termux-camera-info` (should show camera details)

### Problem: Out of memory
**Solution:**
```bash
# Clear cache
pip cache purge

# Lower resolution in termux_main.py
self.frame_width = 160
self.frame_height = 120
```

### Problem: Too slow (< 5 FPS)
**Solution:**
1. Close background apps
2. Enable Performance Mode in Android
3. Lower resolution (see above)
4. Disable other Termux sessions

### Problem: Audio warnings not working
**Note:** Audio is intentionally disabled in Termux (no TTS support). Use visual warnings only.

---

## 🔬 Advanced Configuration

### Custom Settings
Create `config_termux.py`:
```python
# Mobile-optimized settings
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
TARGET_FPS = 10
CONFIDENCE_THRESHOLD = 0.5
SAVE_INTERVAL = 5  # Save frame every N seconds

# Detection settings
ENABLE_YOLO = True
ENABLE_STAIRS = True
ENABLE_POTHOLES = True
ENABLE_SIDEWALK = False  # Too slow for mobile

# Proximity settings
IMMEDIATE_THRESHOLD = 0.7
NEAR_THRESHOLD = 0.4
```

### Run with Custom Config
```python
# In termux_main.py, add at top:
import config_termux as config
```

---

## 🌐 Remote Access (Optional)

### Access from Computer
```bash
# On phone (Termux):
pkg install openssh
sshd

# Get phone IP:
ifconfig wlan0

# On computer:
ssh u0_a123@192.168.1.100 -p 8022
```

### View Output Remotely
```bash
# On phone:
python termux_main.py --mode continuous --duration 3600

# On computer (view photos):
scp -P 8022 u0_a123@192.168.1.100:~/storage/pictures/nav_*.jpg ./
```

---

## 📈 Next Steps

1. ✅ **Test single shot mode** - Verify camera works
2. ✅ **Run 1-minute continuous** - Check performance
3. ✅ **Walk outside** - Real-world testing
4. ✅ **Adjust settings** - Optimize for your needs
5. ✅ **Battery test** - See how long it lasts

---

## 🆘 Support

### Check Logs
```bash
cd ~/pedestrian-navigation-ai
cat logs/termux_nav_*.log
```

### System Info
```bash
# Python version
python --version

# Installed packages
pip list | grep -E "torch|opencv|ultralytics"

# Termux info
termux-info
```

### Report Issues
- GitHub: https://github.com/AnwarSha771/pedestrian-navigation-ai/issues
- Include: Phone model, Android version, error message, logs

---

## 🎓 Tips for Best Results

1. **Hold Phone Stable:** Shaky camera = poor detection
2. **Good Lighting:** Works best in daylight
3. **Clear View:** Don't cover camera lens
4. **Chest Level:** Mount at chest height for best angle
5. **Battery:** Start with 80%+ charge
6. **Storage:** Keep 500 MB free space

---

## 🏆 Hackathon Demo Mode

### Quick Demo (30 seconds)
```bash
# Show live detection
python termux_main.py --mode continuous --duration 30

# Then show saved photos
ls -lh ~/storage/pictures/nav_*.jpg
```

### Impressive Stats
- ✅ Runs on phone (no computer needed!)
- ✅ 10 FPS real-time detection
- ✅ Detects 80+ object classes
- ✅ Custom pothole/stairs detection
- ✅ Battery-optimized algorithms
- ✅ Offline capable (no internet needed)

---

**Ready to revolutionize pedestrian safety? Let's go! 🚀**
