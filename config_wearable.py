"""
Wearable Device Configuration for Pedestrian Navigation System
Optimized for battery life, lightweight processing, and hands-free operation
Target devices: Smart glasses, body-worn cameras, head-mounted displays
"""

# ============================================================
# WEARABLE DEVICE SETTINGS
# ============================================================

# Device profiles - uncomment the one you're using
DEVICE_TYPE = "smart_glasses"  # Options: smart_glasses, body_camera, headset, raspberry_pi

DEVICE_PROFILES = {
    "smart_glasses": {
        "camera_index": 0,
        "resolution": (320, 240),  # Lower res for battery
        "fps_target": 10,  # Process 10 frames per second
        "model": "yolov8n",  # Nano model (6MB)
        "confidence": 0.5,
        "enable_cv_detection": False,  # Disable custom CV to save power
        "audio_output": "bluetooth",
        "haptic_enabled": True,
    },
    "body_camera": {
        "camera_index": 0,
        "resolution": (416, 416),  # Medium quality
        "fps_target": 15,
        "model": "yolov8n",
        "confidence": 0.45,
        "enable_cv_detection": True,
        "audio_output": "speaker",
        "haptic_enabled": False,
    },
    "headset": {
        "camera_index": 0,
        "resolution": (640, 480),
        "fps_target": 20,
        "model": "yolov8n",
        "confidence": 0.45,
        "enable_cv_detection": True,
        "audio_output": "headphones",
        "haptic_enabled": True,
    },
    "raspberry_pi": {
        "camera_index": 0,
        "resolution": (320, 240),
        "fps_target": 5,  # Very low for Pi Zero
        "model": "yolov8n",
        "confidence": 0.5,
        "enable_cv_detection": False,
        "audio_output": "speaker",
        "haptic_enabled": True,
    }
}

# Get active profile
ACTIVE_PROFILE = DEVICE_PROFILES[DEVICE_TYPE]

# ============================================================
# CAMERA SETTINGS (Optimized for wearables)
# ============================================================

CAMERA_INDEX = ACTIVE_PROFILE["camera_index"]
FRAME_WIDTH = ACTIVE_PROFILE["resolution"][0]
FRAME_HEIGHT = ACTIVE_PROFILE["resolution"][1]
TARGET_FPS = ACTIVE_PROFILE["fps_target"]

# Camera mounting position (affects detection zones)
CAMERA_MOUNTING = "head"  # Options: head, chest, waist
CAMERA_ANGLE = 0  # Tilt in degrees (0 = horizontal)

# ============================================================
# DETECTION SETTINGS (Battery optimized)
# ============================================================

YOLO_MODEL = ACTIVE_PROFILE["model"]
CONFIDENCE_THRESHOLD = ACTIVE_PROFILE["confidence"]
ENABLE_CUSTOM_CV_DETECTION = ACTIVE_PROFILE["enable_cv_detection"]

# Process every Nth frame to save battery
FRAME_SKIP = 2 if TARGET_FPS > 10 else 1

# Priority classes for wearable use case
PRIORITY_LEVELS = {
    # Critical hazards (priority 5-4)
    "pothole": 5,
    "stairs": 4,
    "curb": 4,
    
    # Important obstacles (priority 3)
    "car": 3,
    "bicycle": 3,
    "motorcycle": 3,
    "pole": 3,
    
    # Awareness items (priority 2)
    "person": 2,
    "dog": 2,
    "traffic_light": 2,
    
    # Low priority (priority 1)
    "bench": 1,
    "fire_hydrant": 1,
}

# ============================================================
# AUDIO FEEDBACK (Wearable-specific)
# ============================================================

AUDIO_OUTPUT_TYPE = ACTIVE_PROFILE["audio_output"]

# Audio settings by output type
AUDIO_SETTINGS = {
    "bluetooth": {
        "enabled": True,
        "volume": 0.8,
        "rate": 180,  # Words per minute
        "voice": "default",
        "spatial_audio": True,  # Directional audio if supported
    },
    "bone_conduction": {
        "enabled": True,
        "volume": 1.0,  # Max volume for bone conduction
        "rate": 150,
        "voice": "default",
        "spatial_audio": False,
    },
    "speaker": {
        "enabled": True,
        "volume": 0.7,
        "rate": 160,
        "voice": "default",
        "spatial_audio": False,
    },
    "headphones": {
        "enabled": True,
        "volume": 0.6,
        "rate": 170,
        "voice": "default",
        "spatial_audio": True,
    }
}

ACTIVE_AUDIO = AUDIO_SETTINGS.get(AUDIO_OUTPUT_TYPE, AUDIO_SETTINGS["speaker"])

# Announcement settings
ANNOUNCEMENT_COOLDOWN = 4.0  # Longer cooldown for wearables
MIN_PRIORITY_FOR_AUDIO = 2
URGENT_ONLY_MODE = False  # Set True to only announce priority 4+

# ============================================================
# HAPTIC FEEDBACK (Vibration patterns)
# ============================================================

HAPTIC_ENABLED = ACTIVE_PROFILE["haptic_enabled"]

# Vibration patterns (duration in ms, intensity 0-1)
HAPTIC_PATTERNS = {
    "immediate_danger": [(200, 1.0), (100, 0), (200, 1.0), (100, 0), (200, 1.0)],  # 3 strong pulses
    "near_hazard": [(150, 0.7), (150, 0)],  # 1 medium pulse
    "far_warning": [(100, 0.4)],  # 1 light pulse
    "left_direction": [(50, 0.6), (50, 0), (50, 0.6)],  # 2 quick pulses
    "right_direction": [(100, 0.6)],  # 1 longer pulse
    "center_direction": [(50, 0.8), (50, 0), (50, 0.8), (50, 0), (50, 0.8)],  # 3 quick pulses
}

# Haptic GPIO pins (for Raspberry Pi)
HAPTIC_GPIO_PIN = 18  # BCM pin number
HAPTIC_USE_PWM = True  # Use PWM for intensity control

# ============================================================
# BATTERY OPTIMIZATION
# ============================================================

BATTERY_SAVER_MODE = True
BATTERY_THRESHOLDS = {
    "normal": 50,  # Above 50%: full performance
    "medium": 20,  # 20-50%: reduce FPS by 30%
    "low": 10,     # 10-20%: reduce FPS by 50%, disable CV
    "critical": 5,  # Below 5%: emergency mode (YOLO only, 5 FPS)
}

# Automatic power management
AUTO_SLEEP_TIMEOUT = 300  # Sleep after 5 minutes of no detection
WAKE_ON_MOTION = True  # Use accelerometer to wake up

# ============================================================
# DISTANCE ESTIMATION (Wearable calibration)
# ============================================================

# Adjust based on camera mounting position
DISTANCE_CALIBRATION = {
    "head": {  # Eye-level camera
        "height_factor": 1.0,
        "offset": 0.0,
    },
    "chest": {  # Chest-mounted camera
        "height_factor": 1.15,
        "offset": -0.3,
    },
    "waist": {  # Belt-mounted camera
        "height_factor": 1.3,
        "offset": -0.5,
    }
}

ACTIVE_CALIBRATION = DISTANCE_CALIBRATION[CAMERA_MOUNTING]

# Distance thresholds (in meters)
DISTANCE_THRESHOLDS = {
    "immediate": 2.0,  # Less than 2 meters
    "near": 5.0,       # 2-5 meters
    "far": 10.0,       # 5-10 meters
}

# ============================================================
# DISPLAY SETTINGS (For debugging only)
# ============================================================

# Disable display on actual wearables to save power
ENABLE_DISPLAY = False  # Set False for production wearable
DISPLAY_FPS = False
DISPLAY_DETECTIONS = False
HEADLESS_MODE = True  # Run without GUI

# ============================================================
# CONNECTIVITY (For cloud/companion app)
# ============================================================

# Bluetooth connection to phone app
BLUETOOTH_ENABLED = True
BLUETOOTH_DEVICE_NAME = "PedestrianNav"

# WiFi for data sync
WIFI_ENABLED = False
CLOUD_SYNC = False

# Companion app integration
SEND_TO_APP = True  # Send detection data to phone app
APP_UPDATE_RATE = 1.0  # Update app every 1 second

# ============================================================
# DATA LOGGING (For training/improvement)
# ============================================================

LOG_DETECTIONS = True
LOG_PATH = "logs/wearable/"
LOG_FORMAT = "json"  # json, csv
LOG_INCLUDE_FRAMES = False  # Don't save frames to save space

# ============================================================
# HARDWARE-SPECIFIC SETTINGS
# ============================================================

# Raspberry Pi settings
USE_PICAMERA = False  # Set True if using Pi Camera module
PI_CAMERA_ROTATION = 0  # 0, 90, 180, 270

# ESP32-CAM settings
ESP32_STREAM_URL = None  # e.g., "http://192.168.1.100:81/stream"

# Arduino haptic controller
ARDUINO_SERIAL_PORT = None  # e.g., "COM3" or "/dev/ttyUSB0"
ARDUINO_BAUD_RATE = 9600

# ============================================================
# VISUAL SETTINGS (Minimal for wearables)
# ============================================================

# Colors (RGB format) - only used if display enabled
COLOR_IMMEDIATE = (0, 0, 255)    # Red
COLOR_NEAR = (0, 165, 255)       # Orange
COLOR_FAR = (0, 255, 0)          # Green
COLOR_SIDEWALK = (255, 255, 0)   # Cyan

DRAW_BOUNDING_BOXES = False
DRAW_LABELS = False
DRAW_STATUS = False

# ============================================================
# GESTURE CONTROL (For hands-free operation)
# ============================================================

GESTURE_CONTROL_ENABLED = False
GESTURES = {
    "wave_hand": "toggle_audio",
    "point_left": "repeat_last_left",
    "point_right": "repeat_last_right",
    "thumbs_up": "path_clear_confirmation",
}

# ============================================================
# ADVANCED FEATURES
# ============================================================

# Environmental awareness
USE_AMBIENT_LIGHT_SENSOR = False
USE_ACCELEROMETER = True  # For motion detection
USE_GYROSCOPE = True  # For camera orientation

# Adaptive behavior
ADJUST_TO_WALKING_SPEED = True  # Increase detection range when moving fast
ADJUST_TO_ENVIRONMENT = True  # Indoor vs outdoor modes

# Multi-modal feedback
COMBINE_AUDIO_HAPTIC = True  # Use both audio and haptic together
AUDIO_OR_HAPTIC_ONLY = False  # Use only one based on environment noise

print(f"✓ Wearable config loaded: {DEVICE_TYPE}")
print(f"  Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
print(f"  Target FPS: {TARGET_FPS}")
print(f"  Audio: {AUDIO_OUTPUT_TYPE}")
print(f"  Haptic: {'Enabled' if HAPTIC_ENABLED else 'Disabled'}")
