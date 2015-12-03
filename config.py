# Game Keys
SPRINT = SHIFT = 160 # Windows key code
JUMP = Z = 90
WHIP = X = 88
UP = 38
DOWN = 40
LEFT = 37
RIGHT = 39
BOMB = A = 65
ROPE = S = 83
USE = C = 67
BUY = P = 80

START = T = 84
END = I = 73
LEVEL = K = 75

# Single press keys
ACTIONS = [JUMP, WHIP, USE, BOMB, ROPE, BUY]

# Press + hold keys
MOVEMENTS = [SPRINT, UP, DOWN, LEFT, RIGHT]

# All keys used for gameplay
GAME_KEYS = ACTIONS + MOVEMENTS


# Style
COLORS = {
    JUMP: (0.48, 0.52, 0.47, 0.5),
    WHIP: (0.75, 0.54, 0.29, 0.5),
    BOMB: (1.00, 0.00, 0.00, 0.5),
    ROPE: (0.50, 0.33, 0.20, 0.5),
    USE:  (0.00, 0.00, 0.00, 0.5),
    BUY:  (1.00, 0.69, 0.23, 0.5),
}

LEVEL_COLORS = [
    (0.85, 0.80, 0.62, 1), # Mine
    (0.66, 0.80, 0.40, 1), # Jungle
    (0.20, 0.60, 0.86, 1), # Ice
    (0.97, 0.48, 0.32, 1), # Temple
    (0.86, 0.20, 0.13, 1), # Boss 
]

DEFAULT_COLOR = (0, 0, 0, 1)
