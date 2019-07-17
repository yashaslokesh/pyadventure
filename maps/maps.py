from configparser import ConfigParser

class MapController(object):
    def __init__(self, filename):
        self.key = {}

        config = ConfigParser(comment_prefixes=';')
        config.read(filename)
        self.map = config.get('world', 'map').split('\n')
        ## Number of rows gives the height
        self.width = len(self.map[0])
        self.height = len(self.map)

        ## Parse through symbol specs
        for section in config.sections():
            ## If length of the name of the section is 1, it's a tile
            if len(section) == 1:
                tile_specs = dict(config.items(section))
                self.key[section] = tile_specs

        ## Pass in coordinates of a tile in order to get specs for that location
        def get_tile(self, x, y):
            try:
                char = self.map[y][x]
            except IndexError:
                return {}
            try:
                return self.key[char]
            except KeyError:
                return {}

        def get_bool(self, x, y, spec_name):
            b = self.get_tile(x, y).get(spec_name)

            return b in ('True', 'true', 'on', '1', 'yes')

        def is_wall(self, x, y):
            return self.get_bool(x, y, 'wall')

        def is_blocking(self, x, y):
            if not (0 <= x < self.width and 0 <= y < self.height):
                return True
            return self.get_bool(x, y, 'block')