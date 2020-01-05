# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Independent from screen size, determines
# how big the map will be
TILE_LENGTH = 40
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = TILE_LENGTH, TILE_LENGTH # Quick fix to enforce a square while not breaking existing game...
# TODO: Remove redundant TILE_* identifiers above... requires changing code in other files also.

INVENTORY_SIZE = INVENTORY_WIDTH, INVENTORY_HEIGHT = (
    600,
    600,
)

INVENTORY_COORDS = INVENTORY_X, INVENTORY_Y = (
    SCREEN_WIDTH // 2 - INVENTORY_WIDTH // 2,
    SCREEN_HEIGHT // 2 - INVENTORY_HEIGHT // 2,
)

SELECTION_BOX_THICKNESS = 20

# Speeds for normally scaled character
GRAVITY = 70
JUMP_SPEED = -1200

WALKING_SPEED = 200
TERMINAL_VEL = 450

SCALE = 0.25

GRAVITY_SCL = GRAVITY * SCALE
JUMP_SPEED_SCL = JUMP_SPEED * SCALE

WALKING_SPEED_SCL = WALKING_SPEED * SCALE
TERMINAL_VEL_SCL = TERMINAL_VEL * SCALE
