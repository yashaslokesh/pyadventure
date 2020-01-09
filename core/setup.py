import pygame

import os

from . import sprites
from . import maps
from . import constants as const

os.environ["SDL_VIDEO_WINDOW_POS"] = "500,0"


def setup_player():
    talking_seq = [2, 1, 2, 1, 0, 1, 2, 1]
    walk_right = [0, 1]
    walk_left = [0, 1]

    images_dir = "ka"
    talk_dir = os.path.join(images_dir, "talking")
    walk_right_dir = os.path.join(images_dir, "walk_right")
    walk_left_dir = os.path.join(images_dir, "walk_left")

    ka = sprites.Player(x=500, y=600, scale=0.15)
    ka.add_animation(sprites.PlayerStates.TALKING, talking_seq, talk_dir)
    ka.add_animation(
        sprites.PlayerStates.WALK_RIGHT, walk_right, walk_right_dir, move_animation=True
    )
    ka.add_animation(
        sprites.PlayerStates.WALK_LEFT, walk_left, walk_left_dir, move_animation=True
    )

    # TODO: Add custom jump anim
    ka.add_animation(sprites.PlayerStates.JUMPING, talking_seq, talk_dir)

    # TODO: Add custom falling anim
    ka.add_animation(sprites.PlayerStates.FALLING, talking_seq, talk_dir)

    ka.active_state = sprites.PlayerStates.FALLING

    return ka


def setup_tiles():
    red_tile = pygame.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
    green_tile = pygame.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))

    red_tile.fill(pygame.Color(255, 0, 0))
    green_tile.fill(pygame.Color(0, 255, 0))

    tiles = {maps.MapTile.WALL: red_tile, maps.MapTile.FLOOR: green_tile}
    return tiles


def setup_maps():
    """ TODO: Only returns one map currently, might have to return dict with enum keys or an ordered map list in the
         future """

    def setup_map_1():
        map_1_path = os.path.join("maps", "world_1.map")
        map_1_controller = maps.MapController(map_1_path)

        return map_1_controller

    def setup_map_2():
        map_2_path = os.path.join("maps", "world_2.map")
        map_2_controller = maps.MapController(map_2_path)

        return map_2_controller

    return {1: setup_map_1(), 2: setup_map_2()}

