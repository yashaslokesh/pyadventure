import os
import core.constants as const
import pygame
from core.maps import MapController
from core.sprites import Player, PlayerStates
from pygame.locals import *

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"


def setup_npc():
    pass


class Game:
    def __init__(self):
        # self.screen_size = self.width, self.height = 800, 800
        self.screen: pygame.Surface = pygame.display.set_mode(const.SCREEN_SIZE)
        pygame.display.set_caption("Adventurers!")

        self.player = self.setup_player()
        self.background = self.setup_maps()

        self.map_sprite = MapController(os.path.join("maps", "world_1.map"))
        self.map_sprite.render()

        self.inventory_active = False

        self.screen_boundaries = [
            pygame.Rect(-50,                0,                   50,                 const.SCREEN_HEIGHT),  # left boundary
            pygame.Rect(0,                  const.SCREEN_HEIGHT, const.SCREEN_WIDTH, 50),                   # bottom
            pygame.Rect(const.SCREEN_WIDTH, 0,                   50,                 const.SCREEN_HEIGHT),  # right
            pygame.Rect(0,                  -50,                 const.SCREEN_WIDTH, 50),                   # top

            pygame.Rect(0, 400, 400, 50)
        ]

    ## Static for now, as we only return the player and don't change the class state
    @staticmethod
    def setup_player():
        talking_seq = [2, 1, 2, 1, 0, 1, 2, 1]
        walk_right = [0, 1]
        walk_left = [0, 1]

        images_dir = "ka"
        talk_dir = os.path.join(images_dir, "talking")
        walk_right_dir = os.path.join(images_dir, "walk_right")
        walk_left_dir = os.path.join(images_dir, "walk_left")

        ka = Player()
        ka.add_animation(PlayerStates.TALKING, talking_seq, talk_dir)
        ka.add_animation(
            PlayerStates.WALK_RIGHT, walk_right, walk_right_dir, move_animation=True
        )
        ka.add_animation(
            PlayerStates.WALK_LEFT, walk_left, walk_left_dir, move_animation=True
        )

        ## TODO: Add custom jump anim
        ka.add_animation(PlayerStates.JUMPING, talking_seq, talk_dir)

        ka.active_state = PlayerStates.WALK_RIGHT

        return ka


    @staticmethod
    def setup_maps():
        """ Only returns one map currently, might have to return dict with enum keys or an ordered map list in the
        future """

        def setup_map_1():
            map_1_path = os.path.join("maps", "world_1.map")
            map_1_controller = MapController(map_1_path)
            map_1 = map_1_controller.render()

            return map_1

        return setup_map_1()

    def run(self):
        self.screen.blit(self.map_sprite.map_image, (0, 0))
        print(self.background.get_size())

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

            keys = pygame.key.get_pressed()

            prev_rect = None

            if not self.inventory_active:
                prev_rect = self.player.update(keys, self.screen_boundaries)
                # self.background.update(keys)
                self.map_sprite.update(keys)

            if prev_rect is not None:
                # self.screen.blit(self.background, (prev_rect.x, prev_rect.y), area=prev_rect)
                # TODO: Figure out
                #  better way to blit a piece of the background image over player's previous position, is hardcoded
                #  currently to largest image size
                corner = prev_rect.x, prev_rect.y
                self.screen.blit(self.background, corner, area=Rect(corner, (132, 240)))

            self.map_sprite.draw(self.screen)
            self.player.draw(self.screen)

            for bound in self.screen_boundaries:
                pygame.draw.rect(self.screen, const.WHITE, bound)

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
