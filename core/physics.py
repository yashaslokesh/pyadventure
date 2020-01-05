import pygame
import pygame.math

from typing import Sequence

from . import constants as const


class PhysicsBody:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def move(self, vel: pygame.Vector2, obstacles: Sequence[pygame.Rect]):
        collisions = {"top": False, "bottom": False, "left": False, "right": False}

        # TODO:
        #  Problem: Found a problem with collisions... The x_vel or y_vel may be too high sometimes causing the
        #  sprite to move through a wall and then this method would possibly move them a little further
        #  to prevent a sprite from getting stuck inside an obstacle. This problem is only caused by JUMPING so far,
        #  since the y_val magnitude is higher than the length of a tile.
        #  Solution: ???????????????????????????????????????????

        col_vel = vel.normalize()
        col_vel.scale_to_length(const.TILE_LENGTH)  # Vector of length 40 in the direction of our movement

        self.rect.move_ip(vel.x, 0)
        collision_indices = self.rect.collidelistall(obstacles)
        for obj in map(lambda i: obstacles[i], collision_indices):
            if vel.x > 0:
                self.rect.right = obj.left
                collisions["right"] = True
            else:
                self.rect.left = obj.right
                collisions["left"] = True

        self.rect = self.rect.move(0, vel.y)
        collision_indices = self.rect.collidelistall(obstacles)
        for obj in map(lambda i: obstacles[i], collision_indices):
            if vel.y > 0:
                self.rect.bottom = obj.top
                collisions["bottom"] = True
            else:
                self.rect.top = obj.bottom
                collisions["top"] = True

        return collisions

    def update_xy(self, x, y):
        self.rect.x, self.rect.y = x, y
