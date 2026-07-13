#!/usr/bin/env python3
"""
Real-Time Air Canvas - Main Application
Draw in the air using colored markers and your webcam!
"""

import cv2
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.detector import MarkerDetector
from src.canvas import Canvas
from src.utils import save_drawing
from config.settings import (
    WINDOW_NAME, DEBUG_WINDOW,
    KEY_COLOR_1, KEY_COLOR_2, KEY_COLOR_3,
    KEY_CLEAR, KEY_SAVE, KEY_QUIT
)

class AirCanvasApp:
    """Main application class"""
    
    def __init__(self, camera_id=0):
        """
        Initialize the Air Canvas application
        
        Args:
            camera_id: Webcam device ID
        """
        self.camera_id = camera_id
        self.cap = None
        self.detector = MarkerDetector('blue')
        self.canvas = None
        self.is_drawing = False
        self.running = True
        
        # Color mapping for keys
        self.color_map = {
            KEY_COLOR_1: 'blue',
            KEY_COLOR_2: 'green',
            KEY_COLOR_3: 'red'
        }
        
    def initialize(self):
        """Initialize camera and canvas"""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_id}")
            return False
            
        # Get frame dimensions
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read from camera")
            return False
            
        height, width = frame.shape[:2]
        self.canvas = Canvas((height, width, 3))
        
        print(f"Camera initialized: {width}x{height}")
        print("Controls:")
        print("  1, 2, 3  - Switch colors (Blue, Green, Red)")
        print("  c        - Clear canvas")
        print("  s        - Save drawing")
        print("  q        - Quit")
        print("\nStart drawing with your colored marker!")
        
        return True
        
    def run(self):
        """Main application loop"""
        if not self.initialize():
            return
            
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            # Flip horizontally for mirror view
            frame = cv2.flip(frame, 1)
            
            # Detect marker position
            position = self.detector.detect(frame)
            
            # Draw on canvas if marker is detected
            if position is not None:
                # Draw a circle at the marker position (visual feedback)
                color = self.canvas.get_color_bgr()
                cv2.circle(frame, position, 10, color, -1)
                
                # Draw on canvas
                if self.is_drawing:
                    self.canvas.draw_line_to(position)
                else:
                    self.canvas.draw_point(position)
                    self.is_drawing = True
            else:
                # Marker lost - stop drawing
                self.is_drawing = False
                
            # Get debug mask
            mask = self.detector.get_mask(frame)
            
            # Combine frame with canvas
            canvas_img = self.canvas.get_canvas()
            combined = cv2.addWeighted(frame, 0.6, canvas_img, 0.4, 0)
            
            # Add UI text
            self._draw_ui(combined)
            
            # Display
            cv2.imshow(WINDOW_NAME, combined)
            cv2.imshow(DEBUG_WINDOW, mask)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            self._handle_key(key)
            
        # Cleanup
        self.cleanup()
        
    def _draw_ui(self, frame):
        """Draw UI elements on the frame"""
        # Color indicator
        current_color = self.canvas.get_current_color()
        color_bgr = self.canvas.get_color_bgr()
        
        # Show current color
        cv2.rectangle(frame, (10, 10), (60, 60), color_bgr, -1)
        cv2.putText(frame, f"Color: {current_color}", (70, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Instructions
        y_pos = frame.shape[0] - 30
        cv2.putText(frame, "1:Blue 2:Green 3:Red | c:Clear s:Save q:Quit", 
                    (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Status
        status = "DRAWING" if self.is_drawing else "READY"
        cv2.putText(frame, f"Status: {status}", 
                    (frame.shape[1] - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (0, 255, 0) if self.is_drawing else (255, 255, 0), 2)
        
    def _handle_key(self, key):
        """Handle keyboard input"""
        if key == KEY_QUIT:
            self.running = False
            return
            
        # Color switching
        if key in self.color_map:
            color_name = self.color_map[key]
            self.detector.set_color(color_name)
            self.canvas.set_color(color_name)
            print(f"Switched to {color_name}")
            
        # Clear canvas
        elif key == KEY_CLEAR:
            self.canvas.clear()
            self.is_drawing = False
            print("Canvas cleared")
            
        # Save drawing
        elif key == KEY_SAVE:
            canvas_img = self.canvas.get_canvas()
            if np.any(canvas_img != 0):  # Check if canvas is not empty
                filename = save_drawing(canvas_img)
                print(f"Drawing saved as {filename}")
            else:
                print("Canvas is empty - nothing to save")
                
    def cleanup(self):
        """Release resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed")


def main():
    """Entry point"""
    app = AirCanvasApp(camera_id=0)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
