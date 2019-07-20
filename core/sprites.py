""" This module contains all sprite definitions used in the game """

import math
import os
from enum import Enum

import pygame
from pygame.locals import *

from .constants import *
from .images import load_image


# Works if run from the base directory

# def load_image(path):
#     image = pygame.image.load(os.path.join('assets', 'images', path))
#     image = image.convert_alpha()
#     return image


class PlayerStates(Enum):
    STANDING = 1
    WALK_LEFT = 2
    WALK_RIGHT = 3
    TALKING = 4


##
class Player(pygame.sprite.DirtySprite):
    """ This class will control the player sprite.
    
    self.animations is a dictionary with (str, animation sequence) pairs. The str represents the name of an animation,
    and the animation sequence is a list of numbers that specify the images that should be used in animation that 
    sequence.

    self.active_anim is set to 'talking-sequence' starting off, because that's where the game will start.
    
    self.anim_frame should be reset every time the animation is changed

    self.anim_frame_changed_speed is set to 0.08, cannot be changed at runtime.
    """

    def __init__(self, start_x, start_y):
        pygame.sprite.DirtySprite.__init__(self)

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

        self.START_LOCATION = start_x, start_y

        self.animation_speed = 0.10

        self.move_animations = set()

        self.active_anim = None
        self.rect = None

        self._active_state = None

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

    def set_active_state(self, new_state: PlayerStates):
        """ Pass in the new state, alter the sprite's properties based on the new state.
        The active state is automatically set to the most recent state for which an animation was added
        using add_animation(). This method takes care of changing animations
        """

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

    # def set_active_animation(self, animation_name : str):
    #     """ Pass in a string representing the active animation, and the sprite will use that
    #     animation on the next update cycle. This method must be called once before the sprite's
    #     update method is used. """
    #
    #     if animation_name not in self.animations:
    #         raise ValueError('An animation that does not exist was chosen. Please add it first')
    #
    #     if self.rect is None:
    #         """ If the active animation hasn't been set yet, then we want to start from a pre-determined location. """
    #         x, y = self.START_LOCATION
    #     else:
    #         """ Else we start from the previous location """
    #         x, y = self.rect.x, self.rect.y
    #
    #     """ Set active animation string, to be used in update() """
    #     self.active_anim = animation_name
    #
    #     self.anim_frame = 0.00
    #
    #     """ Set first image in animation sequence to be the sprite's image """
    #     animation_image_num = self.animations[self.active_anim][0]
    #     self.image = self.images[self.active_anim][animation_image_num]
    #
    #     self.rect = self.image.get_rect()
    #
    #     self.rect.x = x
    #     self.rect.y = y

    def get_active_animation(self):
        """
        Returns the string representation for the active animation from when it was added.
        """
        return self.active_anim

    def get_active_state(self):
        return self._active_state

    """ Define active_state as a property with the previously defined getter and setter functions """
    active_state = property(
        get_active_state, set_active_state, doc="Activate state of this player"
    )

    def _handle_input(self, keys):
        horiz_speed = 0
        vert_speed = 0

        if keys[K_RIGHT]:
            self.set_active_state(PlayerStates.WALK_RIGHT)
            if self.rect.x + self.rect.width + 5 <= SCREEN_WIDTH:
                horiz_speed = 5

        if keys[K_LEFT]:
            self.set_active_state(PlayerStates.WALK_LEFT)
            if self.rect.x - 5 >= 0:
                horiz_speed = -5

        if keys[K_UP]:
            # if self._active_state in (PlayerStates.WALK_LEFT, PlayerStates.WALK_RIGHT):
            if self.rect.y - 5 >= 0:
                vert_speed = -5

        if keys[K_DOWN]:
            # if self._active_state in (PlayerStates.WALK_LEFT, PlayerStates.WALK_RIGHT):
            if self.rect.y + self.rect.height + 5 <= SCREEN_HEIGHT:
                vert_speed = 5

        ## TODO: Determine if this is the best way to switch a moving state to a neutral state... maybe make FSM?
        if all(i == 0 for i in (horiz_speed, vert_speed)):
            self.set_active_state(PlayerStates.TALKING)

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

    def _update_animation(self, sprite_speed: list):
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
