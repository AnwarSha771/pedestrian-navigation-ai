"""
Utility functions for the Pedestrian Navigation System
"""

import cv2
import numpy as np
from typing import Tuple
import config


def draw_detection_box(frame: np.ndarray, 
                       detection: dict,
                       show_label: bool = True,
                       show_confidence: bool = True,
                       show_distance: bool = True) -> np.ndarray:
    """
    Draw bounding box and label for a detection
    
    Args:
        frame: Input frame
        detection: Detection dictionary with bbox, class_name, etc.
        show_label: Whether to show class label
        show_confidence: Whether to show confidence score
        show_distance: Whether to show distance estimate
        
    Returns:
        Frame with annotation drawn
    """
    bbox = detection['bbox']
    x1, y1, x2, y2 = bbox
    
    # Get color based on distance category
    distance_category = detection.get('distance_category', 'far')
    color = config.COLORS.get(distance_category, config.COLORS['far'])
    
    # Draw bounding box
    thickness = 3 if distance_category == 'immediate' else 2
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Build label text
    label_parts = []
    
    if show_label:
        class_name = detection['class_name'].replace('_', ' ').title()
        label_parts.append(class_name)
    
    if show_confidence:
        confidence = detection.get('confidence', 0)
        label_parts.append(f"{confidence:.0%}")
    
    if show_distance:
        distance_m = detection.get('distance_m', 0)
        label_parts.append(f"{distance_m:.1f}m")
    
    label = " | ".join(label_parts)
    
    # Draw label background
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 2
    
    (label_width, label_height), baseline = cv2.getTextSize(
        label, font, font_scale, font_thickness
    )
    
    # Position label above box, or below if too close to top
    label_y = y1 - 10 if y1 - 10 > label_height else y1 + label_height + 10
    
    # Draw background rectangle
    cv2.rectangle(frame,
                 (x1, label_y - label_height - 5),
                 (x1 + label_width + 10, label_y + baseline),
                 color, -1)
    
    # Draw text
    cv2.putText(frame, label,
               (x1 + 5, label_y - 5),
               font, font_scale,
               config.COLORS['text'], font_thickness)
    
    return frame


def draw_fps(frame: np.ndarray, fps: float) -> np.ndarray:
    """
    Draw FPS counter on frame
    
    Args:
        frame: Input frame
        fps: Current FPS
        
    Returns:
        Frame with FPS drawn
    """
    text = f"FPS: {fps:.1f}"
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(
        text, font, font_scale, font_thickness
    )
    
    # Position in top-right corner
    x = frame.shape[1] - text_width - 10
    y = text_height + 10
    
    # Draw background
    cv2.rectangle(frame,
                 (x - 5, y - text_height - 5),
                 (x + text_width + 5, y + baseline),
                 (0, 0, 0), -1)
    
    # Draw text
    cv2.putText(frame, text, (x, y),
               font, font_scale, (0, 255, 0), font_thickness)
    
    return frame


def draw_status_panel(frame: np.ndarray, 
                     status_info: dict) -> np.ndarray:
    """
    Draw status information panel
    
    Args:
        frame: Input frame
        status_info: Dictionary with status information:
            - detections_count: Number of detections
            - audio_enabled: Whether audio is on
            - path_clear: Whether path is clear
            - clearance_distance: Distance path is clear
            
    Returns:
        Frame with status panel
    """
    panel_height = 100
    panel_width = 300
    margin = 10
    
    # Position in top-left
    x = margin
    y = margin
    
    # Draw semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay,
                 (x, y),
                 (x + panel_width, y + panel_height),
                 (0, 0, 0), -1)
    frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
    
    # Draw border
    cv2.rectangle(frame,
                 (x, y),
                 (x + panel_width, y + panel_height),
                 (255, 255, 255), 2)
    
    # Draw status text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    line_height = 20
    
    y_offset = y + 25
    
    # Detections count
    text = f"Detections: {status_info.get('detections_count', 0)}"
    cv2.putText(frame, text, (x + 10, y_offset),
               font, font_scale, (255, 255, 255), font_thickness)
    y_offset += line_height
    
    # Audio status
    audio_status = "ON" if status_info.get('audio_enabled', False) else "OFF"
    audio_color = (0, 255, 0) if status_info.get('audio_enabled', False) else (0, 0, 255)
    text = f"Audio: {audio_status}"
    cv2.putText(frame, text, (x + 10, y_offset),
               font, font_scale, audio_color, font_thickness)
    y_offset += line_height
    
    # Path status
    path_clear = status_info.get('path_clear', False)
    if path_clear:
        clearance = status_info.get('clearance_distance', 0)
        text = f"Path: CLEAR ({clearance:.1f}m)"
        color = (0, 255, 0)
    else:
        text = "Path: OBSTRUCTED"
        color = (0, 0, 255)
    
    cv2.putText(frame, text, (x + 10, y_offset),
               font, font_scale, color, font_thickness)
    
    return frame


def draw_help_text(frame: np.ndarray) -> np.ndarray:
    """
    Draw keyboard controls help text
    
    Args:
        frame: Input frame
        
    Returns:
        Frame with help text
    """
    help_text = [
        "Controls:",
        "Q - Quit",
        "S - Toggle Sound",
        "D - Toggle Debug",
        "P - Pause"
    ]
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    font_thickness = 1
    line_height = 18
    
    # Position in bottom-left
    x = 10
    y = frame.shape[0] - len(help_text) * line_height - 10
    
    for i, text in enumerate(help_text):
        y_pos = y + i * line_height
        
        # Draw text shadow for readability
        cv2.putText(frame, text, (x + 1, y_pos + 1),
                   font, font_scale, (0, 0, 0), font_thickness + 1)
        
        # Draw text
        cv2.putText(frame, text, (x, y_pos),
                   font, font_scale, (255, 255, 255), font_thickness)
    
    return frame


def calculate_fps(prev_time: float, current_time: float) -> float:
    """
    Calculate FPS based on time difference
    
    Args:
        prev_time: Previous frame time
        current_time: Current frame time
        
    Returns:
        FPS value
    """
    time_diff = current_time - prev_time
    if time_diff > 0:
        return 1.0 / time_diff
    return 0.0


def resize_frame(frame: np.ndarray, 
                target_width: int = None,
                target_height: int = None) -> np.ndarray:
    """
    Resize frame while maintaining aspect ratio
    
    Args:
        frame: Input frame
        target_width: Target width (optional)
        target_height: Target height (optional)
        
    Returns:
        Resized frame
    """
    height, width = frame.shape[:2]
    
    if target_width is None and target_height is None:
        return frame
    
    if target_width is None:
        # Calculate width based on height
        aspect_ratio = width / height
        target_width = int(target_height * aspect_ratio)
    elif target_height is None:
        # Calculate height based on width
        aspect_ratio = height / width
        target_height = int(target_width * aspect_ratio)
    
    resized = cv2.resize(frame, (target_width, target_height))
    return resized


def create_demo_frame(frame_size: Tuple[int, int] = (1280, 720)) -> np.ndarray:
    """
    Create a demo frame for testing (simulated urban scene)
    
    Args:
        frame_size: (width, height) of frame
        
    Returns:
        Generated demo frame
    """
    width, height = frame_size
    frame = np.ones((height, width, 3), dtype=np.uint8) * 128
    
    # Draw "ground" (lower 2/3 of frame)
    ground_top = height // 3
    frame[ground_top:, :] = [180, 180, 180]  # Light gray sidewalk
    
    # Draw some "obstacles"
    # Dark spot (pothole)
    cv2.circle(frame, (width // 2, int(height * 0.7)), 50, (30, 30, 30), -1)
    
    # Rectangle (person or obstacle)
    cv2.rectangle(frame, 
                 (int(width * 0.3), int(height * 0.4)),
                 (int(width * 0.35), int(height * 0.8)),
                 (100, 100, 150), -1)
    
    return frame


def log_detection(detection: dict):
    """
    Print detection information to console (for debugging)
    
    Args:
        detection: Detection dictionary
    """
    class_name = detection.get('class_name', 'unknown')
    confidence = detection.get('confidence', 0)
    distance_m = detection.get('distance_m', 0)
    distance_category = detection.get('distance_category', 'unknown')
    direction_phrase = detection.get('direction_phrase', 'unknown')
    threat_score = detection.get('threat_score', 0)
    
    print(f"[DETECTION] {class_name.upper()}: "
          f"{distance_category} ({distance_m:.1f}m) "
          f"{direction_phrase} | "
          f"Confidence: {confidence:.0%} | "
          f"Threat: {threat_score}/100")
