""" This module contains all sprite definitions used in the game """

import pygame
import os
import math
# Works if run from the base directory
import core.images as images

# def load_image(path):
#     image = pygame.image.load(os.path.join('assets', 'images', path))
#     image = image.convert_alpha()
#     return image

class GameSprite(pygame.sprite.Sprite):
    """ This class will control the player sprite.
    
    self.animations is a dictionary with (str, animation sequence) pairs. The str represents the name of an animation,
    and the animation sequence is a list of numbers that specify the images that should be used in animation that 
    sequence.

    self.active_anim is set to 'talking-sequence' starting off, because that's where the game will start.
    
    self.anim_frame should be reset every time the animation is changed

    self.anim_frame_changed_speed is set to 0.08, cannot be changed at runtime.
    """

    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)

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

    def add_animation(self, animation_name : str, animation_sequence, path : str, move_animation : bool = False):
        """ 
        Add animations with an identifying "animation_name" tag, along with a sequence of numbers
        for the animation sequence (that double as the image file names), and the path to image files
        of the animation 
        """

        self.animations[animation_name] = animation_sequence
        self.images[animation_name] = []

        if move_animation:
            self.move_animations.add(animation_name)

        """Loads each image only once into another dictionary containing a list of images for each animation sequence"""
        animation_image_frames = sorted([i for i in set(animation_sequence)])

        for frame in animation_image_frames:
            image = images.load_image(os.path.join(path, f'{frame}.png'))
            (self.images[animation_name]).append(image)

    def set_active_animation(self, animation_name : str):
        """ Pass in a string representing the active animation, and the sprite will use that
        animation on the next update cycle. This method must be called once before the sprite's
        update method is used. """

        if animation_name not in self.animations:
            raise ValueError('An animation that does not exist was chosen. Please add it first')

        if self.rect is None:
            """ If the active animation hasn't been set yet, then we want to start from a pre-determined location. """
            x, y = self.START_LOCATION
        else:
            """ Else we start from the previous location """
            x, y = self.rect.x, self.rect.y

        """ Set active animation string, to be used in update() """
        self.active_anim = animation_name

        self.anim_frame = 0.00

        """ Set first image in animation sequence to be the sprite's image """
        animation_image_num = self.animations[self.active_anim][0]
        self.image = self.images[self.active_anim][animation_image_num]

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
    
    def get_active_animation(self):
        """
        Returns the string representation for the active animation from when it was added.
        """
        return self.active_anim
    

    def update(self, screen : pygame.surface.Surface, sprite_speed : list):
        """ 
        Move_sprite will be true if the speed has some non-zero value. Granted, it is only ever a two-element list,
        but using the any() function makes it clean to read.
        
        If the animation is supposed to be updated, it will be. Otherwise, nothing happens to the sprite's current
        image and rect and animation frame, and we draw the sprite again. """
        move_sprite = any(speed != 0 for speed in sprite_speed)

        if ((self.active_anim in self.move_animations and move_sprite) or
            self.active_anim not in self.move_animations):
                self._update_animation(sprite_speed)

        screen.blit(self.image, self.rect)
        
    def _update_animation(self, sprite_speed : list):
        """
        Will be called if the sprite is supposed to move if the active animation is an animation of movement, or if
        the animation is a non-movement animation. This function just updates the image and the rectangle of the sprite.
        To update the rectangle, we just call the pygame.rect.Rect.move() method with our speed list
        """

        self.anim_frame += self.animation_speed

        if self.anim_frame >= len(self.animations[self.active_anim]):
            self.anim_frame = 0.00

        animation_image_num = self.animations[self.active_anim][math.floor(self.anim_frame)]

        self.image = self.images[self.active_anim][animation_image_num]

        self.rect = self.rect.move(sprite_speed)

