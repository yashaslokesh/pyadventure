import pygame
from pygame.locals import *

from configparser import ConfigParser
from enum import Enum

import core.constants as const
import core.setup as setup


class MapTileType(Enum):
    wall = "#"
    floor = "_"


class MapController(object):
    def __init__(self, filename):
        self.key = {}

        config = ConfigParser(comment_prefixes=";")
        config.read(filename)
        self.map = config.get("world", "map").split("\n")

        self.tiles = setup.setup_tiles()

        # Let config file specify for easy reading
        self.tiled_size = self.tiled_width, self.tiled_height = (
            len(self.map[0]),
            len(self.map),
        )

        self.full_size = self.full_width, self.full_height = (
            self.tiled_width * const.TILE_WIDTH,
            self.tiled_height * const.TILE_HEIGHT,
        )

        # print(f'Width: {self.width}, Height: {self.height}')

        # Parse through symbol specs
        for section in config.sections():
            # If length of the name of the section is 1, it's a tile
            if len(section) == 1:
                tile_specs = dict(config.items(section))

                tile_type = MapTileType(section)
                self.key[tile_type] = tile_specs

    def render(self) -> None:
        map_image = pygame.Surface(self.full_size)

        for y, line in enumerate(self.map):
            for x, sym in enumerate(line):
                tile_type = MapTileType(sym)
                tile_surf = self.tiles[tile_type]
                map_image.blit(tile_surf, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

        # Returns the configured background image
        self.map_image = map_image
        self.rect = self.map_image.get_rect()

    def update(self, keys, time_delta):
        move_speed = self._handle_input(keys, time_delta)

        self.rect = self.rect.move(move_speed)

    def _handle_input(self, keys, time_delta):
        horz_scroll = 0
        vert_scroll = 0

        scroll_mag = const.WALKING_SPEED * time_delta / 1000

        # Move this map left to make it appear as if player is moving right
        if keys[K_RIGHT]:
            # if self.rect.x >= 0:
            if self.rect.x + self.full_width - scroll_mag >= const.SCREEN_WIDTH:
                horz_scroll = -scroll_mag

        # Move surface right
        if keys[K_LEFT]:
            # if self.rect.x + self.rect.width <= const.SCREEN_WIDTH:
            if self.rect.x + scroll_mag <= 0:
                horz_scroll = scroll_mag

        # Move down
        if keys[K_UP]:
            # if self.rect.y + self.rect.height <= const.SCREEN_WIDTH:
            if self.rect.y + scroll_mag <= 0:
                vert_scroll = scroll_mag

        # Move up
        if keys[K_DOWN]:
            # if self.rect.y >= 0:
            if self.rect.y + self.full_height - scroll_mag >= const.SCREEN_HEIGHT:
                vert_scroll = -scroll_mag

        return horz_scroll, vert_scroll

    def draw(self, screen: pygame.Surface):
        screen.blit(self.map_image, self.rect)
