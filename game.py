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
        pygame.display.set_caption("Adventurers!")

        self.player = self.setup_player()
        self.background = self.setup_maps()

        self.map_sprite = MapController(os.path.join("maps", "world_1.map"))
        self.map_sprite.render()

    ## Static for now, as we only return the player and don't change the class state
    @staticmethod
    def setup_player():
        def setup_ka():
            talking_seq = [2, 1, 2, 1, 0, 1, 2, 1]
            walk_right = [0, 1]
            walk_left = [0, 1]

            images_dir = "ka"
            talk_dir = os.path.join(images_dir, "300")
            walk_right_dir = os.path.join(images_dir, "walk_right")
            walk_left_dir = os.path.join(images_dir, "walk_left")

            ka = Player(0, 0)
            ka.add_animation(PlayerStates.TALKING, talking_seq, talk_dir)
            ka.add_animation(
                PlayerStates.WALK_RIGHT, walk_right, walk_right_dir, move_animation=True
            )
            ka.add_animation(
                PlayerStates.WALK_LEFT, walk_left, walk_left_dir, move_animation=True
            )

            ka.set_active_state(PlayerStates.TALKING)

            return ka

        return setup_ka()

    @staticmethod
    def setup_maps():
        """ Only returns one map currently, might have to return dict with enum keys or an ordered map list in the future """

        def setup_map_1():
            map_1_path = os.path.join("maps", "world_1.map")
            map_1_controller = MapController(map_1_path)
            map_1 = map_1_controller.render()

            return map_1

        return setup_map_1()

    def run(self):
        # background_offset = x_offset, y_offset = -80, -80

        # self.map_sprite.map_image.scroll(dx= x_offset, dy= y_offset)

        self.screen.blit(self.map_sprite.map_image, (0, 0))
        print(self.background.get_size())

        self.inventory_active = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_i:
                        self.inventory_active = not self.inventory_active
                        print('Touched')
                    else:
                        print('Juo')
                        self.player.inventory.update(event)


            keys = pygame.key.get_pressed()
            # self.screen.fill(BLACK)

            # if keys[K_i]:

            #     print('Touched')

            if not self.inventory_active:

                prev_rect = self.player.update(keys)
            # self.background.update(keys)
                self.map_sprite.update(keys)



            if prev_rect is not None:
                # self.screen.blit(self.background, (prev_rect.x, prev_rect.y), area=prev_rect)
                ## TODO: Figure out better way to blit a piece of the background image over player's previous position, is hardcoded currently to largest image size
                corner = prev_rect.x, prev_rect.y
                self.screen.blit(self.background, corner, area=Rect(corner, (132, 240)))

            self.map_sprite.draw(self.screen)
            self.player.draw(self.screen)

            if self.inventory_active:
                self.player.inventory.draw(self.screen)

            pygame.display.flip()


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
