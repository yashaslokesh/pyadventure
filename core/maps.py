from configparser import ConfigParser
from enum import Enum

import core.constants as const
import pygame


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
        self.width = config.getint("world", "width")
        self.height = config.getint("world", "height")

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
        map_image = pygame.Surface(const.SCREEN_SIZE)

        for y, line in enumerate(self.map):
            for x, sym in enumerate(line):
                tile_type = MapTileType(sym)
                tile_surf = self.tiles[tile_type]
                map_image.blit(tile_surf, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

        ## Returns the configured background image
        return map_image
