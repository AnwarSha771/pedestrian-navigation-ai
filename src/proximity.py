"""
Proximity Estimation Module
Calculates distance and location of detected hazards using bounding box analysis
"""

import numpy as np
from typing import Dict, Tuple
import config


class ProximityEstimator:
    """Estimates proximity of detected objects using computer vision heuristics"""
    
    def __init__(self, frame_width: int = 1280, frame_height: int = 720):
        """
        Initialize proximity estimator
        
        Args:
            frame_width: Width of video frame in pixels
            frame_height: Height of video frame in pixels
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Cache thresholds for performance
        self.immediate_height_px = int(frame_height * config.DISTANCE_THRESHOLDS['immediate']['bbox_height_ratio'])
        self.immediate_bottom_px = int(frame_height * config.DISTANCE_THRESHOLDS['immediate']['bbox_bottom_ratio'])
        self.near_height_px = int(frame_height * config.DISTANCE_THRESHOLDS['near']['bbox_height_ratio'])
        self.near_bottom_px = int(frame_height * config.DISTANCE_THRESHOLDS['near']['bbox_bottom_ratio'])
    
    def calculate_distance_category(self, bbox: list) -> Tuple[str, float]:
        """
        Calculate distance category based on bounding box
        
        Algorithm:
        - Objects lower in frame are closer
        - Larger objects are closer
        - Combination of both provides good approximation
        
        Args:
            bbox: [x1, y1, x2, y2] bounding box coordinates
            
        Returns:
            Tuple of (category: str, estimated_distance_m: float)
            Categories: 'immediate', 'near', 'far'
        """
        x1, y1, x2, y2 = bbox
        
        # Calculate bbox properties
        bbox_height = y2 - y1
        bbox_width = x2 - x1
        bbox_bottom = y2
        bbox_area = bbox_height * bbox_width
        
        # Normalized metrics (0-1)
        height_ratio = bbox_height / self.frame_height
        bottom_ratio = bbox_bottom / self.frame_height
        area_ratio = bbox_area / (self.frame_width * self.frame_height)
        
        # Weighted score (higher = closer)
        # Bottom position is weighted more heavily as it's more reliable
        proximity_score = (bottom_ratio * 0.6) + (height_ratio * 0.3) + (area_ratio * 0.1)
        
        # Determine category
        if (bbox_height > self.immediate_height_px or 
            bbox_bottom > self.immediate_bottom_px or
            proximity_score > 0.7):
            category = 'immediate'
            distance_m = min(proximity_score * 3, 2.0)  # Max 2m for immediate
        elif (bbox_height > self.near_height_px or 
              bbox_bottom > self.near_bottom_px or
              proximity_score > 0.4):
            category = 'near'
            distance_m = 2.0 + (0.7 - proximity_score) * 10  # 2-5m
        else:
            category = 'far'
            distance_m = 5.0 + (0.4 - proximity_score) * 20  # 5-10m
        
        # Clamp distance to reasonable range
        distance_m = max(0.5, min(distance_m, 15.0))
        
        return category, round(distance_m, 1)
    
    def calculate_direction(self, bbox: list) -> str:
        """
        Calculate directional position of object relative to camera
        
        Args:
            bbox: [x1, y1, x2, y2] bounding box coordinates
            
        Returns:
            Direction string: 'center', 'left', 'right', 'far_left', 'far_right'
        """
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) / 2
        frame_center = self.frame_width / 2
        
        # Calculate offset from center
        offset = center_x - frame_center
        offset_ratio = offset / frame_center
        
        # Determine direction
        if abs(offset_ratio) < 0.2:
            return 'center'
        elif offset_ratio < -0.5:
            return 'far_left'
        elif offset_ratio < 0:
            return 'left'
        elif offset_ratio > 0.5:
            return 'far_right'
        else:
            return 'right'
    
    def get_directional_phrase(self, direction: str) -> str:
        """
        Convert direction to natural language phrase
        
        Args:
            direction: Direction string from calculate_direction()
            
        Returns:
            Natural language phrase
        """
        phrases = {
            'center': 'directly ahead',
            'left': 'on the left',
            'right': 'on the right',
            'far_left': 'far left',
            'far_right': 'far right'
        }
        return phrases.get(direction, 'ahead')
    
    def analyze_detection(self, detection: Dict) -> Dict:
        """
        Perform complete proximity analysis on a detection
        
        Args:
            detection: Detection dictionary from HazardDetector
            
        Returns:
            Enhanced detection with proximity information:
                - distance_category: 'immediate', 'near', or 'far'
                - distance_m: Estimated distance in meters
                - direction: Directional position
                - direction_phrase: Natural language direction
                - threat_score: Combined threat assessment (0-100)
        """
        bbox = detection['bbox']
        
        # Calculate distance
        distance_category, distance_m = self.calculate_distance_category(bbox)
        
        # Calculate direction
        direction = self.calculate_direction(bbox)
        direction_phrase = self.get_directional_phrase(direction)
        
        # Calculate threat score
        # Combines: priority (0-5), distance (closer = higher), direction (center = higher)
        priority_score = detection['priority'] * 10  # 0-50
        
        # Distance score (closer = higher)
        if distance_category == 'immediate':
            distance_score = 40
        elif distance_category == 'near':
            distance_score = 25
        else:
            distance_score = 10
        
        # Direction score (center is most threatening)
        direction_scores = {
            'center': 10,
            'left': 7,
            'right': 7,
            'far_left': 3,
            'far_right': 3
        }
        direction_score = direction_scores.get(direction, 5)
        
        threat_score = min(priority_score + distance_score + direction_score, 100)
        
        # Add proximity information to detection
        detection.update({
            'distance_category': distance_category,
            'distance_m': distance_m,
            'direction': direction,
            'direction_phrase': direction_phrase,
            'threat_score': threat_score
        })
        
        return detection
    
    def filter_most_critical(self, detections: list) -> Dict:
        """
        Select the most critical detection from a list
        
        Args:
            detections: List of detections with proximity analysis
            
        Returns:
            Single most critical detection, or None if list is empty
        """
        if not detections:
            return None
        
        # Sort by threat score (highest first)
        sorted_detections = sorted(detections, 
                                  key=lambda d: d['threat_score'], 
                                  reverse=True)
        
        return sorted_detections[0]
    
    def calculate_path_clearance(self, detections: list, 
                                 center_corridor_width: float = 0.4) -> Tuple[bool, float]:
        """
        Calculate if center path is clear for walking
        
        Args:
            detections: List of analyzed detections
            center_corridor_width: Width of center corridor as ratio of frame width (0-1)
            
        Returns:
            Tuple of (is_clear: bool, clearance_distance_m: float)
        """
        # Define center corridor bounds
        left_bound = self.frame_width * (0.5 - center_corridor_width / 2)
        right_bound = self.frame_width * (0.5 + center_corridor_width / 2)
        
        # Check for obstacles in center corridor
        min_distance = 15.0  # Assume clear up to 15m
        path_clear = True
        
        for detection in detections:
            bbox = detection['bbox']
            x1, x2 = bbox[0], bbox[2]
            
            # Check if bbox overlaps with center corridor
            if x2 > left_bound and x1 < right_bound:
                # Object is in center path
                if detection.get('distance_m', 15.0) < min_distance:
                    min_distance = detection['distance_m']
                    path_clear = False
        
        clearance_distance = min_distance if not path_clear else 15.0
        
        return path_clear, clearance_distance
