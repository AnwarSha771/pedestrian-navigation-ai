"""
Termux-Optimized Pedestrian Navigation System
Runs directly on Android phone (OnePlus 11R tested)
Uses Termux environment with camera access
"""

import os
import sys
import cv2
import time
import subprocess
import numpy as np
from pathlib import Path
from datetime import datetime
import tempfile

# Check if running in Termux
IS_TERMUX = os.path.exists('/data/data/com.termux')

if IS_TERMUX:
    print("🤖 Running in Termux environment")
else:
    print("⚠️  Warning: Not detected as Termux environment")

# Import core modules
try:
    from src.detector import HazardDetector
    from src.proximity import ProximityEstimator
    from src.utils import draw_detection_box, draw_status_panel
except ImportError:
    print("⚠️  Core modules not found. Make sure you're in project directory")
    print("Run: cd ~/pedestrian-navigation-ai")
    sys.exit(1)


class TermuxNavigationSystem:
    """Pedestrian navigation optimized for Termux on Android"""
    
    def __init__(self, use_video_file=None):
        """
        Initialize Termux navigation system
        
        Args:
            use_video_file: Path to video file (None = use camera)
        """
        print("\n" + "="*60)
        print("📱 TERMUX PEDESTRIAN NAVIGATION SYSTEM")
        print("   Running on Android via Termux")
        print("="*60)
        
        self.use_video_file = use_video_file
        self.temp_dir = Path(tempfile.gettempdir()) / "termux_nav"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Mobile-optimized settings
        self.frame_width = 320
        self.frame_height = 240
        self.target_fps = 10  # Lower FPS for mobile CPU
        self.confidence_threshold = 0.5
        
        # Initialize AI components
        print("\n🔧 Initializing AI components (mobile optimized)...")
        self.detector = HazardDetector()
        self.proximity_estimator = ProximityEstimator()
        
        # Audio disabled in Termux (no TTS support)
        self.audio_enabled = False
        print("🔇 Audio warnings disabled (Termux limitation)")
        
        # Statistics
        self.frame_count = 0
        self.detection_count = 0
        self.fps_start = time.time()
        self.current_fps = 0
        
        # Camera setup
        if use_video_file:
            self.camera_mode = "video"
            self.cap = cv2.VideoCapture(use_video_file)
            print(f"📹 Using video file: {use_video_file}")
        else:
            self.camera_mode = "termux-api"
            self.cap = None
            print("📷 Using Termux camera API")
            self._check_termux_api()
        
        print("\n✅ System initialized!")
        print(f"   Resolution: {self.frame_width}x{self.frame_height}")
        print(f"   Target FPS: {self.target_fps}")
        print(f"   Camera mode: {self.camera_mode}")
    
    def _check_termux_api(self):
        """Check if Termux:API is installed"""
        try:
            result = subprocess.run(
                ['termux-camera-info'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print("✅ Termux:API detected")
                
                # Parse camera info
                import json
                cameras = json.loads(result.stdout)
                print(f"📷 Found {len(cameras)} camera(s)")
                for cam_id, info in cameras.items():
                    facing = info.get('facing', 'unknown')
                    print(f"   Camera {cam_id}: {facing}")
            else:
                print("⚠️  Termux:API not responding")
                print("Install from: https://f-droid.org/packages/com.termux.api/")
        
        except FileNotFoundError:
            print("❌ Termux:API not installed!")
            print("\nInstall it:")
            print("1. Install Termux:API app from F-Droid")
            print("2. Run: pkg install termux-api")
            sys.exit(1)
        
        except Exception as e:
            print(f"⚠️  Camera check failed: {e}")
    
    def capture_frame_termux(self):
        """Capture frame using Termux camera API"""
        photo_path = self.temp_dir / f"frame_{int(time.time()*1000)}.jpg"
        
        try:
            # Capture photo using termux-camera-photo
            # -c 0 = back camera, -c 1 = front camera
            result = subprocess.run(
                ['termux-camera-photo', '-c', '0', str(photo_path)],
                capture_output=True,
                timeout=3
            )
            
            if result.returncode != 0:
                print(f"⚠️  Camera capture failed: {result.stderr}")
                return None
            
            # Wait for file to be written
            time.sleep(0.1)
            
            if not photo_path.exists():
                print("⚠️  Photo file not created")
                return None
            
            # Read image
            frame = cv2.imread(str(photo_path))
            
            # Delete temporary file
            try:
                photo_path.unlink()
            except:
                pass
            
            if frame is None:
                print("⚠️  Failed to read captured photo")
                return None
            
            # Resize to target resolution
            frame = cv2.resize(frame, (self.frame_width, self.frame_height))
            
            return frame
        
        except subprocess.TimeoutExpired:
            print("⚠️  Camera timeout")
            return None
        
        except Exception as e:
            print(f"⚠️  Capture error: {e}")
            return None
    
    def capture_frame_video(self):
        """Capture frame from video file"""
        if self.cap is None:
            return None
        
        ret, frame = self.cap.read()
        
        if not ret:
            return None
        
        # Resize to target resolution
        frame = cv2.resize(frame, (self.frame_width, self.frame_height))
        
        return frame
    
    def capture_frame(self):
        """Capture frame from appropriate source"""
        if self.camera_mode == "termux-api":
            return self.capture_frame_termux()
        else:
            return self.capture_frame_video()
    
    def process_frame(self, frame):
        """Process frame and detect hazards"""
        if frame is None:
            return None
        
        self.frame_count += 1
        
        # Run detection
        detections = self.detector.detect(frame)
        
        # Analyze proximity
        analyzed_detections = []
        for det in detections:
            analyzed = self.proximity_estimator.analyze_detection(det, frame.shape)
            analyzed_detections.append(analyzed)
        
        # Get most critical
        critical = self.proximity_estimator.filter_most_critical(analyzed_detections)
        
        if critical:
            self.detection_count += 1
            
            # Print warning to terminal (since no audio)
            obj_class = critical.get('class', 'unknown')
            distance = critical.get('distance_category', 'unknown')
            direction = critical.get('direction', 'unknown')
            threat = critical.get('threat_score', 0)
            
            print(f"⚠️  [{obj_class.upper()}] {distance} - {direction} (threat: {threat}/100)")
        
        # Draw detections on frame
        for det in analyzed_detections:
            draw_detection_box(frame, det)
        
        # Update FPS
        self._update_fps()
        
        # Draw status
        status_text = f"FPS: {self.current_fps:.1f} | Detections: {self.detection_count}"
        cv2.putText(frame, status_text, (5, 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        return frame
    
    def _update_fps(self):
        """Calculate FPS"""
        elapsed = time.time() - self.fps_start
        if elapsed > 1.0:
            self.current_fps = self.frame_count / elapsed
            self.frame_count = 0
            self.fps_start = time.time()
    
    def save_frame(self, frame, filename="output.jpg"):
        """Save frame to storage"""
        output_path = Path.home() / "storage" / "pictures" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cv2.imwrite(str(output_path), frame)
        print(f"💾 Saved: {output_path}")
    
    def run_continuous(self, duration=60):
        """
        Run continuous detection for specified duration
        
        Args:
            duration: How many seconds to run (default 60)
        """
        print("\n" + "-"*60)
        print(f"⚡ Starting detection loop ({duration} seconds)...")
        print("   Processing frames from camera")
        print("   Press Ctrl+C to stop early")
        print("-"*60 + "\n")
        
        start_time = time.time()
        last_save_time = start_time
        save_interval = 5  # Save frame every 5 seconds
        
        try:
            while (time.time() - start_time) < duration:
                # Capture frame
                frame = self.capture_frame()
                
                if frame is None:
                    print("⚠️  Failed to capture frame, retrying...")
                    time.sleep(0.5)
                    continue
                
                # Process frame
                processed = self.process_frame(frame)
                
                # Save frame periodically
                current_time = time.time()
                if current_time - last_save_time >= save_interval:
                    timestamp = datetime.now().strftime("%H%M%S")
                    self.save_frame(processed, f"nav_{timestamp}.jpg")
                    last_save_time = current_time
                
                # Control frame rate
                time.sleep(1.0 / self.target_fps)
        
        except KeyboardInterrupt:
            print("\n\n⏹  Stopped by user")
        
        finally:
            self.cleanup()
        
        elapsed = time.time() - start_time
        print(f"\n📊 Session complete: {elapsed:.1f}s, {self.detection_count} detections")
    
    def run_single_shot(self):
        """Capture and process single frame"""
        print("\n📸 Taking single photo...")
        
        frame = self.capture_frame()
        
        if frame is None:
            print("❌ Failed to capture photo")
            return
        
        print("✅ Photo captured, processing...")
        
        processed = self.process_frame(frame)
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"detection_{timestamp}.jpg"
        self.save_frame(processed, output_file)
        
        print(f"\n✅ Done! Check: ~/storage/pictures/{output_file}")
    
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up...")
        
        if self.cap:
            self.cap.release()
        
        # Clean temp directory
        try:
            for f in self.temp_dir.glob("*.jpg"):
                f.unlink()
        except:
            pass
        
        print("✅ Cleanup complete")


def main():
    """Main entry point for Termux version"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pedestrian Navigation for Termux/Android"
    )
    parser.add_argument(
        "--mode",
        choices=["continuous", "single"],
        default="continuous",
        help="Detection mode (continuous or single shot)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration in seconds (for continuous mode)"
    )
    parser.add_argument(
        "--video",
        type=str,
        help="Use video file instead of camera"
    )
    
    args = parser.parse_args()
    
    # Create system
    system = TermuxNavigationSystem(use_video_file=args.video)
    
    # Run in selected mode
    if args.mode == "single":
        system.run_single_shot()
    else:
        system.run_continuous(duration=args.duration)


if __name__ == "__main__":
    main()
