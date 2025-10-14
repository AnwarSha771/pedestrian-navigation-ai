"""
Mobile-Optimized Configuration for Termux/Android
Specifically tuned for OnePlus 11R (Snapdragon 8+ Gen 1)
"""

# ============================================
# DEVICE SETTINGS
# ============================================

DEVICE_NAME = "OnePlus 11R"
DEVICE_PLATFORM = "Termux/Android"

# ============================================
# CAMERA SETTINGS
# ============================================

# Resolution (lower = faster)
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Frame rate (10 FPS is good balance for mobile)
TARGET_FPS = 10
FRAME_SKIP = 0  # Process every frame

# Camera source
CAMERA_ID = 0  # 0 = back camera, 1 = front camera
USE_TERMUX_API = True  # Use termux-camera-photo

# ============================================
# DETECTION SETTINGS
# ============================================

# YOLO Configuration
YOLO_MODEL = "yolov8n.pt"  # Nano model (6 MB, fastest)
CONFIDENCE_THRESHOLD = 0.5  # Higher = fewer false positives
IOU_THRESHOLD = 0.45
MAX_DETECTIONS = 10  # Limit for performance

# Enable/disable detection types
ENABLE_YOLO = True
ENABLE_STAIRS = True
ENABLE_POTHOLES = True
ENABLE_SIDEWALK = False  # Too CPU-intensive for mobile

# Custom hazard detection
STAIRS_MIN_LINES = 3
STAIRS_MIN_AREA = 500  # pixels
POTHOLE_MIN_AREA = 300  # pixels

# ============================================
# PROXIMITY SETTINGS
# ============================================

# Distance categories (based on bounding box analysis)
IMMEDIATE_THRESHOLD = 0.7  # > 70% = immediate danger
NEAR_THRESHOLD = 0.4       # 40-70% = near
FAR_THRESHOLD = 0.0        # < 40% = far

# Threat scoring weights
THREAT_DISTANCE_WEIGHT = 0.6
THREAT_SIZE_WEIGHT = 0.3
THREAT_CLASS_WEIGHT = 0.1

# Class-specific threat multipliers
THREAT_MULTIPLIERS = {
    'pothole': 2.5,
    'stairs': 2.0,
    'person': 1.5,
    'car': 2.0,
    'bicycle': 1.8,
    'motorcycle': 1.8,
    'truck': 2.2,
    'bus': 2.2,
    'dog': 1.3,
    'cat': 1.0
}

# ============================================
# AUDIO/FEEDBACK SETTINGS
# ============================================

# Audio disabled in Termux (no TTS support)
ENABLE_AUDIO = False
AUDIO_COOLDOWN = 3.0  # seconds

# Terminal warnings
ENABLE_TERMINAL_WARNINGS = True
WARNING_FORMAT = "⚠️  [{class}] {distance} - {direction} (threat: {threat}/100)"

# ============================================
# BATTERY OPTIMIZATION
# ============================================

# Power saving modes
BATTERY_SAVER_MODE = False  # Auto-adjust based on battery level
LOW_BATTERY_THRESHOLD = 20  # percent

# Low battery settings (auto-applied when < threshold)
LOW_BATTERY_FPS = 5
LOW_BATTERY_RESOLUTION = (240, 180)
LOW_BATTERY_FRAME_SKIP = 2  # Process every 3rd frame

# Motion detection (skip processing if no motion)
ENABLE_MOTION_DETECTION = True
MOTION_THRESHOLD = 0.5  # Lower = more sensitive

# ============================================
# STORAGE SETTINGS
# ============================================

# Output directories
OUTPUT_DIR = "~/storage/pictures"  # Accessible via Android gallery
LOG_DIR = "~/pedestrian-navigation-ai/logs"
TEMP_DIR = "/data/data/com.termux/files/usr/tmp/termux_nav"

# Auto-save settings
AUTO_SAVE_FRAMES = True
SAVE_INTERVAL = 5  # seconds
SAVE_FORMAT = "jpg"
SAVE_QUALITY = 85  # 0-100

# Keep only recent files (auto-cleanup)
MAX_SAVED_FILES = 100
AUTO_DELETE_OLD = True

# ============================================
# LOGGING SETTINGS
# ============================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
LOG_FILE_FORMAT = "termux_nav_%Y%m%d_%H%M%S.log"
MAX_LOG_SIZE_MB = 10

# Console output
VERBOSE = True
SHOW_FPS = True
SHOW_DETECTION_COUNT = True

# ============================================
# PERFORMANCE SETTINGS
# ============================================

# Threading
USE_THREADING = False  # Single thread for mobile stability
NUM_WORKERS = 1

# Memory management
MAX_FRAME_BUFFER = 5
CLEAR_CACHE_INTERVAL = 300  # seconds

# Garbage collection
FORCE_GC_INTERVAL = 60  # seconds

# ============================================
# UI SETTINGS
# ============================================

# Display settings
SHOW_BOUNDING_BOXES = True
SHOW_LABELS = True
SHOW_CONFIDENCE = True
SHOW_DISTANCE = True

# Colors (BGR format)
COLOR_IMMEDIATE = (0, 0, 255)    # Red
COLOR_NEAR = (0, 165, 255)       # Orange
COLOR_FAR = (0, 255, 0)          # Green
COLOR_TEXT = (255, 255, 255)     # White
COLOR_BG = (0, 0, 0)             # Black

# Font settings
FONT_SCALE = 0.4  # Smaller for mobile
FONT_THICKNESS = 1
FONT = 2  # cv2.FONT_HERSHEY_SIMPLEX

# ============================================
# NETWORK SETTINGS (Optional)
# ============================================

# Remote logging (optional)
ENABLE_REMOTE_LOGGING = False
REMOTE_SERVER = "http://your-server.com/api/log"
REMOTE_API_KEY = "your-api-key"

# Upload detections (optional)
ENABLE_CLOUD_UPLOAD = False
UPLOAD_INTERVAL = 60  # seconds
UPLOAD_ONLY_WIFI = True

# ============================================
# DEVELOPMENT/DEBUG SETTINGS
# ============================================

DEBUG_MODE = False
SAVE_DEBUG_FRAMES = False
DEBUG_OUTPUT_DIR = "~/pedestrian-navigation-ai/debug"

# Profiling
ENABLE_PROFILING = False
PROFILE_INTERVAL = 10  # seconds

# Test mode (use video file instead of camera)
TEST_MODE = False
TEST_VIDEO_PATH = "~/storage/downloads/test_video.mp4"

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_battery_level():
    """Get current battery level (requires termux-api)"""
    try:
        import subprocess
        import json
        result = subprocess.run(
            ['termux-battery-status'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('percentage', 100)
    except:
        pass
    return 100  # Assume full if can't read

def should_use_battery_saver():
    """Check if battery saver should be enabled"""
    if not BATTERY_SAVER_MODE:
        return False
    
    battery = get_battery_level()
    return battery < LOW_BATTERY_THRESHOLD

def get_optimized_settings():
    """Get settings optimized for current battery level"""
    if should_use_battery_saver():
        return {
            'fps': LOW_BATTERY_FPS,
            'resolution': LOW_BATTERY_RESOLUTION,
            'frame_skip': LOW_BATTERY_FRAME_SKIP,
            'enable_stairs': False,
            'enable_potholes': False,
        }
    else:
        return {
            'fps': TARGET_FPS,
            'resolution': (FRAME_WIDTH, FRAME_HEIGHT),
            'frame_skip': FRAME_SKIP,
            'enable_stairs': ENABLE_STAIRS,
            'enable_potholes': ENABLE_POTHOLES,
        }

def get_camera_config():
    """Get camera configuration"""
    return {
        'width': FRAME_WIDTH,
        'height': FRAME_HEIGHT,
        'fps': TARGET_FPS,
        'camera_id': CAMERA_ID,
        'use_termux_api': USE_TERMUX_API,
    }

def get_detection_config():
    """Get detection configuration"""
    return {
        'model': YOLO_MODEL,
        'confidence': CONFIDENCE_THRESHOLD,
        'iou': IOU_THRESHOLD,
        'max_detections': MAX_DETECTIONS,
        'enable_yolo': ENABLE_YOLO,
        'enable_stairs': ENABLE_STAIRS,
        'enable_potholes': ENABLE_POTHOLES,
        'enable_sidewalk': ENABLE_SIDEWALK,
    }

# ============================================
# PRINT CONFIG (for debugging)
# ============================================

def print_config():
    """Print current configuration"""
    print("\n" + "="*60)
    print("📱 TERMUX CONFIGURATION")
    print("="*60)
    print(f"Device: {DEVICE_NAME}")
    print(f"Platform: {DEVICE_PLATFORM}")
    print(f"Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
    print(f"Target FPS: {TARGET_FPS}")
    print(f"Battery Saver: {BATTERY_SAVER_MODE}")
    print(f"Battery Level: {get_battery_level()}%")
    print(f"YOLO Model: {YOLO_MODEL}")
    print(f"Confidence: {CONFIDENCE_THRESHOLD}")
    print(f"Audio: {'Enabled' if ENABLE_AUDIO else 'Disabled'}")
    print(f"Detections: YOLO={ENABLE_YOLO}, Stairs={ENABLE_STAIRS}, Potholes={ENABLE_POTHOLES}")
    print("="*60 + "\n")

if __name__ == "__main__":
    print_config()
