# Configuration settings for the Pedestrian Navigation System

# Detection Settings
CONFIDENCE_THRESHOLD = 0.45  # Minimum confidence for detections
IOU_THRESHOLD = 0.45  # Non-max suppression threshold
MAX_DETECTIONS = 10  # Maximum number of detections per frame

# Custom Hazard Classes (in addition to COCO classes)
HAZARD_CLASSES = {
    'stairs': 0,
    'curb': 1,
    'pothole': 2,
    'manhole': 3,
    'broken_pavement': 4,
    'tactile_paving': 5,
    'step': 6,
    'gap': 7
}

# Priority Levels (higher = more critical)
PRIORITY_LEVELS = {
    'pothole': 5,
    'manhole': 5,
    'gap': 5,
    'stairs': 4,
    'curb': 4,
    'step': 4,
    'broken_pavement': 3,
    'tactile_paving': 3,
    'person': 2,
    'bicycle': 2,
    'car': 3,
    'default': 1
}

# Distance Calculation Parameters
DISTANCE_THRESHOLDS = {
    'immediate': {
        'bbox_height_ratio': 0.3,  # >30% of frame height
        'bbox_bottom_ratio': 0.8,  # Bottom >80% down frame
        'distance_m': 2.0
    },
    'near': {
        'bbox_height_ratio': 0.15,  # >15% of frame height
        'bbox_bottom_ratio': 0.6,   # Bottom >60% down frame
        'distance_m': 5.0
    },
    'far': {
        'bbox_height_ratio': 0.0,   # Any smaller object
        'bbox_bottom_ratio': 0.0,   # Any position
        'distance_m': 10.0
    }
}

# Audio Feedback Settings
AUDIO_ENABLED = True
ANNOUNCEMENT_COOLDOWN = 3.0  # Seconds between same-object announcements
MIN_PRIORITY_FOR_AUDIO = 2  # Don't announce objects below this priority
USE_OFFLINE_TTS = True  # Use pyttsx3 instead of gTTS for faster response

# Sidewalk Edge Detection
EDGE_DETECTION_ENABLED = True
EDGE_WARNING_DISTANCE = 0.2  # Warn if edge is within 20% from frame edge
CANNY_THRESHOLD1 = 50
CANNY_THRESHOLD2 = 150

# Visual Display Settings
SHOW_BOUNDING_BOXES = True
SHOW_LABELS = True
SHOW_CONFIDENCE = True
SHOW_DISTANCE = True
SHOW_FPS = True

# Colors (BGR format for OpenCV)
COLORS = {
    'immediate': (0, 0, 255),    # Red
    'near': (0, 165, 255),       # Orange
    'far': (0, 255, 0),          # Green
    'edge': (255, 255, 0),       # Cyan
    'text': (255, 255, 255),     # White
    'background': (0, 0, 0)      # Black
}

# Model Settings
MODEL_PATH = 'yolov8n.pt'  # Will use pre-trained COCO model
# MODEL_PATH = 'models/yolov8n-custom.pt'  # Use custom trained model if available
DEVICE = 'cuda'  # 'cuda' for GPU, 'cpu' for CPU (auto-detected)
IMG_SIZE = 640  # Input image size for YOLO

# Camera/Video Settings
VIDEO_SOURCE = 0  # 0 for webcam, or path to video file
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS_TARGET = 30
