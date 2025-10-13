# Installation and Setup Guide

## System Requirements

### Hardware
- **Minimum**: 
  - CPU: Intel i5 or equivalent
  - RAM: 8GB
  - Webcam or video input device
  
- **Recommended**:
  - CPU: Intel i7 or equivalent
  - RAM: 16GB
  - GPU: NVIDIA GPU with CUDA support (for faster inference)
  - Webcam: 720p or higher resolution

### Software
- Python 3.8 or higher
- pip package manager
- (Optional) CUDA Toolkit 11.8+ for GPU acceleration

## Installation Steps

### 1. Clone or Download the Project

```bash
cd pedestrian-navigation-ai
```

### 2. Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** The first time you run the system, YOLOv8 will automatically download the pre-trained model (~6MB).

### 4. Test Installation

```bash
# Quick test
python demo.py

# Or run main application
python main.py --source 0
```

## Troubleshooting

### Issue: "Import ultralytics could not be resolved"

**Solution:**
```bash
pip install ultralytics
```

### Issue: "No module named 'torch'"

**Solution:**
```bash
# CPU version
pip install torch torchvision

# GPU version (CUDA 11.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Issue: "Could not open video source"

**Solutions:**
1. Check webcam connection: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`
2. Try different camera index: `python main.py --source 1`
3. Use video file instead: `python main.py --source path/to/video.mp4`

### Issue: "TTS engine not available"

**Solution:**
```bash
pip install pyttsx3

# Windows: May need to install pywin32
pip install pywin32
```

### Issue: Low FPS / Slow Performance

**Solutions:**
1. Use GPU if available (install CUDA + PyTorch with CUDA)
2. Lower resolution: Edit `config.py` and reduce `FRAME_WIDTH` and `FRAME_HEIGHT`
3. Increase confidence threshold: `python main.py --confidence 0.6`
4. Reduce `MAX_DETECTIONS` in `config.py`

### Issue: Too many/few detections

**Solutions:**
- Too many detections: Increase confidence threshold
  ```bash
  python main.py --confidence 0.6
  ```
- Too few detections: Lower confidence threshold
  ```bash
  python main.py --confidence 0.3
  ```

## Configuration

### Custom Settings

Edit `config.py` to customize:

```python
# Detection sensitivity
CONFIDENCE_THRESHOLD = 0.45  # Lower = more detections

# Audio frequency
ANNOUNCEMENT_COOLDOWN = 3.0  # Seconds between announcements

# Distance thresholds
DISTANCE_THRESHOLDS = {
    'immediate': {
        'distance_m': 2.0  # Alert if object within 2 meters
    },
    ...
}
```

### Using Custom Trained Model

If you train a custom YOLOv8 model:

1. Place your model in `models/` directory
2. Update `config.py`:
   ```python
   MODEL_PATH = 'models/yolov8n-custom.pt'
   ```

## Performance Optimization

### For Hackathon Demo (Maximum Quality)

```python
# In config.py
CONFIDENCE_THRESHOLD = 0.4  # More sensitive
SHOW_BOUNDING_BOXES = True
SHOW_LABELS = True
SHOW_CONFIDENCE = True
AUDIO_ENABLED = True
```

### For Production (Balanced)

```python
# In config.py
CONFIDENCE_THRESHOLD = 0.5  # More selective
IMG_SIZE = 416  # Smaller for faster inference
MAX_DETECTIONS = 5  # Reduce processing
```

### For Low-End Hardware

```python
# In config.py
CONFIDENCE_THRESHOLD = 0.6
IMG_SIZE = 320  # Smallest size
MAX_DETECTIONS = 3
EDGE_DETECTION_ENABLED = False  # Disable to save CPU
```

## Next Steps

1. **Test with sample videos**: Download urban walking videos and test detection accuracy
2. **Calibrate audio warnings**: Adjust cooldown and priority levels based on feedback
3. **Collect training data**: Annotate custom hazards (potholes, curbs) for improved accuracy
4. **Deploy to mobile**: Export model to TFLite for mobile deployment

## Support

For issues and questions:
1. Check this INSTALL.md guide
2. Review README.md for usage examples
3. Inspect logs with `--debug` flag: `python main.py --debug`

## Hardware Integration (Future)

### Raspberry Pi Deployment
- Use TensorFlow Lite for model inference
- Add haptic feedback motor via GPIO
- Use USB sound card for better audio

### Wearable Device
- Intel Neural Compute Stick for edge AI
- Bone conduction headphones for audio
- Chest-mounted camera for stable POV
