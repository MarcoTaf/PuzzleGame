from abc import ABC, abstractmethod
from Spritesheet import spritesheet
from enum import IntEnum
import Settings
from MyMaths import clamp, sign
from Tile import Tile_type

class Dir(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class entity(ABC):
    @abstractmethod
    def __init_values__():
        raise NotImplementedError

    @abstractmethod
    def execute_ai():
        raise NotImplementedError

    def __acquire_sprite_sheet__(self):
        self.__char_sheet__ = spritesheet(self.__sprite_name__, self.__sprite_size__)

    def __init__(self, location):
        self.__init_values__()
        self.__acquire_sprite_sheet__()
        self.location = location
        self.__last_dir__ = Dir.Down
        self.__current_frame__ = 0
        self.__current_sprite_coords__ = [self.__current_frame__, self.__last_dir__]
        self.HP = self.initial_hp
        

    def get_sprite(self):
        return self.__char_sheet__.get_sprite(self.__current_sprite_coords__)

    def __collision_check_player__(self, player_ent, new_location):
        if (((self.location[0] == player_ent.location[0]) or
             (new_location[0] == player_ent.location[0])) and
             ((self.location[1] == player_ent.location[1]) or
             (new_location[1] == player_ent.location[1]))):
             
             return True

        return False

    def move(self, dir, tile_layer, player_ent = None):
        room_boundries = (0, 0, Settings.TILE_AMOUNTS[0] - 1, Settings.TILE_AMOUNTS[1] - 1)
        
        move_directions = {
            Dir.Up: (0, -1),
            Dir.Right: (1, 0),
            Dir.Down: (0, 1),
            Dir.Left: (-1, 0)
        }

        move_result = move_directions.get(dir, "")
        new_location = [clamp(self.location[0] + move_result[0], room_boundries[0], room_boundries[2]),
        clamp(self.location[1] + move_result[1], room_boundries[1], room_boundries[3])]

        if type(self) == enemy_entity:
            if self.__collision_check_player__(player_ent, new_location):
                player_ent.take_damage(self.__attack_val__)
        
        if not tile_layer[new_location[0]][new_location[1]].get_tile_type() == Tile_type.Wall:
            self.location = new_location

        if tile_layer[self.location[0]][self.location[1]].get_tile_type() == Tile_type.Spikes:
            self.take_damage(1)

        self.__current_sprite_coords__[0] = (self.__current_sprite_coords__[0] + 1) % self.__max_anim_frames__ 
        self.__current_sprite_coords__[1] = dir

    def take_damage(self, amount: int = 1):
        self.HP = clamp(self.HP - amount, 0, 99999999)
        return self.HP

    def destroy(self):
        raise NotImplementedError



class player_entity(entity):
    def __init_values__(self):
        
        self.initial_hp = 10
        self.__sprite_name__ = "warrior_m.png"
        self.__sprite_size__ = (32, 36)
        self.__max_anim_frames__ = 3
        self.__attack_val__ = 0

    def execute_ai(self):
        print("Why are you trying to run the AI for the player?")
        raise NotImplementedError

class enemy_entity(entity):
    def __init_values__(self):
        self.initial_hp = 3
        self.__sprite_name__ = "ninja_m.png"
        self.__sprite_size__ = (32, 36)
        self.__max_anim_frames__ = 3
        self.__attack_val__ = 10
    
    def execute_ai(self, player_ent, tile_layer):
        coord_diff = (self.location[0] - player_ent.location[0], self.location[1] - player_ent.location[1])

        if (abs(coord_diff[0]) >= abs(coord_diff[1])):
            result =  2 + sign(coord_diff[0])
        else:
            result = 1 - sign(coord_diff[1])

        return self.move(result, tile_layer, player_ent)
