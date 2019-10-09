""" This is a utility file for image processing before being used in a game 
"""

import os

import pygame
from PIL import Image


# Navigates into images/ directory, caller must supply the path to file from here
# Assumes being called from the base directory
def load_image(path) -> pygame.Surface:
    image = pygame.image.load(os.path.join("assets", "images", path))
    image = image.convert_alpha()
    return image


""" Should only be called once on a collection of images """


def crop_images(name, path, num_images, x_offset, y_offset, width, height):
    for file in os.listdir(path):
        image = Image.open(os.path.join(path, file))
        image = image.crop((0, 0, width, height))
        image.show()
        print(image.size)
        image.save(os.path.join(path, file))


# The number of pixels of offset in the 50x50 version
KA_HORIZ_PIXEL_OFFSET = 56
KA_VERTI_PIXEL_OFFSET = 20

""" Only make True if you need to reduce image's dimensions. If you do need to, then also
change the numbers in the if statement below and the relevant file name. 
Don't make True otherwise, or else you definitely won't get desired results!
"""
crop_ka = False

if crop_ka:
    design_size = 100
    base_size = 300
    x_offset = (KA_HORIZ_PIXEL_OFFSET / design_size) * base_size
    y_offset = (KA_VERTI_PIXEL_OFFSET / design_size) * base_size
    num_images = 3

    crop_images(
        name="ka",
        # Assuming this module will be run from the base directory...
        path=os.path.join("assets", "images", "ka", f"{str(base_size)}"),
        num_images=3,
        x_offset=0,
        y_offset=0,
        width=base_size - (x_offset),
        height=base_size - (y_offset),
    )
