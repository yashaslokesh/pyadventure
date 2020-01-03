import pygame

import os

import core.sprites as sprites
import core.maps as maps
import core.constants as const

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"


def setup_player():
    talking_seq = [2, 1, 2, 1, 0, 1, 2, 1]
    walk_right = [0, 1]
    walk_left = [0, 1]

    images_dir = "ka"
    talk_dir = os.path.join(images_dir, "talking")
    walk_right_dir = os.path.join(images_dir, "walk_right")
    walk_left_dir = os.path.join(images_dir, "walk_left")

    ka = sprites.Player()
    ka.add_animation(sprites.PlayerStates.TALKING, talking_seq, talk_dir)
    ka.add_animation(
        sprites.PlayerStates.WALK_RIGHT, walk_right, walk_right_dir, move_animation=True
    )
    ka.add_animation(
        sprites.PlayerStates.WALK_LEFT, walk_left, walk_left_dir, move_animation=True
    )

    # TODO: Add custom jump anim
    ka.add_animation(sprites.PlayerStates.JUMPING, talking_seq, talk_dir)

    ka.active_state = sprites.PlayerStates.WALK_RIGHT

    return ka


def setup_tiles():
    red_tile = pygame.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
    green_tile = pygame.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))

    red_tile.fill(pygame.Color(255, 0, 0))
    green_tile.fill(pygame.Color(0, 255, 0))

    tiles = {maps.MapTileType.wall: red_tile, maps.MapTileType.floor: green_tile}
    return tiles


def setup_maps() -> maps.MapController:
    """ TODO: Only returns one map currently, might have to return dict with enum keys or an ordered map list in the
         future """

    def setup_map_1() -> maps.MapController:
        map_1_path = os.path.join("maps", "world_1.map")
        map_1_controller = maps.MapController(map_1_path)
        map_1_controller.render()

        return map_1_controller

    return setup_map_1()

