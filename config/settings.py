"""
Configuration settings for Air Canvas
"""

# Default HSV ranges for different colors
HSV_RANGES = {
    'blue': {
        'lower': (110, 50, 50),
        'upper': (130, 255, 255)
    },
    'green': {
        'lower': (40, 50, 50),
        'upper': (80, 255, 255)
    },
    'red': {
        'lower': (0, 50, 50),
        'upper': (10, 255, 255)
    },
    'yellow': {
        'lower': (20, 50, 50),
        'upper': (35, 255, 255)
    }
}

# Colors for drawing (BGR format)
DRAW_COLORS = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
    'yellow': (0, 255, 255)
}

# Drawing parameters
DRAW_RADIUS = 5
LINE_THICKNESS = 3
MIN_CONTOUR_AREA = 500

# Window settings
WINDOW_NAME = "Air Canvas"
DEBUG_WINDOW = "Mask"

# Key mappings
KEY_COLOR_1 = ord('1')
KEY_COLOR_2 = ord('2')
KEY_COLOR_3 = ord('3')
KEY_CLEAR = ord('c')
KEY_SAVE = ord('s')
KEY_QUIT = ord('q')
