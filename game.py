import pygame
from pygame.locals import *

import core.constants as const
from core.maps import MapController
import core.setup as setup

# TODO: Explore using the mass of a sprite to impact landing force, so mass * gravity indicates what happens when something falls onto something else
# TODO: Figure out system for interacting with an NPC. How to detect if player is close enough? Circle collision?


class Game:
    def __init__(self):
        # Pygame setup
        # self.screen = pygame.display.set_mode(const.SCREEN_SIZE)
        self.screen = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Adventurers!")

        # Used for making movement framerate-independent.
        self.clock = pygame.time.Clock()

        # Game sprites and obstacles setup
        self.player = setup.setup_player()
        self.maps = setup.setup_maps()
        self.active_map = 2

        self.inventory_active = False

        self.screen_boundaries = [
            pygame.Rect(-50,                0,                   50,                 const.SCREEN_HEIGHT),  # left boundary
            pygame.Rect(0,                  const.SCREEN_HEIGHT, const.SCREEN_WIDTH, 50),                   # bottom
            pygame.Rect(const.SCREEN_WIDTH, 0,                   50,                 const.SCREEN_HEIGHT),  # right
            pygame.Rect(0,                  -50,                 const.SCREEN_WIDTH, 50),                   # top
        ]

        self.platforms = [
            # pygame.Rect(0, 600, 300, 30),  # Left platform in the air
            # pygame.Rect(500, 600, 300, 30)  # Left platform in the air
        ]

    def run(self):
        print(self.maps[self.active_map].map_image.get_size())

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_i:
                        self.inventory_active = not self.inventory_active
                    if event.key == K_l:
                        print()
                        print('Current center:', self.player.rect.center, 'Current top-left:', self.player.rect.topleft)
                        print('Active state:', self.player.active_state)
                        print('Collisions:', self.player.collisions)
                    if event.key == K_p:
                        print('Obstacle coords:', self.maps[self.active_map].obstacles)
                    if self.inventory_active:
                        self.player.inventory.update(event)

            time_delta = self.clock.tick()
            keys = pygame.key.get_pressed()

            prev_rect = None

            if not self.inventory_active:
                self.maps[self.active_map].update(keys, time_delta)

            obstacles = self.maps[self.active_map].obstacles

            if not self.inventory_active:
                prev_rect = self.player.update(keys, self.screen_boundaries + obstacles, time_delta)

            """ ******************* Drawing ******************* """
            # if prev_rect is not None:
            #     # TODO: Figure out
            #     #  better way to blit a piece of the background image over player's previous position, is hardcoded
            #     #  currently to largest image size
            #     corner = prev_rect.x, prev_rect.y
            #     self.screen.blit(self.maps[self.active_map].map_image, corner, area=Rect(corner, (132, 240)))

            self.maps[self.active_map].draw(self.screen)
            self.player.draw(self.screen)

            obstacles = self.maps[self.active_map].obstacles

            for obstacle in obstacles:
                pygame.draw.rect(self.screen, const.WHITE, obstacle)

            if self.inventory_active:
                self.player.inventory.draw(self.screen)

            # TODO: Change this line to pygame.display.update() with a rectangle list passed in to optimize drawing.
            pygame.display.flip()


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
