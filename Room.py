from Tile import tile, Tile_type
from random import randint, randrange
import Settings
import Entities

class room():
    
    @staticmethod
    def decide_new_tile_type(max_val = 100):
        new_tile_RNG = randint(1, max_val)

        if new_tile_RNG < Settings.WALLTHRESHOLD:
            return Tile_type.Floor.value
        elif new_tile_RNG >= Settings.WALLTHRESHOLD and new_tile_RNG < Settings.SPIKESTHRESHOLD:
            return Tile_type.Wall.value
        elif new_tile_RNG >= Settings.SPIKESTHRESHOLD:
            return Tile_type.Spikes.value

    def __init__(self, player_ent):
        self.__room_size__ = Settings.TILE_AMOUNTS
        self.room_tiles = []
        self.entity_list = []
        self.player_ent = player_ent
        self.__execute_timer__ = 0
        self.__generate_room_tiles()
        

    def spawn_ent(self, location):
        self.entity_list.append(Entities.enemy_entity(location))

    def __find_rand_spawn__(self, array, dist_from_player: bool = False):
        location = array.pop(randrange(len(array)))
        
        while dist_from_player:
            if (abs(self.player_ent.location[0] - location[0]) +
            abs(self.player_ent.location[1] -  location[1]) >= Settings.SPAWN_DIST_FROM_PLAYER):
                break
            
            location = array.pop(randrange(len(array)))


        return location
            

    def __generate_room_tiles(self):
        valid_spawn_array = []
        for w in range(self.__room_size__[0]):
            new_array = []
            for h in range(self.__room_size__[1]):
                new_tile = tile(type(self).decide_new_tile_type())
                if new_tile.get_tile_type() == Tile_type.Floor.value:
                    valid_spawn_array.append([w, h])

                new_array.append(new_tile)
            self.room_tiles.append(new_array)

        self.player_ent.location = self.__find_rand_spawn__(valid_spawn_array)

        room_spawn_amount = randint(*Settings.ENEMY_SPAWN_RATE)
        for i in range(room_spawn_amount):
            self.spawn_ent(self.__find_rand_spawn__(valid_spawn_array, True))

        

    def execute_entities(self, player_input, score, renderer):
        make_new_room = False
        self.__execute_timer__ +=1
        if self.__execute_timer__ == Settings.EXECUTION_TIMER:
            self.__execute_timer__ = 0
            renderer.flag_update_entity_surf()

            if not player_input == None:
                self.player_ent.move(player_input, self.room_tiles)
                player_input = None
            

            i = 0
            while i < (len(self.entity_list)):
                current_entity = self.entity_list[i]
                current_entity.execute_ai(self.player_ent, self.room_tiles)

                if current_entity.HP <= 0:
                    self.entity_list.pop(i)
                    score += 1

                    if len(self.entity_list) <= 0:
                        make_new_room = True
                        break
    

                    continue

                i+= 1
        return player_input, make_new_room, score