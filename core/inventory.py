# from abc import ABC, abstractmethod
import pygame
from pygame.locals import *

from random import randint

import core.constants as c


class Item(object):
    def __init__(self, name: str):
        self.name = name


class Weapon(Item):
    pass


class Potion(Item):
    pass


w = Weapon("hello")


class Inventory(object):
    def __init__(self):

        self.items = []

        self.active_item = [0, 0]

        self.rect = pygame.Rect(
            c.INVENTORY_X, c.INVENTORY_Y, c.INVENTORY_WIDTH, c.INVENTORY_HEIGHT
        )

        self.sample_item_colors = []

        # set rectangle colors for sample inventory
        for i in range(4):
            self.sample_item_colors.append([])
            for j in range(4):
                r, g, b = randint(50, 255), randint(50, 255), randint(50, 255)
                self.sample_item_colors[i].append((r, g, b))

        self.add_sample_items()

    # TODO: get rid of in the future
    def add_sample_items(self):
        self.items.append(Weapon("Sword"))
        self.items.append(Potion("Health Potion"))

    def update(self, keydown_event):
        if keydown_event.key == K_DOWN:
            self.active_item[1] += 1
            if self.active_item[1] == 4:
                self.active_item[1] = 0
        elif keydown_event.key == K_UP:
            self.active_item[1] += -1
            if self.active_item[1] == -1:
                self.active_item[1] = 3
        elif keydown_event.key == K_LEFT:
            self.active_item[0] -= 1
            if self.active_item[0] == -1:
                self.active_item[0] = 3
        elif keydown_event.key == K_RIGHT:
            self.active_item[0] += 1
            if self.active_item[0] == 4:
                self.active_item[0] = 0

    def draw(self, screen: pygame.Surface):
        # TODO: Add actual sprite here
        pygame.draw.rect(screen, (172, 237, 182), self.rect)
        # TODO: Draw all sprite representations of each item

        # Draws all rectangles for item spaces
        item_rect = self.rect.copy()
        item_rect.size = 150, 150
        for i in range(4):
            item_rect.x = self.rect.x + (i * 150)
            for j in range(4):
                # item_rect = self.rect.copy()
                # item_rect.x, item_rect.y = item_rect.x + (i * 150), item_rect.y + (j * 150)
                item_rect.y = self.rect.y + (j * 150)
                # item_rect.size = 150, 150
                pygame.draw.rect(screen, self.sample_item_colors[i][j], item_rect)

        selection_box = self.rect.copy()
        selection_box.size = 150, 150
        selection_box.x += (self.active_item[0] * 150) + (
            c.SELECTION_BOX_THICKNESS // 2
        )
        selection_box.y += (self.active_item[1] * 150) + (
            c.SELECTION_BOX_THICKNESS // 2
        )
        selection_box.width -= c.SELECTION_BOX_THICKNESS
        selection_box.height -= c.SELECTION_BOX_THICKNESS

        pygame.draw.rect(
            screen, (255, 255, 255), selection_box, c.SELECTION_BOX_THICKNESS
        )


if __name__ == "__main__":
    i = Item(4)
