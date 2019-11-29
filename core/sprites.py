""" This module contains all sprite definitions used in the game """
# external
import pygame
from pygame.locals import *

# python stdlib
import math
import os
from enum import Enum, auto

# project files
import core.constants as c
from core.images import load_image
from core.inventory import Inventory

# Works if run from the base directory

# def load_image(path):
#     image = pygame.image.load(os.path.join('assets', 'images', path))
#     image = image.convert_alpha()
#     return image


class PlayerStates(Enum):
    STANDING = auto()
    WALK_LEFT = auto()
    WALK_RIGHT = auto()
    TALKING = auto()
    JUMPING = auto()


##
class Player(pygame.sprite.DirtySprite):
    """ This class will control the player sprite.
    
    self.animations is a dictionary with (str, animation sequence) pairs. The str represents the name of an animation,
    and the animation sequence is a list of numbers that specify the images that should be used in animation that 
    sequence.

    self._active_state is set to 'talking-sequence' starting off, because that's where the game will start.
    
    self.anim_frame should be reset every time the animation is changed

    self.anim_frame_changed_speed is set to 0.08, cannot be changed at runtime.
    """

    def __init__(self, start_x, start_y):
        super().__init__()

        """ 
        Initializes all dictionaries used for storing various animation values, all dictionaries have animation names
        as their keys.

        self.animations has a list of ints for the animation sequence. This is used so that we don't have to load the 
        same image multiple times for the animation.

        self.images has a list of animation images loaded in order, so that the list of ints in self.animations can 
        access the list of animation images easily.
        """
        self.animations = {}
        self.images = {}
        self.mass = 50

        self.START_LOCATION = start_x, start_y

        self.animation_speed = 0.10

        self.move_animations = set()

        self.rect = None

        self.y_momentum = 0

        self._active_state = None

        """ TODO: Remove this in the future, only used now because sprites' animations take different sizes """
        self.max_width = None

        self.inventory = Inventory()

    def add_animation(
        self,
        anim_state: PlayerStates,
        anim_seq: list,
        path: str,
        move_animation: bool = False,
    ):
        """ 
        Add animations with an identifying "animation_name" tag, along with a sequence of numbers
        for the animation sequence (that double as the image file names), and the path to image files
        of the animation 
        """

        self.animations[anim_state] = anim_seq
        self.images[anim_state] = []

        if move_animation:
            self.move_animations.add(anim_state)

        """Loads each image only once into another dictionary containing a list of images for each animation sequence"""
        animation_image_frames = sorted([i for i in set(anim_seq)])

        for frame in animation_image_frames:
            image = load_image(os.path.join(path, f"{frame}.png"))
            (self.images[anim_state]).append(image)

        # Sets active state
        self.set_active_state(anim_state)

        """ TODO: Remove in future when sprite animation sizes are uniform """
        # self.max_width = max(max(surf.get_width() for surf in ))

        self.max_width = 0
        for anim_list in self.images.values():
            for surf in anim_list:
                w = surf.get_width()

                if w > self.max_width:
                    self.max_width = w

        # self.max_width = max(surf.get_width for surf in (l for l in self.images.values()))

    def set_active_state(self, new_state: PlayerStates):
        """ Pass in the new state, alter the sprite's properties based on the new state.
        The active state is automatically set to the most recent state for which an animation was added
        using add_animation(). This method takes care of changing animations
        """
        if new_state == PlayerStates.JUMPING:
            self.y_momentum = c.JUMP_SPEED

        changed_state = self._active_state != new_state

        self._active_state = new_state

        self._update_state_animation(changed_state)

    def _update_state_animation(self, changed_state: bool):
        """ Should not have to call this method, is automatically called when state is changed """

        # Only reset animation frame progress if we have a new animation, else we can continue animation
        if changed_state:
            self.anim_frame = 0.00

        if self.rect is None:
            """ If the active animation hasn't been set yet, then we want to start from a pre-determined location. """
            x, y = self.START_LOCATION
        else:
            """ Else we start from the previous location """
            x, y = self.rect.x, self.rect.y

        first_image_num = self.animations[self._active_state][0]
        self.image = self.images[self._active_state][first_image_num]

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

    def get_active_state(self):
        return self._active_state

    """ Define active_state as a property with the previously defined getter and setter functions """
    active_state = property(
        get_active_state, set_active_state, doc="Activate state of this player"
    )

    def _handle_input(self, keys):
        """ TODO: Replace all occurrences of max_width with just rect.width 
        Requires fixing some animations first.
        """
        horiz_speed = 0
        vert_speed = 0

        """
        Consulted this PEP document... switch statements were not added to python
        https://www.python.org/dev/peps/pep-3103/#if-elif-chain-vs-dict-based-dispatch
        So dictionary dispatch is used instead.
        """

        def case_standing():
            pass

        def case_walk_left():
            nonlocal horiz_speed
            if keys[K_UP]:
                self.y_momentum = c.JUMP_SPEED
                self.set_active_state(PlayerStates.JUMPING)
            elif keys[K_RIGHT]:
                self.set_active_state(PlayerStates.WALK_RIGHT)
                if self.rect.right + 5 <= c.SCREEN_WIDTH:
                    horiz_speed = 5
            elif keys[K_LEFT]:
                if self.rect.left - 5 >= 0:
                    horiz_speed = -5

        def case_walk_right():
            nonlocal horiz_speed
            if keys[K_UP]:
                self.y_momentum = c.JUMP_SPEED
                self.set_active_state(PlayerStates.JUMPING)
            elif keys[K_LEFT]:
                self.set_active_state(PlayerStates.WALK_LEFT)
                if self.rect.left - 5 >= 0:
                    horiz_speed = -5
            elif keys[K_RIGHT]:
                if self.rect.right + 5 <= c.SCREEN_WIDTH:
                    horiz_speed = 5

        def case_talking():
            nonlocal horiz_speed
            if keys[K_UP]:
                self.set_active_state(PlayerStates.JUMPING)
                self.y_momentum = c.JUMP_SPEED
            elif keys[K_RIGHT]:
                self.set_active_state(PlayerStates.WALK_RIGHT)
                if self.rect.right + 5 <= c.SCREEN_WIDTH:
                    horiz_speed = 5
            elif keys[K_LEFT]:
                self.set_active_state(PlayerStates.WALK_LEFT)
                if self.rect.left - 5 >= 0:
                    horiz_speed = -5

        def case_jump():
            nonlocal vert_speed, horiz_speed
            if self.rect.bottom + self.y_momentum < c.SCREEN_HEIGHT:
                self.y_momentum += c.GRAVITY
                vert_speed = self.y_momentum
            else:
                self.y_momentum = 0
                self.set_active_state(PlayerStates.TALKING)

            if keys[K_LEFT]:
                if self.rect.left - 5 >= 0:
                    horiz_speed = -5
            elif keys[K_RIGHT]:
                if self.rect.right + 5 <= c.SCREEN_WIDTH:
                    horiz_speed = 5

        switcher_dict = {
            PlayerStates.STANDING: case_standing,
            PlayerStates.WALK_LEFT: case_walk_left,
            PlayerStates.WALK_RIGHT: case_walk_right,
            PlayerStates.TALKING: case_talking,
            PlayerStates.JUMPING: case_jump,
        }

        handler = switcher_dict[self.active_state]
        handler()

        return [horiz_speed, vert_speed]

    ## TODO: Currently returns Rect so Game class can draw background over previous position, but there might be a better way
    def update(self, keys):
        """ 
        Move_sprite will be true if the speed has some non-zero value. Granted, it is only ever a two-element list,
        but using the any() function makes it clean to read.

        If the animation is supposed to be updated, it will be. Otherwise, nothing happens to the sprite's current
        image and rect and animation frame, and we draw the sprite again. """
        sprite_speed = self._handle_input(keys)
        move_sprite = any(speed != 0 for speed in sprite_speed)

        result = None

        ## TODO: Add sprite to LayeredDirty group for easier DirtySprite drawing, in another controller file or game.py
        if (
            self.active_state in self.move_animations and move_sprite
        ) or self.active_state not in self.move_animations:
            prev_rect = self._update_animation(sprite_speed)
            result = prev_rect
            # pygame.draw.rect(screen, BLACK, prev_rect)

        return result

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def _update_animation(self, sprite_speed: list) -> pygame.Rect:
        """
        Will be called if the sprite is supposed to move if the active animation is an animation of movement, or if
        the animation is a non-movement animation. This function just updates the image and the rectangle of the sprite.
        To update the rectangle, we just call the pygame.rect.Rect.move() method with our speed list
        """

        self.anim_frame += self.animation_speed

        if self.anim_frame >= len(self.animations[self.active_state]):
            self.anim_frame = 0.00

        animation_image_num = self.animations[self.active_state][
            math.floor(self.anim_frame)
        ]

        self.image = self.images[self.active_state][animation_image_num]

        prev_rect = self.rect.copy()

        self.rect = self.rect.move(sprite_speed)

        return prev_rect


class NPC(pygame.sprite.DirtySprite):
    """ This class can be subclassed to make any non-player character
    """

    def __init__(self, start_x, start_y):
        super().__init__(self)

        self.animations = {}
        self.images = {}

        self.START_LOCATION = start_x, start_y

        self.animation_speed = 0.10

        self.rect = None

    def add_animation(self, anim_seq: list, path: str):
        pass
