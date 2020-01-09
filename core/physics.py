import pygame
import pygame.math

from typing import Sequence
from operator import attrgetter

from . import constants as const
from . import events


class PhysicsBody:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def move(self, vel: pygame.Vector2, obstacles: Sequence[pygame.Rect]):
        # Velocity is for moving the top-left corner, so it includes the width if moving to the right,
        # and includes the height if moving down
        collisions = {"top": False, "bottom": False, "left": False, "right": False}

        if abs(vel.x) + self.rect.width > const.TILE_LENGTH:
            movement_projection = pygame.Rect(0, self.rect.y, abs(vel.x), self.rect.height)
            if vel.x > 0:
                movement_projection.x = self.rect.right
            else: # vel.x < 0:
                movement_projection.x = self.rect.x - abs(vel.x)

            coll_rects = collidelistall_rects(movement_projection, obstacles)
            if len(coll_rects) == 0:
                self.rect.move_ip(vel.x, 0)
            coll_rects = collidelistall_rects(movement_projection, obstacles)
        else:
            self.rect.move_ip(vel.x, 0)
            coll_rects = collidelistall_rects(self.rect, obstacles)

        if len(coll_rects) != 0:
            if vel.x > 0:
                closest = min(coll_rects, key=attrgetter('x'))
                self.rect.right = closest.left
                collisions["right"] = True
            elif vel.x < 0:
                closest = max(coll_rects, key=attrgetter('x'))
                self.rect.left = closest.right
                collisions["left"] = True

        # y-dir

        if abs(vel.y) + self.rect.height >= const.TILE_LENGTH:
            movement_projection = pygame.Rect(self.rect.x, 0, self.rect.width, abs(vel.y))
            if vel.y < 0:
                movement_projection.y = self.rect.y - abs(vel.y)
            else: # vel.y > 0
                movement_projection.y = self.rect.bottom

            coll_rects = collidelistall_rects(movement_projection, obstacles)
            if len(coll_rects) == 0:
                self.rect.move_ip(0, vel.y)

            coll_rects = collidelistall_rects(movement_projection, obstacles)
            pygame.event.post(pygame.event.Event(events.DRAW_RECT_EVENT, {'rects': [movement_projection], 'color': const.BLUE}))
        else:
            self.rect.move_ip(0, vel.y)
            coll_rects = collidelistall_rects(self.rect, obstacles)

        if len(coll_rects) != 0:
            if vel.y > 0:
                closest = min(coll_rects, key=attrgetter('y'))
                self.rect.bottom = closest.top
                collisions["bottom"] = True
            elif vel.y < 0:
                closest = max(coll_rects, key=attrgetter('y'))
                self.rect.top = closest.bottom
                collisions["top"] = True

        return collisions

    def update_xy(self, x, y):
        self.rect.x, self.rect.y = x, y


def collidelistall_rects(rect, obstacles):
    collision_indices = rect.collidelistall(obstacles)
    return list(map(lambda i: obstacles[i], collision_indices))

