"""
Canvas management for Air Canvas
"""

import numpy as np
import cv2
from config.settings import DRAW_COLORS, DRAW_RADIUS, LINE_THICKNESS

class Canvas:
    """Manages the drawing canvas"""
    
    def __init__(self, frame_shape, background_color=(0, 0, 0)):
        """
        Initialize the canvas
        
        Args:
            frame_shape: Shape of the video frame (height, width, channels)
            background_color: Background color (BGR)
        """
        self.shape = frame_shape
        self.background_color = background_color
        self.clear()
        self.current_color = 'blue'
        self.points = []
        self.color_history = []
        
    def clear(self):
        """Clear the canvas"""
        self.canvas = np.full(self.shape, self.background_color, dtype=np.uint8)
        self.points = []
        self.color_history = []
        
    def draw_point(self, position):
        """
        Draw a point on the canvas
        
        Args:
            position: (x, y) coordinates
        """
        if position is None:
            return
            
        color = DRAW_COLORS.get(self.current_color, (255, 0, 0))
        
        # Add point to history
        self.points.append(position)
        self.color_history.append(self.current_color)
        
        # Draw on canvas
        cv2.circle(self.canvas, position, DRAW_RADIUS, color, -1)
        
    def draw_line_to(self, position):
        """
        Draw a line from the last point to the current position
        
        Args:
            position: (x, y) coordinates
        """
        if position is None or len(self.points) == 0:
            return
            
        color = DRAW_COLORS.get(self.current_color, (255, 0, 0))
        
        # Draw line from last point to current position
        last_pos = self.points[-1]
        cv2.line(self.canvas, last_pos, position, color, LINE_THICKNESS)
        
        # Update history
        self.points.append(position)
        self.color_history.append(self.current_color)
        
    def get_canvas(self):
        """Return the canvas image"""
        return self.canvas
    
    def set_color(self, color_name):
        """Change the drawing color"""
        if color_name in DRAW_COLORS:
            self.current_color = color_name
            
    def get_current_color(self):
        """Get the current drawing color"""
        return self.current_color
    
    def get_color_bgr(self):
        """Get the current color in BGR format"""
        return DRAW_COLORS.get(self.current_color, (255, 0, 0))
