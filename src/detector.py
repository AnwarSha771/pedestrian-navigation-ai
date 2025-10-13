"""
Hazard Detector Module
Uses YOLOv8 for real-time detection of urban obstacles and hazards
"""

import cv2
import numpy as np
from ultralytics import YOLO
import torch
from typing import List, Dict, Tuple
import config


class HazardDetector:
    """Detects urban hazards using YOLOv8 object detection"""
    
    def __init__(self, model_path: str = None, device: str = None):
        """
        Initialize the hazard detector
        
        Args:
            model_path: Path to YOLO model weights
            device: 'cuda' or 'cpu' (auto-detects if None)
        """
        self.model_path = model_path or config.MODEL_PATH
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        
        print(f"Loading YOLOv8 model from {self.model_path}...")
        print(f"Using device: {self.device}")
        
        # Load YOLOv8 model
        self.model = YOLO(self.model_path)
        self.model.to(self.device)
        
        # Mapping of COCO classes to our hazard categories
        self.coco_hazard_mapping = {
            'person': 'person',
            'bicycle': 'bicycle',
            'car': 'car',
            'motorcycle': 'motorcycle',
            'bus': 'car',
            'truck': 'car',
            'chair': 'obstacle',
            'bench': 'obstacle',
            'potted plant': 'obstacle',
            'fire hydrant': 'obstacle',
            'stop sign': 'sign',
            'parking meter': 'obstacle',
            'backpack': 'obstacle',
            'suitcase': 'obstacle'
        }
        
        print("✓ Hazard detector initialized successfully")
    
    def detect(self, frame: np.ndarray, confidence_threshold: float = None) -> List[Dict]:
        """
        Detect hazards in a frame
        
        Args:
            frame: Input image (BGR format)
            confidence_threshold: Minimum confidence for detections
            
        Returns:
            List of detection dictionaries with keys:
                - class_name: Name of detected class
                - confidence: Detection confidence (0-1)
                - bbox: [x1, y1, x2, y2] bounding box coordinates
                - center: (x, y) center point of bbox
        """
        confidence_threshold = confidence_threshold or config.CONFIDENCE_THRESHOLD
        
        # Run inference
        results = self.model(frame, 
                           conf=confidence_threshold,
                           iou=config.IOU_THRESHOLD,
                           max_det=config.MAX_DETECTIONS,
                           verbose=False)
        
        detections = []
        
        # Process results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Extract box information
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                
                # Map COCO classes to hazard categories
                hazard_type = self.coco_hazard_mapping.get(class_name, class_name)
                
                # Calculate center point
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                
                detection = {
                    'class_name': hazard_type,
                    'original_class': class_name,
                    'confidence': confidence,
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'center': (center_x, center_y),
                    'priority': config.PRIORITY_LEVELS.get(hazard_type, 
                                                          config.PRIORITY_LEVELS['default'])
                }
                
                detections.append(detection)
        
        return detections
    
    def detect_custom_hazards(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect custom hazards using image processing techniques
        This is a fallback/supplement to ML detection for stairs, curbs, potholes
        
        Args:
            frame: Input image (BGR format)
            
        Returns:
            List of detection dictionaries (same format as detect())
        """
        detections = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect potential stairs/steps using horizontal line detection
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                               minLineLength=100, maxLineGap=10)
        
        if lines is not None:
            # Group horizontal lines that could indicate stairs
            horizontal_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
                if angle < 15 or angle > 165:  # Nearly horizontal
                    horizontal_lines.append((x1, y1, x2, y2))
            
            # If multiple horizontal lines in lower part of frame, likely stairs
            if len(horizontal_lines) >= 3:
                # Create bounding box around detected lines
                y_coords = [y for _, y, _, _ in horizontal_lines]
                x_coords = [x for x, _, _, _ in horizontal_lines] + [x for _, _, x, _ in horizontal_lines]
                
                if y_coords and x_coords:
                    y_min, y_max = min(y_coords), max(y_coords)
                    x_min, x_max = min(x_coords), max(x_coords)
                    
                    # Only consider if in lower half of frame
                    if y_min > frame.shape[0] * 0.3:
                        detection = {
                            'class_name': 'stairs',
                            'original_class': 'stairs_detected',
                            'confidence': 0.6,
                            'bbox': [x_min, y_min, x_max, y_max],
                            'center': ((x_min + x_max) // 2, (y_min + y_max) // 2),
                            'priority': config.PRIORITY_LEVELS.get('stairs', 4)
                        }
                        detections.append(detection)
        
        # Detect dark spots (potential potholes/manholes)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours of dark regions
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            # Filter by size (must be significant but not entire frame)
            if 500 < area < frame.shape[0] * frame.shape[1] * 0.1:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Must be in lower 2/3 of frame
                if y > frame.shape[0] * 0.33:
                    # Check if roughly circular (pothole/manhole indicator)
                    circularity = 4 * np.pi * area / (cv2.arcLength(contour, True) ** 2)
                    
                    if circularity > 0.5:  # Reasonably circular
                        detection = {
                            'class_name': 'pothole',
                            'original_class': 'pothole_detected',
                            'confidence': min(0.5 + circularity * 0.3, 0.8),
                            'bbox': [x, y, x + w, y + h],
                            'center': (x + w//2, y + h//2),
                            'priority': config.PRIORITY_LEVELS.get('pothole', 5)
                        }
                        detections.append(detection)
        
        return detections
    
    def combine_detections(self, ml_detections: List[Dict], 
                          cv_detections: List[Dict]) -> List[Dict]:
        """
        Combine ML and computer vision detections, removing duplicates
        
        Args:
            ml_detections: Detections from YOLO model
            cv_detections: Detections from image processing
            
        Returns:
            Combined list of unique detections
        """
        all_detections = ml_detections.copy()
        
        for cv_det in cv_detections:
            # Check if this detection overlaps significantly with any ML detection
            is_duplicate = False
            cv_bbox = cv_det['bbox']
            
            for ml_det in ml_detections:
                ml_bbox = ml_det['bbox']
                
                # Calculate IoU (Intersection over Union)
                x1 = max(cv_bbox[0], ml_bbox[0])
                y1 = max(cv_bbox[1], ml_bbox[1])
                x2 = min(cv_bbox[2], ml_bbox[2])
                y2 = min(cv_bbox[3], ml_bbox[3])
                
                if x2 > x1 and y2 > y1:
                    intersection = (x2 - x1) * (y2 - y1)
                    cv_area = (cv_bbox[2] - cv_bbox[0]) * (cv_bbox[3] - cv_bbox[1])
                    ml_area = (ml_bbox[2] - ml_bbox[0]) * (ml_bbox[3] - ml_bbox[1])
                    union = cv_area + ml_area - intersection
                    iou = intersection / union if union > 0 else 0
                    
                    if iou > 0.3:  # Significant overlap
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                all_detections.append(cv_det)
        
        return all_detections
