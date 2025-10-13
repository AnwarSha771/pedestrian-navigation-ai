"""
Sidewalk Edge Detection Module
Detects sidewalk boundaries using color and texture analysis (Shore-lining assist)
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import config


class SidewalkDetector:
    """Detects sidewalk edges to help users stay on safe path"""
    
    def __init__(self, frame_width: int = 1280, frame_height: int = 720):
        """
        Initialize sidewalk edge detector
        
        Args:
            frame_width: Width of video frame
            frame_height: Height of video frame
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Focus on lower portion of frame (where ground is visible)
        self.roi_top = int(frame_height * 0.5)  # Start from middle
        self.roi_bottom = frame_height
        
        # Warning thresholds (as ratio of frame width)
        self.warning_distance = config.EDGE_WARNING_DISTANCE
        
        print("✓ Sidewalk edge detector initialized")
    
    def detect_edges(self, frame: np.ndarray) -> Tuple[Optional[int], Optional[int]]:
        """
        Detect left and right edges of sidewalk
        
        Uses edge detection and color segmentation to find boundaries
        
        Args:
            frame: Input BGR image
            
        Returns:
            Tuple of (left_edge_x, right_edge_x) in pixels, or (None, None) if not found
        """
        # Extract ROI (region of interest - lower half of frame)
        roi = frame[self.roi_top:self.roi_bottom, :]
        
        # Convert to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 
                         config.CANNY_THRESHOLD1, 
                         config.CANNY_THRESHOLD2)
        
        # Find vertical edges (sidewalk boundaries are typically vertical in frame)
        # Use Sobel operator to emphasize vertical edges
        sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobelx = np.uint8(np.absolute(sobelx))
        
        # Combine Canny and Sobel
        combined_edges = cv2.bitwise_or(edges, sobelx)
        
        # Find edges in left and right portions
        left_edge = self._find_edge_in_region(combined_edges, 'left')
        right_edge = self._find_edge_in_region(combined_edges, 'right')
        
        return left_edge, right_edge
    
    def _find_edge_in_region(self, edge_image: np.ndarray, side: str) -> Optional[int]:
        """
        Find edge in left or right portion of frame
        
        Args:
            edge_image: Binary edge image
            side: 'left' or 'right'
            
        Returns:
            X-coordinate of edge, or None if not found
        """
        height, width = edge_image.shape
        
        if side == 'left':
            # Search from left to center
            search_start = 0
            search_end = width // 2
            search_direction = 1
        else:
            # Search from right to center
            search_start = width - 1
            search_end = width // 2
            search_direction = -1
        
        # Column-wise search
        edge_votes = []
        
        for x in range(search_start, search_end, search_direction):
            # Count edge pixels in this column
            column_edges = np.sum(edge_image[:, x] > 0)
            
            # If significant edge activity found
            if column_edges > height * 0.3:  # >30% of column has edges
                edge_votes.append(x)
                
                # Found strong edge
                if len(edge_votes) >= 3:
                    return int(np.median(edge_votes))
        
        return None
    
    def detect_edge_by_color(self, frame: np.ndarray) -> Tuple[Optional[int], Optional[int]]:
        """
        Detect sidewalk edges using color segmentation
        
        Assumes sidewalk is lighter than surrounding (grass, road)
        
        Args:
            frame: Input BGR image
            
        Returns:
            Tuple of (left_edge_x, right_edge_x) in pixels
        """
        # Extract ROI
        roi = frame[self.roi_top:self.roi_bottom, :]
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Define range for gray/light colors (typical sidewalk)
        # Sidewalks are usually gray with low saturation
        lower_gray = np.array([0, 0, 80])     # Low saturation, medium-high value
        upper_gray = np.array([180, 50, 255])
        
        # Create mask for sidewalk color
        sidewalk_mask = cv2.inRange(hsv, lower_gray, upper_gray)
        
        # Morphological operations to clean up mask
        kernel = np.ones((5, 5), np.uint8)
        sidewalk_mask = cv2.morphologyEx(sidewalk_mask, cv2.MORPH_CLOSE, kernel)
        sidewalk_mask = cv2.morphologyEx(sidewalk_mask, cv2.MORPH_OPEN, kernel)
        
        # Find boundaries of largest white region
        contours, _ = cv2.findContours(sidewalk_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
        
        # Find largest contour (assumed to be sidewalk)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        left_edge = x
        right_edge = x + w
        
        return left_edge, right_edge
    
    def check_user_position(self, left_edge: Optional[int], 
                          right_edge: Optional[int]) -> Tuple[bool, Optional[str]]:
        """
        Check if user (camera) is dangerously close to sidewalk edge
        
        Assumes camera is centered in frame, representing user's position
        
        Args:
            left_edge: X-coordinate of left edge
            right_edge: X-coordinate of right edge
            
        Returns:
            Tuple of (is_near_edge: bool, edge_side: str or None)
            edge_side is 'left' or 'right' if near edge, None otherwise
        """
        if left_edge is None or right_edge is None:
            return False, None
        
        # Calculate warning zone boundaries
        warning_width = int(self.frame_width * self.warning_distance)
        left_warning_zone = left_edge + warning_width
        right_warning_zone = right_edge - warning_width
        
        # Camera/user is at center of frame
        user_x = self.frame_width // 2
        
        # Check if user is in warning zone
        if user_x < left_warning_zone:
            return True, 'left'
        elif user_x > right_warning_zone:
            return True, 'right'
        else:
            return False, None
    
    def draw_edge_overlay(self, frame: np.ndarray, 
                         left_edge: Optional[int], 
                         right_edge: Optional[int]) -> np.ndarray:
        """
        Draw visual overlay showing detected edges
        
        Args:
            frame: Input frame
            left_edge: X-coordinate of left edge
            right_edge: X-coordinate of right edge
            
        Returns:
            Frame with overlay drawn
        """
        overlay = frame.copy()
        
        if left_edge is not None:
            # Draw left edge line
            cv2.line(overlay, 
                    (left_edge, self.roi_top), 
                    (left_edge, self.roi_bottom),
                    config.COLORS['edge'], 2)
            
            # Draw warning zone
            warning_width = int(self.frame_width * self.warning_distance)
            cv2.rectangle(overlay,
                         (left_edge, self.roi_top),
                         (left_edge + warning_width, self.roi_bottom),
                         config.COLORS['edge'], 1)
        
        if right_edge is not None:
            # Draw right edge line
            cv2.line(overlay,
                    (right_edge, self.roi_top),
                    (right_edge, self.roi_bottom),
                    config.COLORS['edge'], 2)
            
            # Draw warning zone
            warning_width = int(self.frame_width * self.warning_distance)
            cv2.rectangle(overlay,
                         (right_edge - warning_width, self.roi_top),
                         (right_edge, self.roi_bottom),
                         config.COLORS['edge'], 1)
        
        # Blend overlay with original frame
        result = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        return result
    
    def process_frame(self, frame: np.ndarray) -> dict:
        """
        Complete sidewalk edge processing for a frame
        
        Args:
            frame: Input BGR image
            
        Returns:
            Dictionary with:
                - left_edge: X-coordinate or None
                - right_edge: X-coordinate or None
                - near_edge: Boolean
                - edge_side: 'left', 'right', or None
                - annotated_frame: Frame with visualization
        """
        # Try edge detection first (more reliable for well-defined edges)
        left_edge, right_edge = self.detect_edges(frame)
        
        # If edge detection fails, try color-based detection
        if left_edge is None or right_edge is None:
            left_edge_color, right_edge_color = self.detect_edge_by_color(frame)
            left_edge = left_edge or left_edge_color
            right_edge = right_edge or right_edge_color
        
        # Check user position
        near_edge, edge_side = self.check_user_position(left_edge, right_edge)
        
        # Create annotated frame
        annotated_frame = frame.copy()
        if config.EDGE_DETECTION_ENABLED and (left_edge or right_edge):
            annotated_frame = self.draw_edge_overlay(frame, left_edge, right_edge)
        
        return {
            'left_edge': left_edge,
            'right_edge': right_edge,
            'near_edge': near_edge,
            'edge_side': edge_side,
            'annotated_frame': annotated_frame
        }
