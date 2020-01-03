import pygame

from typing import Sequence


class PhysicsBody:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def move(self, x_vel, y_vel, obstacles: Sequence[pygame.Rect]):
        self.rect.x += x_vel
        collision_indices = self.rect.collidelistall(obstacles)
        collisions = {"top": False, "bottom": False, "left": False, "right": False}

        for obj in map(lambda i: obstacles[i], collision_indices):
            if x_vel > 0:
                self.rect.right = obj.left
                collisions["right"] = True
            else:
                self.rect.left = obj.right
                collisions["left"] = True

        self.rect.y += y_vel
        collision_indices = self.rect.collidelistall(obstacles)

        for obj in map(lambda i: obstacles[i], collision_indices):
            if y_vel > 0:
                self.rect.bottom = obj.top - 1
                collisions["bottom"] = True
            else:
                self.rect.top = obj.bottom
                collisions["top"] = True

        # print(collisions)

        return collisions
