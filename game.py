import os

import core.constants as const
import pygame
from core.maps import MapController
from core.sprites import Player, PlayerStates
from pygame.locals import *

BLACK = 0, 0, 0


class Game:
    def __init__(self):
        # self.screen_size = self.width, self.height = 800, 800
        self.screen: pygame.Surface = pygame.display.set_mode(const.SCREEN_SIZE)
        pygame.display.set_caption('Adventurers!')

        self.player = self.setup_player()
        self.background = self.setup_maps()

    ## Static for now, as we only return the player and don't change the class state
    @staticmethod
    def setup_player():

        def setup_ka():
            talking_seq = [2, 1, 2, 1, 0, 1, 2, 1]
            walk_right = [0, 1]
            walk_left = [0, 1]

            images_dir = 'ka'
            talk_dir = os.path.join(images_dir, '300')
            walk_right_dir = os.path.join(images_dir, 'walk_right')
            walk_left_dir = os.path.join(images_dir, 'walk_left')

            ka = Player(0, 0)
            ka.add_animation(PlayerStates.TALKING, talking_seq, talk_dir)
            ka.add_animation(PlayerStates.WALK_RIGHT, walk_right, walk_right_dir, move_animation=True)
            ka.add_animation(PlayerStates.WALK_LEFT, walk_left, walk_left_dir, move_animation=True)

            ka.set_active_state(PlayerStates.TALKING)

            return ka

        return setup_ka()

    @staticmethod
    def setup_maps():
        """ Only returns one map currently, might have to return dict with enum keys or an ordered map list in the future """

        def setup_map_1():
            map_1_path = os.path.join('maps', 'world_1.map')
            map_1_controller = MapController(map_1_path)
            map_1 = map_1_controller.render()

            return map_1

        return setup_map_1()

    def run(self):
        self.screen.blit(self.background, (0, 0))
        print(self.background.get_size())

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                    running = False

            keys = pygame.key.get_pressed()
            # self.screen.fill(BLACK)

            self.player.update(self.screen, keys)
            pygame.display.flip()


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
