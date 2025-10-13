# 🦯 Intelligent Pedestrian Navigation for Impaired Users (SAITR02)

## 🎯 Problem Statement
A context-aware navigation system that identifies common urban barriers for visually or mobility-impaired users using real-time Computer Vision.

## 🌟 Key Features

### 1. **Critical Hazard Detection**
- **Stairs/Curbs/Steps**: Major trip hazards
- **Potholes/Manholes/Gaps**: Fall and injury risks
- **Broken Sidewalk/Tactile Paving**: Path obstructions

### 2. **Intelligent Proximity Estimation**
- Real-time distance calculation using bounding box analysis
- Three-tier warning system: Immediate (<2m), Near (2-5m), Far (>5m)

### 3. **Smart Audio Feedback**
- Priority-based obstacle announcement
- Filters out low-priority objects to avoid information overload
- Clear, directional TTS warnings

### 4. **Shore-Lining Assist**
- Sidewalk edge detection using color/texture analysis
- Keeps users safely on the path

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd pedestrian-navigation-ai

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 model (happens automatically on first run)
```

### Run the Demo

```bash
# Using webcam (default)
python main.py

# Using video file
python main.py --source path/to/video.mp4

# With custom confidence threshold
python main.py --confidence 0.5
```

### Keyboard Controls
- **'q'**: Quit application
- **'s'**: Toggle sound warnings
- **'d'**: Toggle debug display
- **'p'**: Pause/Resume detection

## 🏗️ Architecture

```
┌─────────────────┐
│  Camera Input   │
│  (Webcam/Video) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  YOLOv8-Nano Detection  │
│  - Stairs/Curbs         │
│  - Potholes/Gaps        │
│  - Sidewalk Damage      │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Proximity Estimator     │
│  - Bounding Box Size     │
│  - Vertical Position     │
│  - Distance Categories   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Intelligent Filter      │
│  - Priority Ranking      │
│  - Closest Object        │
│  - Threat Assessment     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Audio Feedback (TTS)    │
│  - Directional Warnings  │
│  - Distance Callouts     │
└──────────────────────────┘
```

## 🎮 Demo Scenarios

### Scenario 1: Multiple Obstacles
System detects: person (far), pothole (near), curb (immediate)
**Output**: "DANGER: Curb directly ahead, immediate!"

### Scenario 2: Clear Path
No hazards detected within 5 meters
**Output**: "Path clear for 5 meters"

### Scenario 3: Sidewalk Edge
User drifts toward edge
**Output**: "Caution: Approaching sidewalk edge on right"

## 📊 Technical Details

### Model: YOLOv8-Nano
- **Speed**: ~100 FPS on modern laptop GPU
- **Accuracy**: High precision for urban obstacles
- **Custom Classes**: stairs, curb, pothole, manhole, broken_pavement

### Proximity Algorithm
```python
distance_category = calculate_proximity(
    bbox_height=box_height,
    bbox_y_position=box_bottom,
    frame_height=frame.shape[0]
)
```

### Priority System
1. **Critical** (5): Potholes, Manholes, Large Gaps
2. **High** (4): Stairs, Curbs, Steps
3. **Medium** (3): Broken Pavement, Obstacles
4. **Low** (2): People, Bikes (when far)

## 🏆 Hackathon Winning Features

1. **Context-Specific Detection**: Custom training for urban hazards not in standard datasets
2. **No Information Overload**: Intelligent filtering announces only the most critical obstacle
3. **Practical Deployment**: Runs on laptop/phone hardware, no special equipment needed
4. **Real-World Impact**: Solves actual pain points GPS navigation cannot address

## 📁 Project Structure

```
pedestrian-navigation-ai/
├── main.py                    # Main application entry point
├── src/
│   ├── detector.py           # YOLOv8 hazard detection
│   ├── proximity.py          # Distance estimation
│   ├── audio_feedback.py     # TTS warning system
│   ├── sidewalk_detector.py  # Edge detection for shore-lining
│   └── utils.py              # Helper functions
├── models/
│   └── yolov8n-custom.pt     # Custom trained model (optional)
├── data/
│   └── sample_videos/        # Test videos
├── requirements.txt
└── README.md
```

## 🔧 Configuration

Edit `config.py` to customize:
- Detection confidence threshold
- Distance calculation parameters
- Audio warning frequency
- Priority levels for different hazards

## 📝 Future Enhancements

- [ ] Depth camera integration (Intel RealSense)
- [ ] Haptic feedback vest/band support
- [ ] Cloud-based continuous learning
- [ ] Multi-language TTS support
- [ ] GPS integration for route planning

## 👥 Team & Acknowledgments

Built for SAITR02 Hackathon Challenge
