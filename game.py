import pygame
from pygame.locals import *

import itertools

import core.constants as const
from core.maps import MapController
import core.setup as setup

# TODO: Explore using the mass of a sprite to impact landing force, so mass * gravity indicates what happens when something falls onto something else
# TODO: Make framerate independent movements with pygame.time.Clock()
# TODO: Figure out system for interacting with an NPC. How to detect if player is close enough? Circle collision?


class Game:
    def __init__(self):
        # Pygame setup
        self.screen: pygame.Surface = pygame.display.set_mode(const.SCREEN_SIZE)
        pygame.display.set_caption("Adventurers!")

        # Used for making movement framerate-independent.
        self.clock = pygame.time.Clock()

        # Game sprites and obstacles setup
        self.player = setup.setup_player()
        self.map = setup.setup_maps()
        self.map.render()

        # self.map_sprite = MapController(os.path.join("maps", "world_1.map"))
        # self.map_sprite.render()

        self.inventory_active = False

        self.screen_boundaries = [
            pygame.Rect(-50,                0,                   50,                 const.SCREEN_HEIGHT),  # left boundary
            pygame.Rect(0,                  const.SCREEN_HEIGHT, const.SCREEN_WIDTH, 50),                   # bottom
            pygame.Rect(const.SCREEN_WIDTH, 0,                   50,                 const.SCREEN_HEIGHT),  # right
            pygame.Rect(0,                  -50,                 const.SCREEN_WIDTH, 50),                   # top
        ]

        self.platforms = [
            pygame.Rect(0, 400, 400, 50) # Left platform in the air
        ]

    def run(self):
        print(self.map.map_image.get_size())

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_i:
                        self.inventory_active = not self.inventory_active
                    if self.inventory_active:
                        self.player.inventory.update(event)

            time_delta = self.clock.tick()
            # print(self.clock.get_fps())
            print(time_delta)
            keys = pygame.key.get_pressed()

            prev_rect = None

            if not self.inventory_active:
                prev_rect = self.player.update(keys, self.screen_boundaries + self.platforms, time_delta)
                self.map.update(keys, time_delta)

            """ ******************* Drawing ******************* """
            if prev_rect is not None:
                # TODO: Figure out
                #  better way to blit a piece of the background image over player's previous position, is hardcoded
                #  currently to largest image size
                corner = prev_rect.x, prev_rect.y
                self.screen.blit(self.map.map_image, corner, area=Rect(corner, (132, 240)))

            self.map.draw(self.screen)
            self.player.draw(self.screen)

            for obstacle in (self.screen_boundaries + self.platforms):
                pygame.draw.rect(self.screen, const.WHITE, obstacle)

            pygame.draw.rect(self.screen, const.BLUE, pygame.Rect(self.player.rect.left, self.player.rect.top, 100, 100))

            if self.inventory_active:
                self.player.inventory.draw(self.screen)

            pygame.display.flip()


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
