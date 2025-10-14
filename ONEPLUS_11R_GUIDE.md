# 📱 OnePlus 11R Deployment Guide

**Complete guide to run Pedestrian Navigation AI on your OnePlus 11R**

---

## 🎯 What You'll Get

✅ Run AI navigation **directly on your phone**  
✅ Use OnePlus 11R camera for real-time detection  
✅ No computer needed after setup  
✅ Works offline (no internet required)  
✅ 8-10 FPS detection speed  
✅ 4-5 hour battery life  

---

## 📋 What You Need

### Hardware
- ✅ OnePlus 11R (your phone)
- ✅ 2+ GB free storage
- ✅ Battery charged to 80%+
- ✅ WiFi (for initial download only)

### Software (will install)
- Termux (Linux on Android)
- Termux:API (camera access)
- Python 3.11
- PyTorch (AI framework)
- YOLOv8 (detection model)

---

## 🚀 Step-by-Step Installation

### Step 1: Install Termux Apps (5 minutes)

#### 1.1 Download F-Droid Store
- Open browser on phone
- Go to: **https://f-droid.org/**
- Download F-Droid APK
- Install (allow "Unknown sources" if asked)

#### 1.2 Install Termux
- Open F-Droid app
- Search: "Termux"
- Install **com.termux** (main app)
- Wait for download (~50 MB)

#### 1.3 Install Termux:API
- In F-Droid, search: "Termux:API"
- Install **com.termux.api**
- Wait for download (~5 MB)

**⚠️ Important:** Both MUST be from F-Droid, not Google Play Store!

---

### Step 2: Setup Termux (15 minutes)

#### 2.1 Open Termux
- Launch Termux app
- You'll see a black terminal screen
- Wait for prompt: `$`

#### 2.2 Grant Storage Access
Type this command and press Enter:
```bash
termux-setup-storage
```
- A permission popup appears
- Tap **"Allow"**
- This lets Termux save photos to your gallery

#### 2.3 Update Packages
Copy and paste this command:
```bash
pkg update -y && pkg upgrade -y
```
- Takes 2-3 minutes
- Downloads ~100 MB
- Press "Y" if asked anything

#### 2.4 Download Setup Script
```bash
cd ~
pkg install wget -y
wget https://raw.githubusercontent.com/AnwarSha771/pedestrian-navigation-ai/main/termux/setup_termux.sh
```

#### 2.5 Run Automated Setup
```bash
bash setup_termux.sh
```

**What happens now:**
- Installs Python 3.11 (3 min)
- Installs NumPy, OpenCV (5 min)
- Installs PyTorch (CPU version) (5 min)
- Installs YOLOv8 (2 min)
- Downloads AI model - 6 MB (1 min)
- **Total time: 15-20 minutes**

☕ **Take a break!** This is the longest part.

---

### Step 3: Get Project Code (2 minutes)

#### 3.1 Clone Repository
```bash
cd ~
pkg install git -y
git clone https://github.com/AnwarSha771/pedestrian-navigation-ai.git
cd pedestrian-navigation-ai
```

#### 3.2 Verify Files
```bash
ls -la
```

You should see:
- ✅ `termux_main.py` (main app)
- ✅ `termux/` folder (configs)
- ✅ `src/` folder (AI modules)
- ✅ `yolov8n.pt` (AI model)

---

### Step 4: Test Camera (1 minute)

#### 4.1 Run Camera Test
```bash
bash termux/test_camera.sh
```

**If successful:**
```
✅ Camera works!
Photo saved as test_photo.jpg
```

**If failed:**
1. Open Android Settings
2. Apps → Termux:API → Permissions
3. Enable **Camera** permission
4. Try again

---

### Step 5: First Detection! (2 minutes)

#### 5.1 Single Photo Test
```bash
python termux_main.py --mode single
```

**What happens:**
1. Camera takes 1 photo
2. AI detects objects (people, cars, potholes, stairs)
3. Prints warnings to terminal
4. Saves result to gallery

**Expected output:**
```
📱 TERMUX PEDESTRIAN NAVIGATION SYSTEM
🔧 Initializing AI components...
✅ System initialized!
📸 Taking single photo...
✅ Photo captured, processing...

⚠️  [PERSON] near - right (threat: 70/100)
⚠️  [POTHOLE] immediate - center (threat: 92/100)

💾 Saved: ~/storage/pictures/detection_152034.jpg
✅ Done!
```

#### 5.2 View Results
- Open your **Gallery app**
- Look for `detection_*.jpg`
- You'll see detected objects with colored boxes!

---

## 🎮 How to Use

### Mode 1: Single Shot (Quick Check)
```bash
python termux_main.py --mode single
```
**Use when:** Checking a specific area before walking

---

### Mode 2: Continuous (Real Walking)
```bash
python termux_main.py --mode continuous --duration 60
```
**What happens:**
- Captures photos every 0.1 seconds (10 FPS)
- Detects hazards in real-time
- Prints warnings to screen
- Auto-saves frames every 5 seconds
- Runs for 60 seconds

**To stop early:** Press Ctrl + C (volume down + C)

---

### Mode 3: Long Walk (1 hour)
```bash
python termux_main.py --mode continuous --duration 3600
```
- Runs for 1 hour
- Perfect for real navigation
- Uses ~20% battery

---

## 📊 Real-World Usage

### Scenario 1: Walking to Class
```bash
# Start detection
python termux_main.py --mode continuous --duration 600

# Put phone in pocket (camera facing out) or mount on chest
# Walk normally
# System detects obstacles automatically
# Check terminal for warnings

# Stop when you arrive (Ctrl+C)
```

### Scenario 2: Testing New Route
```bash
# Take single photos at key points
python termux_main.py --mode single
# Walk a bit
python termux_main.py --mode single
# Repeat
```

---

## 🔋 Battery Life

### Normal Mode
- Resolution: 320x240
- FPS: 10
- **Runtime:** 4-5 hours

### Battery Saver Mode
Edit: `nano termux/config_termux.py`
```python
BATTERY_SAVER_MODE = True
LOW_BATTERY_THRESHOLD = 20  # Auto-saves battery at 20%
```
- **Runtime:** 6-8 hours

---

## 📸 Understanding the Output

### Detection Colors
- 🔴 **Red Box:** IMMEDIATE danger (< 2 meters)
- 🟠 **Orange Box:** NEAR (2-5 meters)
- 🟢 **Green Box:** FAR (> 5 meters)

### Object Classes
- `person` - People walking
- `car`, `truck`, `bus` - Vehicles
- `bicycle`, `motorcycle` - Two-wheelers
- `pothole` - Road hazards (custom CV)
- `stairs` - Stairs/steps (custom CV)
- `dog`, `cat` - Animals

### Threat Scores
- 90-100: Critical danger
- 70-89: High threat
- 50-69: Moderate
- < 50: Low risk

---

## 🛠️ Performance Tuning

### If Too Slow (< 5 FPS)

#### Option 1: Lower Resolution
```bash
nano termux/config_termux.py
```
Change:
```python
FRAME_WIDTH = 240  # Was 320
FRAME_HEIGHT = 180 # Was 240
```

#### Option 2: Reduce FPS
```python
TARGET_FPS = 5  # Was 10
```

#### Option 3: Disable Custom Detection
```python
ENABLE_STAIRS = False
ENABLE_POTHOLES = False
```
(Only use YOLO, faster but less accurate)

---

### If Too Fast (Draining Battery)
```python
TARGET_FPS = 8  # Reduce from 10
SAVE_INTERVAL = 10  # Save less often
```

---

## 🐛 Troubleshooting

### Problem: "Module not found"
**Solution:**
```bash
cd ~/pedestrian-navigation-ai
pip install ultralytics opencv-python-headless torch torchvision
```

---

### Problem: Camera black screen
**Solution:**
```bash
# 1. Check permissions
# Android Settings → Apps → Termux:API → Permissions → Camera → Allow

# 2. Test camera manually
termux-camera-photo test.jpg

# 3. Check if test.jpg exists
ls -lh test.jpg
```

---

### Problem: "Permission denied" when saving
**Solution:**
```bash
# Re-grant storage access
termux-setup-storage
# Tap "Allow" again
```

---

### Problem: Out of memory
**Solution:**
```bash
# 1. Close all other apps
# 2. Restart Termux
# 3. Lower resolution (see Performance Tuning above)
# 4. Clear pip cache
pip cache purge
```

---

### Problem: Too slow (< 5 FPS)
**Solution:**
```bash
# Enable Performance Mode on OnePlus 11R:
# Settings → Battery → Performance Mode → ON

# In Termux, lower settings:
nano termux/config_termux.py
# Change FRAME_WIDTH to 240, FRAME_HEIGHT to 180
```

---

## 📱 OnePlus 11R Specific Tips

### Enable Performance Mode
- Settings → Battery → Performance Mode → **ON**
- Gives ~2 extra FPS

### Disable Battery Optimization for Termux
- Settings → Apps → Termux → Battery
- Select **"Don't optimize"**
- Prevents Android from killing app

### Mount Phone for Best Results
1. **Chest Mount:** Use phone lanyard, camera facing forward
2. **Pocket Mount:** In shirt pocket, camera lens visible
3. **Hand Held:** Hold steady at chest level

### Camera Angle
- Point forward and slightly downward (~15° angle)
- This captures both ground hazards and forward obstacles

---

## 🎯 Best Practices

### Before Walking
1. ✅ Charge phone to 80%+
2. ✅ Test camera: `bash termux/test_camera.sh`
3. ✅ Run single shot test to verify
4. ✅ Mount phone securely
5. ✅ Start continuous mode

### During Walking
- 📱 Keep phone stable (minimize shaking)
- 🔊 Glance at terminal for warnings
- 🔋 Monitor battery percentage
- 📸 System auto-saves frames every 5 seconds

### After Walking
- 🛑 Stop with Ctrl+C
- 📊 Check Gallery for saved detections
- 📝 Review logs if needed: `cat logs/termux_nav_*.log`

---

## 🔍 Viewing Saved Photos

### In Gallery
- Open **Gallery app**
- Look for `detection_*.jpg` (single shots)
- Look for `nav_*.jpg` (continuous frames)
- Photos show colored boxes around detected objects

### In Termux
```bash
# List saved photos
ls -lh ~/storage/pictures/detection_*.jpg
ls -lh ~/storage/pictures/nav_*.jpg

# View with Termux
termux-open ~/storage/pictures/detection_latest.jpg
```

---

## 📊 Check System Status

### View Configuration
```bash
cd ~/pedestrian-navigation-ai
python termux/config_termux.py
```
Shows current settings.

### Check Battery
```bash
termux-battery-status
```

### Check Storage
```bash
df -h ~/storage/pictures
```

---

## 🎓 Advanced Features

### Feature 1: Auto-Save Every Photo
```python
# In config_termux.py:
AUTO_SAVE_FRAMES = True
SAVE_INTERVAL = 1  # Save every second
```

### Feature 2: Motion Detection (Save Battery)
```python
ENABLE_MOTION_DETECTION = True
MOTION_THRESHOLD = 0.5
```
Only processes frames if camera detects movement.

### Feature 3: GPS Logging (Requires termux-api)
```bash
# Get current location
termux-location

# Log location with detection
# (Future feature - coming soon!)
```

---

## 🆘 Getting Help

### Check Logs
```bash
cat ~/pedestrian-navigation-ai/logs/termux_nav_*.log
```

### System Info
```bash
# Termux version
termux-info

# Python packages
pip list | grep -E "torch|opencv|ultralytics"

# Available storage
df -h
```

### Report Bug
- GitHub: https://github.com/AnwarSha771/pedestrian-navigation-ai/issues
- Include: OnePlus 11R, OxygenOS version, error message, log file

---

## 🚀 Quick Reference Card

### Start Detection
```bash
cd ~/pedestrian-navigation-ai
python termux_main.py --mode continuous --duration 3600
```

### Stop Detection
**Press:** Ctrl + C (Volume Down + C)

### Test Camera
```bash
bash termux/test_camera.sh
```

### View Photos
Open **Gallery App** → Look for `detection_*.jpg`

### Check Battery
```bash
termux-battery-status
```

---

## 🎉 You're Ready!

Your OnePlus 11R is now a powerful AI navigation assistant!

**Next steps:**
1. ✅ Test in safe indoor area first
2. ✅ Walk around house to verify detection
3. ✅ Try outdoors in familiar area
4. ✅ Adjust settings for your preference
5. ✅ Use for real navigation!

---

## 📞 Support Contacts

- **GitHub Issues:** https://github.com/AnwarSha771/pedestrian-navigation-ai/issues
- **Documentation:** See `termux/TERMUX_SETUP.md`
- **Quick Help:** See `termux/QUICKSTART.md`

---

**Happy navigating! 🚶‍♂️➡️🏆**

**Your OnePlus 11R + AI = Safer Walking! 💪**
