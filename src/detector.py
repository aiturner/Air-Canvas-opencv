"""
Marker detection module for Air Canvas
"""

import cv2
import numpy as np
from config.settings import HSV_RANGES
from src.utils import create_color_mask, find_largest_contour, get_centroid

class MarkerDetector:
    """Detects and tracks colored markers in video feed"""
    
    def __init__(self, color_name='blue'):
        """
        Initialize the marker detector
        
        Args:
            color_name: Name of the color to detect
        """
        self.color_name = color_name
        # Get the HSV range dictionary for this color
        color_range = HSV_RANGES.get(color_name, HSV_RANGES['blue'])
        # Extract lower and upper as numpy arrays
        self.lower_hsv = np.array(color_range['lower'], dtype=np.uint8)
        self.upper_hsv = np.array(color_range['upper'], dtype=np.uint8)
        self.prev_position = None
        
    def detect(self, frame):
        """
        Detect marker position in a frame
        
        Args:
            frame: BGR image
            
        Returns:
            (x, y) position of marker, or None if not detected
        """
        # Create color mask
        mask = create_color_mask(frame, self.lower_hsv, self.upper_hsv)
        
        # Find largest contour
        contour = find_largest_contour(mask)
        
        if contour is not None:
            # Get centroid
            position = get_centroid(contour)
            
            # Smooth movement (optional)
            if self.prev_position is not None and position is not None:
                # Simple moving average smoothing
                position = (
                    int(0.7 * position[0] + 0.3 * self.prev_position[0]),
                    int(0.7 * position[1] + 0.3 * self.prev_position[1])
                )
            
            self.prev_position = position
            return position
        
        self.prev_position = None
        return None
    
    def get_mask(self, frame):
        """Get the color mask for debugging"""
        return create_color_mask(frame, self.lower_hsv, self.upper_hsv)
    
    def set_color(self, color_name):
        """Change the detection color"""
        self.color_name = color_name
        color_range = HSV_RANGES.get(color_name, HSV_RANGES['blue'])
        self.lower_hsv = np.array(color_range['lower'], dtype=np.uint8)
        self.upper_hsv = np.array(color_range['upper'], dtype=np.uint8)
        self.prev_position = None
