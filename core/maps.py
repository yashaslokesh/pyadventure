import pygame
from pygame.locals import *

from enum import Enum, auto

from . import constants as const
from . import setup


class MapTile(Enum):
    FLOOR = auto()
    WALL = auto()

    @staticmethod
    def get_tile_from_string(tile_repr):
        if tile_repr == '_':
            return MapTile.FLOOR
        elif tile_repr == '#':
            return MapTile.WALL


class MapController(object):
    def __init__(self, filename):
        with open(filename) as f:
            map_config = f.readlines()
            map_config = list(map(lambda s: s.strip(), map_config))

        self.map = map_config

        self.tiles = setup.setup_tiles()
        self.obstacles = []

        self.tiling_size = self.tiled_width, self.tiled_height = len(self.map[0]), len(self.map)
        self.true_size = self.true_width, self.true_height = self.tiled_width * const.TILE_WIDTH, self.tiled_height * const.TILE_HEIGHT

        # Always renders automatically, when created.
        self._render()

    def _render(self):
        map_image = pygame.Surface(self.true_size)

        for y, line in enumerate(self.map):
            for x, sym in enumerate(line):
                tile = MapTile.get_tile_from_string(sym)
                tile_surf = self.tiles[tile]
                obs = map_image.blit(tile_surf, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))
                if tile == MapTile.WALL:
                    self.obstacles.append(obs)

        # Returns the configured background image
        self.map_image = map_image
        self.rect = self.map_image.get_rect()

    def update(self, keys, time_delta):
        move_speed = self._handle_input(keys, time_delta)

        self.obstacles = list(map(lambda r: r.move(move_speed), self.obstacles))

        self.rect = self.rect.move(move_speed)

        return move_speed

    def _handle_input(self, keys, time_delta):
        horz_scroll = 0
        vert_scroll = 0

        scroll_mag = const.WALKING_SPEED * (time_delta / 1000)

        # Move this map left to make it appear as if player is moving right
        if keys[K_RIGHT]:
            # if self.rect.x >= 0:
            if self.rect.x + self.true_width - scroll_mag >= const.SCREEN_WIDTH:
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
            if self.rect.y + self.true_height - scroll_mag >= const.SCREEN_HEIGHT:
                vert_scroll = -scroll_mag

        return horz_scroll, vert_scroll

    def draw(self, screen: pygame.Surface):
        screen.blit(self.map_image, self.rect)
