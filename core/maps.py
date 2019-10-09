from configparser import ConfigParser
from enum import Enum

import core.constants as const
import pygame

from pygame.locals import *


class MapTileType(Enum):
    wall = "#"
    floor = "_"


class MapController(object):
    def __init__(self, filename):
        self.key = {}

        config = ConfigParser(comment_prefixes=";")
        config.read(filename)
        self.map = config.get("world", "map").split("\n")

        ##
        self.tiles = MapController.setup_tiles()

        ## Let config file specify for easy reading
        self.tiled_size = self.tiled_width, self.tiled_height = (
            len(self.map[0]),
            len(self.map),
        )

        self.full_size = self.full_width, self.full_height = (
            self.tiled_width * const.TILE_WIDTH,
            self.tiled_height * const.TILE_HEIGHT,
        )

        # print(f'Width: {self.width}, Height: {self.height}')

        ## Parse through symbol specs
        for section in config.sections():
            ## If length of the name of the section is 1, it's a tile
            if len(section) == 1:
                tile_specs = dict(config.items(section))

                tile_type = MapTileType(section)
                self.key[tile_type] = tile_specs

    @staticmethod
    def setup_tiles():
        red_tile = pygame.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
        green_tile = pygame.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))

        red_tile.fill(pygame.Color(255, 0, 0))
        green_tile.fill(pygame.Color(0, 255, 0))

        tiles = {MapTileType.wall: red_tile, MapTileType.floor: green_tile}
        return tiles

    def render(self) -> pygame.Surface:
        map_image = pygame.Surface(self.full_size)

        for y, line in enumerate(self.map):
            for x, sym in enumerate(line):
                tile_type = MapTileType(sym)
                tile_surf = self.tiles[tile_type]
                map_image.blit(tile_surf, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

        ## Returns the configured background image
        self.map_image = map_image
        self.rect = self.map_image.get_rect()
        return map_image

    def draw(self, screen: pygame.Surface):
        screen.blit(self.map_image, self.rect)

    def _handle_input(self, keys):
        horz_scroll = 0
        vert_scroll = 0

        # Move this map left to make it appear as if player is moving right
        if keys[K_RIGHT]:
            # if self.rect.x >= 0:
            if self.rect.x + self.full_width - 5 >= const.SCREEN_WIDTH:
                horz_scroll = -5

        # Move surface right
        if keys[K_LEFT]:
            # if self.rect.x + self.rect.width <= const.SCREEN_WIDTH:
            if self.rect.x + 5 <= 0:
                horz_scroll = 5

        # Move down
        if keys[K_UP]:
            # if self.rect.y + self.rect.height <= const.SCREEN_WIDTH:
            if self.rect.y + 5 <= 0:
                vert_scroll = 5

        # Move up
        if keys[K_DOWN]:
            # if self.rect.y >= 0:
            if self.rect.y + self.full_height - 5 >= const.SCREEN_HEIGHT:
                vert_scroll = -5

        return [horz_scroll, vert_scroll]

    def update(self, keys):
        move_speed = self._handle_input(keys)

        self.rect = self.rect.move(move_speed)
