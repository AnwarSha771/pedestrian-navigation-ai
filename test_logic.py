"""
Quick Logic Test - Verify core algorithms work without camera/hardware
"""

import sys
import os
sys.path.insert(0, 'src')

def test_proximity_logic():
    """Test proximity estimation logic"""
    print("Testing proximity estimation...")
    
    from proximity import ProximityEstimator
    
    estimator = ProximityEstimator(1280, 720)
    
    # Test case 1: Close object (large bbox, bottom of frame)
    bbox_close = [500, 600, 700, 700]  # Large box at bottom
    category, distance = estimator.calculate_distance_category(bbox_close)
    print(f"  Close object: {category} at {distance}m")
    assert category == "immediate", "Should detect as immediate"
    
    # Test case 2: Far object (small bbox, top of frame)
    bbox_far = [600, 100, 650, 150]  # Small box at top
    category, distance = estimator.calculate_distance_category(bbox_far)
    print(f"  Far object: {category} at {distance}m")
    assert category == "far", "Should detect as far"
    
    print("  ✓ Proximity logic works!")
    return True

def test_threat_scoring():
    """Test threat scoring algorithm"""
    print("\nTesting threat scoring...")
    
    from proximity import ProximityEstimator
    
    estimator = ProximityEstimator(1280, 720)
    
    # Mock detection
    detection = {
        'class_name': 'pothole',
        'confidence': 0.85,
        'bbox': [500, 600, 700, 700],
        'center': (600, 650),
        'priority': 5
    }
    
    analyzed = estimator.analyze_detection(detection)
    
    print(f"  Object: {analyzed['class_name']}")
    print(f"  Distance: {analyzed['distance_category']} ({analyzed['distance_m']}m)")
    print(f"  Direction: {analyzed['direction_phrase']}")
    print(f"  Threat Score: {analyzed['threat_score']}/100")
    
    assert analyzed['threat_score'] > 50, "High priority close object should have high threat"
    print("  ✓ Threat scoring works!")
    return True

def test_audio_message_generation():
    """Test audio message generation"""
    print("\nTesting audio message generation...")
    
    from audio_feedback import AudioFeedback
    
    audio = AudioFeedback(enabled=False)  # Disabled to avoid actual speech
    
    detection = {
        'class_name': 'pothole',
        'distance_m': 2.5,
        'distance_category': 'near',
        'direction_phrase': 'directly ahead'
    }
    
    message = audio.generate_warning_message(detection)
    print(f"  Generated message: '{message}'")
    
    assert 'pothole' in message.lower(), "Should mention object type"
    assert 'ahead' in message.lower(), "Should mention direction"
    print("  ✓ Audio message generation works!")
    return True

def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    import config
    
    print(f"  Confidence threshold: {config.CONFIDENCE_THRESHOLD}")
    print(f"  Priority levels defined: {len(config.PRIORITY_LEVELS)}")
    print(f"  Distance thresholds: {len(config.DISTANCE_THRESHOLDS)}")
    
    assert hasattr(config, 'CONFIDENCE_THRESHOLD'), "Config should have CONFIDENCE_THRESHOLD"
    assert hasattr(config, 'PRIORITY_LEVELS'), "Config should have PRIORITY_LEVELS"
    print("  ✓ Configuration loads correctly!")
    return True

def main():
    print("="*60)
    print("PEDESTRIAN NAVIGATION - LOGIC TEST")
    print("="*60)
    print("\nTesting core algorithms WITHOUT camera/hardware...\n")
    
    results = {}
    
    try:
        results['Configuration'] = test_configuration()
    except Exception as e:
        print(f"  ✗ Configuration failed: {e}")
        results['Configuration'] = False
    
    try:
        results['Proximity Logic'] = test_proximity_logic()
    except Exception as e:
        print(f"  ✗ Proximity logic failed: {e}")
        results['Proximity Logic'] = False
    
    try:
        results['Threat Scoring'] = test_threat_scoring()
    except Exception as e:
        print(f"  ✗ Threat scoring failed: {e}")
        results['Threat Scoring'] = False
    
    try:
        results['Audio Messages'] = test_audio_message_generation()
    except Exception as e:
        print(f"  ✗ Audio generation failed: {e}")
        results['Audio Messages'] = False
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("="*60)
    
    if all(results.values()):
        print("\n✅ All logic tests passed! Core algorithms work correctly.")
        print("\nTo test full system with camera:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run: python demo.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check error messages above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
