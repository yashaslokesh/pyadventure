import pygame
import pygame.math

from typing import Sequence
from operator import attrgetter

from . import constants as const


class PhysicsBody:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def move(self, vel: pygame.Vector2, obstacles: Sequence[pygame.Rect]):
        # Velocity is for moving the top-left corner, so it includes the width if moving to the right,
        # and includes the height if moving down
        collisions = {"top": False, "bottom": False, "left": False, "right": False}

        # TODO:
        #  Problem: Found a problem with collisions... The x_vel or y_vel may be too high sometimes causing the
        #  sprite to move through a wall and then this method would possibly move them a little further
        #  to prevent a sprite from getting stuck inside an obstacle. This problem is only caused by JUMPING so far,
        #  since the y_val magnitude is higher than the length of a tile.
        #  Solution: ???????????????????????????????????????????
        #  Possible solution: Create a rectangle that represents our velocity vector in one of the two directions,
        #                     and then test for collision between this rect and the obstacles. This is only necessary
        #                     if the velocity will be greater than the TILE_LENGTH (currently 40)

        if abs(vel.x) > const.TILE_LENGTH:
            movement_projection = pygame.Rect(self.rect.x, self.rect.y, self.rect.width + abs(vel.x), self.rect.height)
            coll_rects = collidelistall_rects(movement_projection, obstacles)
        else:
            self.rect.move_ip(vel.x, 0)
            coll_rects = collidelistall_rects(self.rect, obstacles)

        if len(coll_rects) != 0:
            if vel.x > 0:
                closest = min(coll_rects, key=attrgetter('x'))
                self.rect.right = closest.left
                collisions["right"] = True
            else:
                closest = max(coll_rects, key=attrgetter('x'))
                self.rect.left = closest.right
                collisions["left"] = True

        if abs(vel.y) > const.TILE_LENGTH:
            movement_projection = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,
                                              self.rect.height + abs(vel.y))
            if vel.y < 0:
                movement_projection.top = self.rect.y + vel.y
            coll_rects = collidelistall_rects(movement_projection, obstacles)
        else:
            self.rect.move_ip(0, vel.y)
            coll_rects = collidelistall_rects(self.rect, obstacles)

        if len(coll_rects) != 0:
            if vel.y > 0:
                closest = min(coll_rects, key=attrgetter('y'))
                self.rect.bottom = closest.top
                collisions["bottom"] = True
            else:
                closest = max(coll_rects, key=attrgetter('y'))
                self.rect.top = closest.bottom
                collisions["top"] = True

        return collisions

    def update_xy(self, x, y):
        self.rect.x, self.rect.y = x, y


def collidelistall_rects(rect, obstacles):
    collision_indices = rect.collidelistall(obstacles)
    return list(map(lambda i: obstacles[i], collision_indices))

