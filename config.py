# config.py
# Game constants and configuration

# Board settings
BOARD_SIZE = 100
BOARD_DIMENSION = 10  # 10x10 grid
CELL_SIZE = 60  # pixels per cell
BOARD_WIDTH = CELL_SIZE * BOARD_DIMENSION
BOARD_HEIGHT = CELL_SIZE * BOARD_DIMENSION

# Colors
COLORS = {
    'BOARD_BG': '#2C3E50',
    'CELL_LIGHT': '#ECF0F1',
    'CELL_DARK': '#BDC3C7',
    'SNAKE': '#E74C3C',
    'LADDER': '#27AE60',
    'PLAYER1': '#3498DB',
    'PLAYER2': '#E67E22',
    'PLAYER3': '#9B59B6',
    'PLAYER4': '#F1C40F',
    'TEXT': '#2C3E50',
    'BUTTON': '#3498DB',
    'BUTTON_HOVER': '#2980B9',
    'DICE_RED': '#E74C3C',
    'DICE_WHITE': '#FFFFFF',
    'HIGHLIGHT': '#F39C12'
}

# Snake positions: {head: tail}
SNAKES = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78
}

# Ladder positions: {bottom: top}
LADDERS = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100
}

# Special positions for visual effects
SPECIAL_POSITIONS = {
    'snakes': SNAKES,
    'ladders': LADDERS
}

# Game rules
MAX_PLAYERS = 4
MIN_PLAYERS = 2
WIN_POSITION = 100
CONSECUTIVE_SIX_LIMIT = 3