"""
USED ONLY FOR REFERENCE -
There were some things I implemented in this file that have not been implemented in the other main "game.py" file yet,
so this file is being kept for reference for when I want to implement those things.
"""

import os

import core.sprites as sprites
import core.text as text
import pygame

SCREEN_SIZE = WIDTH, HEIGHT = 800, 800
NAME = "First program!"
FRAMERATE_CAP = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Custom Events ------------
# pygame.USEREVENT = 24, pygame.NUMEVENTS = 32, so we use values in between these
SCROLL_TEXT_EVENT = pygame.USEREVENT + 1  # value of 25

# Font sizes -----------------
DPCOMIC_SCROLLING_TEXT_SIZE = 35

# Timers --------------
# pygame.time.set_timer() takes "event id" and "milliseconds" to fire each event
pygame.time.set_timer(SCROLL_TEXT_EVENT, 100)  # Timer for intro text scroll

# Initialize pygame modules
pygame.init()
pygame.font.init()

# Initialize game with SCREEN_SIZE size and name
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(NAME)

clock = pygame.time.Clock()

## Animation sequences --------------------------------------------
# Main sprite's animation
KA_TALKING_ANIM_SEQUENCE = [2, 1, 2, 1, 0, 1, 2, 1]
KA_WALK_RIGHT = [0, 1]
KA_WALK_LEFT = [0, 1]

# Ball animation
BALL_DEFAULT = [0]

## Directories for animation images ----------------------------
# Main sprite's animation directories
KA_BASE_DIR = "ka"
KA_TALK_DIR = os.path.join(KA_BASE_DIR, "talking")
KA_WALK_RIGHT_DIR = os.path.join(KA_BASE_DIR, "walk_right")
KA_WALK_LEFT_DIR = os.path.join(KA_BASE_DIR, "walk_left")

# Ball animation directory
BALL_DEFAULT_DIR = os.path.join("ball", "multicolored_red_ball")

## Adding player animations
ka = sprites.GameSprite(start_x=0, start_y=0)
ka.add_animation("talking", KA_TALKING_ANIM_SEQUENCE, KA_TALK_DIR)
ka.add_animation("walk_right", KA_WALK_RIGHT, KA_WALK_RIGHT_DIR, move_animation=True)
ka.add_animation("walk_left", KA_WALK_LEFT, KA_WALK_LEFT_DIR, move_animation=True)
ka.set_active_animation("talking")

ball = sprites.GameSprite(start_x=400, start_y=200)
ball.add_animation("default", BALL_DEFAULT, BALL_DEFAULT_DIR)
ball.set_active_animation("default")

# Initialize fonts -------------------------------------------
dpcomic_font = text.load_font(
    os.path.join("dpcomic", "dpcomic.ttf"), size=DPCOMIC_SCROLLING_TEXT_SIZE
)

# intro = text.ScrollingText(dpcomic_font, "I was created by Yashas unsing >{07}using the \n dpcomic font! I added in a backcpace >{06}space \n animation capability today, as you can shee >{04}ee here")

walking_animation_intro = text.ScrollingText(
    dpcomic_font,
    "Today, I designed and added walking \n antima >{05}imations. The trickiest parts parts >{06}were pausing the \n animation, getting the sprite to move reliably, and \n implementing dynamic sprite speed changing.",
)

# Start text scrolling
# intro.start_scroll()
walking_animation_intro.start_scroll()


def active_sprite_speed() -> list:
    """ 
    Will calculate the movement for the 'ka' sprite.
    For now, since the 'ka' sprite is the only active sprite, the animations for walking are hardcoded in. I'll
    have to think of a better, or the best way, to handle switching animations. This function returns a list
    of the horizontal speed and vertical speed for the sprite, and the _move() function in the PlayerSprite class
    takes in this list and moves the sprite's rectangle.
    """

    keys = pygame.key.get_pressed()

    horiz_speed = 0
    vert_speed = 0

    if keys[pygame.K_RIGHT]:
        if ka.rect.x + ka.rect.width + 5 <= WIDTH:
            horiz_speed = 5
        if ka.get_active_animation() != "walk_right":
            ka.set_active_animation("walk_right")

    if keys[pygame.K_LEFT]:
        if ka.rect.x - 5 >= 0:
            horiz_speed = -5
        if ka.get_active_animation() != "walk_left":
            ka.set_active_animation("walk_left")

    if keys[pygame.K_UP]:
        if ka.get_active_animation() in ("walk_left", "walk_right"):
            if ka.rect.y - 5 >= 0:
                vert_speed = -5

    if keys[pygame.K_DOWN]:
        if ka.get_active_animation() in ("walk_left", "walk_right"):
            if ka.rect.y + ka.rect.height + 5 <= HEIGHT:
                vert_speed = 5

    return [horiz_speed, vert_speed]


## Game loop, exits if window is closed or application stopped.
running = True
while running:
    # If user closes window or presses 'q', end game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):
            running = False
        elif event.type == SCROLL_TEXT_EVENT:
            # Updates the scrolling text
            # intro.update()
            walking_animation_intro.update()

    # Make screen black and then draw the image over the image's rect
    screen.fill(BLACK)

    # The speed list which will move our sprite's rectangle
    sprite_speed = active_sprite_speed()

    ball_speed = []
    # If ball and ka sprite are colliding
    # if ball.rect.colliderect(ka.rect):

    ka.update()
    ball.update()

    # Draw text
    # intro.draw(screen=screen)
    walking_animation_intro.draw(screen=screen)

    pygame.display.flip()

    # Cap framerate at 30
    clock.tick(FRAMERATE_CAP)
