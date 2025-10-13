"""
Audio Feedback Module
Provides intelligent text-to-speech warnings based on detected hazards
"""

import time
import threading
from typing import Dict, Optional
import config

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("Warning: pyttsx3 not available, audio feedback disabled")


class AudioFeedback:
    """Manages intelligent audio warnings for detected hazards"""
    
    def __init__(self, enabled: bool = True, use_offline: bool = True):
        """
        Initialize audio feedback system
        
        Args:
            enabled: Whether audio is enabled
            use_offline: Use offline TTS (pyttsx3) vs online (gTTS)
        """
        self.enabled = enabled and config.AUDIO_ENABLED
        self.use_offline = use_offline and PYTTSX3_AVAILABLE
        
        # TTS engine
        self.engine = None
        if self.enabled and self.use_offline:
            try:
                self.engine = pyttsx3.init()
                # Configure voice properties
                self.engine.setProperty('rate', 175)  # Speed (words per minute)
                self.engine.setProperty('volume', 0.9)  # Volume (0-1)
                
                # Try to set a clear voice
                voices = self.engine.getProperty('voices')
                if voices:
                    # Prefer female voice (often clearer) or first available
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.engine.setProperty('voice', voice.id)
                            break
                
                print("✓ Offline TTS engine initialized")
            except Exception as e:
                print(f"Warning: Could not initialize TTS engine: {e}")
                self.enabled = False
        
        # Announcement tracking (to avoid spam)
        self.last_announcement_time = {}
        self.last_announced_object = None
        self.cooldown = config.ANNOUNCEMENT_COOLDOWN
        
        # Speaking thread
        self.speaking = False
        self.speak_thread = None
    
    def should_announce(self, detection: Dict) -> bool:
        """
        Determine if a detection should be announced based on priority and timing
        
        Args:
            detection: Detection dictionary with priority and threat info
            
        Returns:
            True if should announce, False otherwise
        """
        if not self.enabled:
            return False
        
        # Check minimum priority
        if detection.get('priority', 0) < config.MIN_PRIORITY_FOR_AUDIO:
            return False
        
        # Create unique key for this detection
        obj_key = f"{detection['class_name']}_{detection.get('direction', 'center')}"
        
        # Check cooldown
        current_time = time.time()
        last_time = self.last_announcement_time.get(obj_key, 0)
        
        if current_time - last_time < self.cooldown:
            return False
        
        # Update last announcement time
        self.last_announcement_time[obj_key] = current_time
        
        return True
    
    def generate_warning_message(self, detection: Dict) -> str:
        """
        Generate natural language warning message
        
        Args:
            detection: Detection with proximity and threat analysis
            
        Returns:
            Warning message string
        """
        class_name = detection['class_name']
        distance_m = detection.get('distance_m', 5.0)
        distance_category = detection.get('distance_category', 'near')
        direction_phrase = detection.get('direction_phrase', 'ahead')
        
        # Format class name for speech
        class_labels = {
            'pothole': 'pothole',
            'manhole': 'manhole cover',
            'stairs': 'stairs',
            'curb': 'curb',
            'step': 'step',
            'gap': 'gap',
            'broken_pavement': 'broken pavement',
            'person': 'pedestrian',
            'bicycle': 'bicycle',
            'car': 'vehicle',
            'obstacle': 'obstacle'
        }
        
        object_label = class_labels.get(class_name, class_name)
        
        # Build message based on urgency
        if distance_category == 'immediate':
            urgency = "DANGER"
            distance_phrase = f"{int(distance_m)} meter" + ("s" if distance_m > 1 else "")
            message = f"{urgency}: {object_label} {direction_phrase}, {distance_phrase}!"
        elif distance_category == 'near':
            urgency = "Caution"
            distance_phrase = f"{int(distance_m)} meters"
            message = f"{urgency}: {object_label} {direction_phrase}, {distance_phrase}."
        else:
            urgency = "Notice"
            message = f"{urgency}: {object_label} {direction_phrase}."
        
        return message
    
    def announce(self, detection: Dict, force: bool = False):
        """
        Announce a detection via TTS
        
        Args:
            detection: Detection to announce
            force: Force announcement even if cooldown not expired
        """
        if not self.enabled and not force:
            return
        
        if not force and not self.should_announce(detection):
            return
        
        message = self.generate_warning_message(detection)
        self._speak(message)
    
    def announce_clear_path(self, clearance_distance: float):
        """
        Announce that path is clear
        
        Args:
            clearance_distance: Distance in meters that path is clear
        """
        if not self.enabled:
            return
        
        # Only announce clear path occasionally
        if self.last_announced_object == 'clear':
            current_time = time.time()
            if current_time - self.last_announcement_time.get('clear', 0) < self.cooldown * 2:
                return
        
        distance_text = f"{int(clearance_distance)} meters" if clearance_distance < 15 else "ahead"
        message = f"Path clear for {distance_text}."
        
        self.last_announced_object = 'clear'
        self.last_announcement_time['clear'] = time.time()
        
        self._speak(message)
    
    def announce_edge_warning(self, edge_side: str):
        """
        Announce sidewalk edge warning
        
        Args:
            edge_side: 'left' or 'right'
        """
        if not self.enabled:
            return
        
        obj_key = f"edge_{edge_side}"
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_announcement_time.get(obj_key, 0) < self.cooldown:
            return
        
        message = f"Caution: Approaching sidewalk edge on {edge_side}."
        
        self.last_announcement_time[obj_key] = current_time
        self._speak(message)
    
    def _speak(self, text: str):
        """
        Internal method to speak text using TTS
        
        Args:
            text: Text to speak
        """
        if not self.engine:
            print(f"[AUDIO] {text}")  # Fallback to print
            return
        
        # Speak in separate thread to avoid blocking
        if self.speaking:
            return  # Skip if already speaking
        
        def speak_thread():
            self.speaking = True
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.speaking = False
        
        self.speak_thread = threading.Thread(target=speak_thread, daemon=True)
        self.speak_thread.start()
    
    def toggle(self) -> bool:
        """
        Toggle audio on/off
        
        Returns:
            New state (True = enabled, False = disabled)
        """
        self.enabled = not self.enabled
        return self.enabled
    
    def cleanup(self):
        """Clean up TTS engine"""
        if self.speak_thread and self.speak_thread.is_alive():
            self.speak_thread.join(timeout=1.0)
        
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass


class AudioManager:
    """Manages audio feedback with intelligent filtering"""
    
    def __init__(self):
        self.audio = AudioFeedback()
        self.last_critical_detection = None
        self.path_clear_count = 0
    
    def process_frame_detections(self, detections: list, 
                                 path_clear: bool, 
                                 clearance_distance: float):
        """
        Process all detections for a frame and make intelligent announcement
        
        Args:
            detections: List of analyzed detections
            path_clear: Whether center path is clear
            clearance_distance: Distance path is clear (meters)
        """
        if not detections or path_clear:
            # Path is clear
            self.path_clear_count += 1
            
            # Only announce clear path every 30 frames (~1 second at 30fps)
            if self.path_clear_count >= 30:
                self.audio.announce_clear_path(clearance_distance)
                self.path_clear_count = 0
            
            self.last_critical_detection = None
            return
        
        self.path_clear_count = 0
        
        # Filter detections by minimum priority
        priority_detections = [d for d in detections 
                              if d.get('priority', 0) >= config.MIN_PRIORITY_FOR_AUDIO]
        
        if not priority_detections:
            return
        
        # Find most critical detection
        most_critical = max(priority_detections, key=lambda d: d.get('threat_score', 0))
        
        # Only announce if different from last or threat increased
        should_announce = False
        
        if self.last_critical_detection is None:
            should_announce = True
        else:
            # Check if it's a different object or same object but closer/higher threat
            same_object = (most_critical['class_name'] == self.last_critical_detection['class_name'] and
                          most_critical.get('direction') == self.last_critical_detection.get('direction'))
            
            if not same_object:
                should_announce = True
            elif most_critical.get('threat_score', 0) > self.last_critical_detection.get('threat_score', 0) + 10:
                should_announce = True  # Threat increased significantly
        
        if should_announce:
            self.audio.announce(most_critical)
            self.last_critical_detection = most_critical
    
    def announce_edge(self, edge_side: str):
        """Announce sidewalk edge warning"""
        self.audio.announce_edge_warning(edge_side)
    
    def toggle_audio(self) -> bool:
        """Toggle audio on/off"""
        return self.audio.toggle()
    
    def cleanup(self):
        """Clean up audio resources"""
        self.audio.cleanup()
