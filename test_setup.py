"""
Test script to verify installation and basic functionality
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    tests = [
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("Ultralytics (YOLOv8)", "ultralytics"),
        ("PyTorch", "torch"),
        ("PIL", "PIL"),
    ]
    
    failed = []
    for name, module in tests:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            failed.append(name)
    
    # Optional imports
    optional = [
        ("pyttsx3 (TTS)", "pyttsx3"),
        ("gTTS", "gtts"),
    ]
    
    print("\nOptional imports:")
    for name, module in optional:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ⚠ {name} - not installed (audio may not work)")
    
    return len(failed) == 0

def test_camera():
    """Test camera access"""
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print(f"  ✓ Camera working (resolution: {frame.shape[1]}x{frame.shape[0]})")
                return True
            else:
                print("  ✗ Camera opened but failed to read frame")
                return False
        else:
            print("  ✗ Could not open camera")
            print("    Try: python main.py --source path/to/video.mp4")
            return False
    except Exception as e:
        print(f"  ✗ Camera test failed: {e}")
        return False

def test_yolo_model():
    """Test YOLOv8 model loading"""
    print("\nTesting YOLOv8 model...")
    try:
        from ultralytics import YOLO
        print("  • Loading YOLOv8-nano model (this may take a moment)...")
        model = YOLO('yolov8n.pt')
        print("  ✓ YOLOv8 model loaded successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to load model: {e}")
        return False

def test_config():
    """Test config file"""
    print("\nTesting configuration...")
    try:
        import config
        print(f"  ✓ Config loaded")
        print(f"    - Confidence threshold: {config.CONFIDENCE_THRESHOLD}")
        print(f"    - Audio enabled: {config.AUDIO_ENABLED}")
        print(f"    - Device: {config.DEVICE}")
        return True
    except Exception as e:
        print(f"  ✗ Config test failed: {e}")
        return False

def test_modules():
    """Test custom modules"""
    print("\nTesting custom modules...")
    try:
        sys.path.insert(0, 'src')
        from detector import HazardDetector
        from proximity import ProximityEstimator
        from audio_feedback import AudioManager
        from sidewalk_detector import SidewalkDetector
        print("  ✓ All custom modules imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Module test failed: {e}")
        return False

def main():
    print("="*60)
    print("🦯 PEDESTRIAN NAVIGATION SYSTEM - TEST SUITE")
    print("="*60)
    print()
    
    results = {
        "Imports": test_imports(),
        "Configuration": test_config(),
        "Custom Modules": test_modules(),
        "Camera": test_camera(),
        "YOLOv8 Model": test_yolo_model(),
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("="*60)
    
    if all(results.values()):
        print("\n✅ All tests passed! System is ready to use.")
        print("\nRun the demo with: python demo.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check camera connection if camera test failed")
        print("3. Review INSTALL.md for detailed setup instructions")
        return 1

if __name__ == '__main__':
    sys.exit(main())
