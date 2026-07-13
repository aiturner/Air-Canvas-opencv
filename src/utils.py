"""
Utility functions for Air Canvas
"""

import cv2
import numpy as np
from datetime import datetime
import os

def get_hsv_range(color_name, hsv_ranges):
    """
    Get HSV range for a given color name
    
    Args:
        color_name: Name of the color
        hsv_ranges: Dictionary of HSV ranges
        
    Returns:
        Tuple of (lower, upper) HSV values
    """
    if color_name in hsv_ranges:
        return hsv_ranges[color_name]
    else:
        raise ValueError(f"Color '{color_name}' not found in HSV ranges")

def create_color_mask(frame, lower_hsv, upper_hsv):
    """
    Create a binary mask for a specific color range
    
    Args:
        frame: BGR image
        lower_hsv: Lower HSV bound
        upper_hsv: Upper HSV bound
        
    Returns:
        Binary mask
    """

    lower = np.array(lower_hsv, dtype=np.uint8)
    upper = np.array(upper_hsv, dtype=np.uint8)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    
    # Morphological operations (cleaning by removing noise without shrinking object) 
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    return mask

def find_largest_contour(mask, min_area=500):
    """
    Find the largest contour in a mask
    
    Args:
        mask: Binary mask
        min_area: Minimum area to consider
        
    Returns:
        Largest contour or None if none found
    """

    # RETR_EXTERNAL only returns external contours & CHIAN_APPROX_SIM compresses
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # Ignores noise
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    
    if not valid_contours:
        return None
    
    return max(valid_contours, key=cv2.contourArea)

def get_centroid(contour):
    """
    Get the centroid of a contour
    
    Args:
        contour: Contour points
        
    Returns:
        (x, y) centroid coordinates
    """
    M = cv2.moments(contour)
    if M['m00'] == 0:
        return None
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return (cx, cy)

def save_drawing(canvas, directory="outputs/drawings"):
    """
    Save the canvas as an image file
    
    Args:
        canvas: Canvas image
        directory: Directory to save to
        
    Returns:
        Filename of saved image
    """
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{timestamp}.png"
    filepath = os.path.join(directory, filename)
    cv2.imwrite(filepath, canvas)
    return filename
