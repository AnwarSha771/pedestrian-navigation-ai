"""
Wearable Device Version - Pedestrian Navigation System
Optimized for smart glasses, body cameras, and head-mounted displays
Features: Battery optimization, haptic feedback, hands-free operation
"""

import cv2
import time
import numpy as np
from pathlib import Path
import argparse
import json
from datetime import datetime

# Import wearable configuration
import config_wearable as config

# Import core modules
from src.detector import HazardDetector
from src.proximity import ProximityEstimator
from src.audio_feedback import AudioManager
from src.sidewalk_detector import SidewalkDetector


class WearableNavigationSystem:
    """Lightweight navigation system optimized for wearable devices"""
    
    def __init__(self, source=0):
        """
        Initialize wearable navigation system
        
        Args:
            source: Camera index or video file path
        """
        print("\n" + "="*60)
        print("🦯 WEARABLE PEDESTRIAN NAVIGATION SYSTEM")
        print("   Optimized for Smart Glasses & Body Cameras")
        print("="*60)
        
        self.source = source
        self.frame_count = 0
        self.last_detection_time = time.time()
        
        # Battery optimization
        self.battery_level = 100  # Simulated, read from actual battery
        self.sleep_mode = False
        
        # Initialize camera
        self._init_camera()
        
        # Initialize AI components
        print("\n🔧 Initializing AI components (lightweight mode)...")
        self.detector = HazardDetector()
        self.proximity_estimator = ProximityEstimator()
        
        # Initialize audio with wearable settings
        self.audio_manager = AudioManager(
            enabled=config.ACTIVE_AUDIO["enabled"],
            rate=config.ACTIVE_AUDIO["rate"],
            volume=config.ACTIVE_AUDIO["volume"]
        )
        
        # Initialize sidewalk detector (if enabled)
        if config.ENABLE_CUSTOM_CV_DETECTION:
            self.sidewalk_detector = SidewalkDetector()
        else:
            self.sidewalk_detector = None
            print("⚡ Custom CV detection disabled (battery saver)")
        
        # Haptic feedback
        if config.HAPTIC_ENABLED:
            self._init_haptic()
        else:
            self.haptic = None
        
        # Data logging
        if config.LOG_DETECTIONS:
            self._init_logging()
        
        # FPS tracking
        self.fps_start_time = time.time()
        self.fps_frame_count = 0
        self.current_fps = 0
        
        print("\n✅ Wearable system initialized successfully!")
        print(f"   Device: {config.DEVICE_TYPE}")
        print(f"   Resolution: {config.FRAME_WIDTH}x{config.FRAME_HEIGHT}")
        print(f"   Target FPS: {config.TARGET_FPS}")
        print(f"   Headless: {config.HEADLESS_MODE}")
        
    def _init_camera(self):
        """Initialize camera with wearable-optimized settings"""
        print(f"\n📹 Initializing camera: {self.source}")
        print(f"   Resolution: {config.FRAME_WIDTH}x{config.FRAME_HEIGHT}")
        print(f"   Target FPS: {config.TARGET_FPS}")
        
        self.cap = cv2.VideoCapture(self.source)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera: {self.source}")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        # Disable auto-focus for faster processing (if supported)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        
    def _init_haptic(self):
        """Initialize haptic feedback system"""
        print("📳 Initializing haptic feedback...")
        
        try:
            # Try to initialize GPIO for Raspberry Pi
            if config.HAPTIC_GPIO_PIN:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(config.HAPTIC_GPIO_PIN, GPIO.OUT)
                self.haptic = GPIO
                print("✓ GPIO haptic initialized")
        except ImportError:
            print("⚠ GPIO not available (simulating haptic)")
            self.haptic = "simulated"
        except Exception as e:
            print(f"⚠ Haptic init failed: {e}")
            self.haptic = None
    
    def _init_logging(self):
        """Initialize detection logging"""
        log_dir = Path(config.LOG_PATH)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = log_dir / f"detections_{timestamp}.{config.LOG_FORMAT}"
        self.detection_log = []
        
        print(f"📝 Logging enabled: {self.log_file}")
    
    def trigger_haptic(self, pattern_name):
        """Trigger haptic vibration pattern"""
        if not self.haptic or not config.HAPTIC_ENABLED:
            return
        
        pattern = config.HAPTIC_PATTERNS.get(pattern_name, [])
        
        if self.haptic == "simulated":
            print(f"📳 [HAPTIC] {pattern_name}: {pattern}")
            return
        
        # Actual GPIO control
        try:
            import RPi.GPIO as GPIO
            for duration_ms, intensity in pattern:
                if intensity > 0:
                    GPIO.output(config.HAPTIC_GPIO_PIN, GPIO.HIGH)
                    time.sleep(duration_ms / 1000.0)
                else:
                    GPIO.output(config.HAPTIC_GPIO_PIN, GPIO.LOW)
                    time.sleep(duration_ms / 1000.0)
        except Exception as e:
            print(f"⚠ Haptic error: {e}")
    
    def process_frame(self, frame):
        """
        Process a single frame with battery-optimized detection
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Processed frame (if display enabled)
        """
        self.frame_count += 1
        
        # Frame skip for battery optimization
        if self.frame_count % config.FRAME_SKIP != 0:
            return frame
        
        # Run YOLO detection
        yolo_detections = self.detector.detect(frame)
        
        # Run custom CV detection (if enabled)
        if config.ENABLE_CUSTOM_CV_DETECTION and self.sidewalk_detector:
            cv_detections = self.detector.detect_custom_hazards(frame)
            all_detections = self.detector.combine_detections(
                yolo_detections, cv_detections
            )
        else:
            all_detections = yolo_detections
        
        # Analyze proximity and threat for each detection
        analyzed_detections = []
        for det in all_detections:
            analyzed = self.proximity_estimator.analyze_detection(det, frame.shape)
            analyzed_detections.append(analyzed)
        
        # Get most critical threat
        critical_detection = self.proximity_estimator.filter_most_critical(
            analyzed_detections
        )
        
        # Trigger audio feedback
        if critical_detection:
            was_announced = self.audio_manager.process_frame_detections(
                [critical_detection]
            )
            
            # Trigger haptic feedback
            if config.HAPTIC_ENABLED and was_announced:
                distance = critical_detection.get("distance_category", "far")
                direction = critical_detection.get("direction", "center")
                
                # Choose haptic pattern based on urgency
                if distance == "immediate":
                    self.trigger_haptic("immediate_danger")
                elif distance == "near":
                    self.trigger_haptic("near_hazard")
                
                # Add directional haptic
                if direction == "left":
                    self.trigger_haptic("left_direction")
                elif direction == "right":
                    self.trigger_haptic("right_direction")
                elif direction == "center":
                    self.trigger_haptic("center_direction")
        
        # Log detection
        if config.LOG_DETECTIONS and critical_detection:
            self._log_detection(critical_detection)
        
        # Update FPS
        self._update_fps()
        
        return frame
    
    def _log_detection(self, detection):
        """Log detection to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "frame": self.frame_count,
            "class": detection.get("class", "unknown"),
            "confidence": detection.get("confidence", 0.0),
            "distance": detection.get("distance_category", "unknown"),
            "direction": detection.get("direction", "unknown"),
            "threat_score": detection.get("threat_score", 0),
            "bbox": detection.get("bbox", []),
        }
        
        self.detection_log.append(log_entry)
        
        # Write to file every 10 detections
        if len(self.detection_log) >= 10:
            self._flush_log()
    
    def _flush_log(self):
        """Write detection log to disk"""
        if not self.detection_log:
            return
        
        try:
            with open(self.log_file, 'a') as f:
                for entry in self.detection_log:
                    if config.LOG_FORMAT == "json":
                        f.write(json.dumps(entry) + "\n")
                    elif config.LOG_FORMAT == "csv":
                        # Simple CSV format
                        line = f"{entry['timestamp']},{entry['class']},{entry['confidence']},{entry['distance']}\n"
                        f.write(line)
            
            self.detection_log = []
        except Exception as e:
            print(f"⚠ Log write error: {e}")
    
    def _update_fps(self):
        """Update FPS counter"""
        self.fps_frame_count += 1
        elapsed = time.time() - self.fps_start_time
        
        if elapsed > 1.0:
            self.current_fps = self.fps_frame_count / elapsed
            self.fps_frame_count = 0
            self.fps_start_time = time.time()
    
    def run(self):
        """Main processing loop for wearable device"""
        print("\n" + "-"*60)
        print("⚡ Starting wearable detection loop...")
        print("   Mode: Headless (no display)")
        print("   Press Ctrl+C to stop")
        print("-"*60 + "\n")
        
        try:
            while True:
                # Read frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("⚠ Failed to read frame")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Display (only if not headless)
                if not config.HEADLESS_MODE and config.ENABLE_DISPLAY:
                    cv2.imshow("Wearable Navigation", processed_frame)
                    
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        self.audio_manager.toggle_sound()
                
                # Sleep mode check (save battery)
                if config.BATTERY_SAVER_MODE:
                    time_since_detection = time.time() - self.last_detection_time
                    if time_since_detection > config.AUTO_SLEEP_TIMEOUT:
                        print("😴 Entering sleep mode (no activity)")
                        time.sleep(1.0)  # Reduce processing
                
                # Control FPS to target
                time.sleep(1.0 / config.TARGET_FPS)
                
        except KeyboardInterrupt:
            print("\n\n⏹ Stopping wearable system...")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up resources...")
        
        # Flush remaining logs
        if config.LOG_DETECTIONS:
            self._flush_log()
        
        # Release camera
        if self.cap:
            self.cap.release()
        
        # Cleanup GPIO
        if self.haptic and self.haptic != "simulated":
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup()
            except:
                pass
        
        # Close windows
        cv2.destroyAllWindows()
        
        print("✅ Cleanup complete")
        print("\n" + "="*60)
        print("Thank you for using Wearable Navigation System!")
        print("="*60 + "\n")


def main():
    """Main entry point for wearable application"""
    parser = argparse.ArgumentParser(
        description="Wearable Pedestrian Navigation System"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Camera index or video file path"
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["smart_glasses", "body_camera", "headset", "raspberry_pi"],
        default=config.DEVICE_TYPE,
        help="Wearable device type"
    )
    
    args = parser.parse_args()
    
    # Convert camera index to int if numeric
    source = int(args.source) if args.source.isdigit() else args.source
    
    # Update device type if specified
    if args.device != config.DEVICE_TYPE:
        config.DEVICE_TYPE = args.device
        config.ACTIVE_PROFILE = config.DEVICE_PROFILES[args.device]
        print(f"🔄 Switched to device profile: {args.device}")
    
    # Create and run wearable system
    system = WearableNavigationSystem(source=source)
    system.run()


if __name__ == "__main__":
    main()
