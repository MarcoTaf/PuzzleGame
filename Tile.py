import enum
from Settings import WINDOW_SIZE, TILE_AMOUNTS

class Tile_type(enum.IntEnum):
    Floor = 0
    Wall = 1
    Spikes = 2

class tile():
    @staticmethod
    def define_tile_size():
        return (WINDOW_SIZE[0] / TILE_AMOUNTS[0], WINDOW_SIZE[1] / TILE_AMOUNTS[1])

    @staticmethod
    def acquire_tile_boundries(coords):
        tile_size = tile.define_tile_size()
        return((tile_size[0] * coords[0], tile_size[1] * coords[1], tile_size[0] * (coords[0] + 1) - 1,
        tile_size[1] * (coords[1] + 1) - 1)) #x1, y1, x2, y2

    def __init__(self, t_type):
        self.__tile_type__ = t_type
        self.__tile_entity__ = None

    def swap_tile(self,t_type):
        self.__tile_type__ = t_type

    def get_tile_type(self):
        return self.__tile_type__

    def get_tile_entity(self):
        return self.__tile_entity__

    def set_tile_entity(self, entity):
        self.__tile_entity__ = entity

    def move_tile_entity(self, other):
        if other.get_tile_entity() == None:
            other.set_tile_entity(self.get_tile_entity())
            self.set_tile_entity(None)
            return True
        
        return False

