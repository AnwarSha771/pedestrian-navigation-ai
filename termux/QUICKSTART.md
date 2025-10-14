# 🚀 Quick Start - Termux on OnePlus 11R

**Get running in 3 minutes!**

---

## Prerequisites ✅

1. **Termux** installed from F-Droid (NOT Play Store)
2. **Termux:API** installed from F-Droid
3. OnePlus 11R with Android 11+
4. 2 GB free storage
5. WiFi connection (for initial setup)

---

## 🎯 Quick Installation

### 1. Open Termux, run:
```bash
# Grant storage access
termux-setup-storage

# Download and run setup
cd ~
wget https://raw.githubusercontent.com/AnwarSha771/pedestrian-navigation-ai/main/termux/setup_termux.sh
bash setup_termux.sh
```

**Wait 10-15 minutes** for installation ☕

---

### 2. Get project code:
```bash
cd ~
git clone https://github.com/AnwarSha771/pedestrian-navigation-ai.git
cd pedestrian-navigation-ai
```

---

### 3. Test camera:
```bash
bash termux/test_camera.sh
```

Should show: ✅ Camera works!

---

### 4. Run detection:
```bash
python termux_main.py --mode single
```

Should detect objects and save photo!

---

## 🎮 Basic Commands

### Single Photo Detection
```bash
python termux_main.py --mode single
```
- Takes 1 photo
- Detects hazards
- Saves to: `~/storage/pictures/`

### Continuous Detection (1 minute)
```bash
python termux_main.py --mode continuous --duration 60
```
- Real-time detection
- 10 FPS
- Auto-saves frames

### Custom Duration (5 minutes)
```bash
python termux_main.py --mode continuous --duration 300
```

### Stop Anytime
Press: **Ctrl + C**

---

## 📱 Expected Output

```
📱 TERMUX PEDESTRIAN NAVIGATION SYSTEM
   Running on Android via Termux
==========================================

🔧 Initializing AI components...
✅ System initialized!
   Resolution: 320x240
   Target FPS: 10
   Camera mode: termux-api

📸 Taking single photo...
✅ Photo captured, processing...

⚠️  [PERSON] near - right (threat: 70/100)
⚠️  [POTHOLE] immediate - center (threat: 92/100)

💾 Saved: ~/storage/pictures/detection_152034.jpg
✅ Done!
```

---

## 📊 View Results

### Open Gallery App
- Photos → Look for `detection_*.jpg` or `nav_*.jpg`
- Shows detected objects with boxes and labels

### Check in Termux
```bash
ls -lh ~/storage/pictures/nav_*.jpg
```

---

## 🐛 Quick Fixes

### "Module not found"
```bash
cd ~/pedestrian-navigation-ai
pip install ultralytics opencv-python-headless torch
```

### "Camera permission denied"
- Settings → Apps → Termux:API → Permissions → Camera → Allow

### "Too slow"
- Close other apps
- Enable Performance Mode (Android settings)

### "Command not found"
```bash
pkg install termux-api
```

---

## 🎓 Next Steps

1. ✅ Run `--mode single` once
2. ✅ Try `--mode continuous` for 30 seconds
3. ✅ Walk around and test
4. ✅ Check battery usage
5. ✅ Read full guide: `termux/TERMUX_SETUP.md`

---

## 💡 Pro Tips

- **Battery:** Start with 80%+ charge
- **Lighting:** Works best in daylight
- **Stable:** Hold phone steady at chest level
- **Storage:** Keep 500 MB free
- **Speed:** Close background apps for best FPS

---

## 📖 Full Documentation

For advanced configuration, troubleshooting, and optimization:
```bash
cd ~/pedestrian-navigation-ai/termux
cat TERMUX_SETUP.md
```

---

## 🆘 Help

**GitHub Issues:** https://github.com/AnwarSha771/pedestrian-navigation-ai/issues

**Check logs:**
```bash
cat ~/pedestrian-navigation-ai/logs/termux_nav_*.log
```

---

**Ready? Let's detect some hazards! 🚶‍♂️➡️🚧**
