# Demo Script for Pedestrian Navigation System
# Quick test with sample video or webcam

"""
Demo script to showcase the system's capabilities
"""

import sys
import os

# Ensure the main module can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import PedestrianNavigationSystem

def run_demo():
    """Run a quick demo"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   INTELLIGENT PEDESTRIAN NAVIGATION SYSTEM - DEMO         ║
    ║   SAITR02 Hackathon Project                               ║
    ╚════════════════════════════════════════════════════════════╝
    
    This demo will showcase:
    ✓ Real-time hazard detection (stairs, potholes, curbs)
    ✓ Intelligent proximity estimation
    ✓ Priority-based audio warnings
    ✓ Sidewalk edge detection
    
    The system will use your webcam by default.
    """)
    
    input("Press ENTER to start the demo...")
    
    try:
        # Create system with webcam
        system = PedestrianNavigationSystem(
            video_source=0,
            confidence=0.4,  # Lower threshold for demo
            debug=True       # Show all debug info
        )
        
        system.run()
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your webcam is connected and not in use")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Try running: python main.py --source 0")
        sys.exit(1)

if __name__ == '__main__':
    run_demo()
