from turtle import screensize
import pygame
import Settings
from Tile import Tile_type, tile
from Spritesheet import spritesheet
from Colors import COL_WHITE_0_ALPHA, COL_WHITE, COL_BLACK, COL_RED

class renderer():
    def draw_tile_borders(self):
        surf_size = self.__tile_surf__.get_size()

        tile_width = surf_size[0] / Settings.TILE_AMOUNTS[0]
        tile_height = surf_size[1] / Settings.TILE_AMOUNTS[1]

        line_color = (0, 0, 0)
        for w in range(Settings.TILE_AMOUNTS[0]):
            pygame.draw.line(self.__tile_surf__, line_color,(w*tile_width, 0), 
            (w*tile_width, surf_size[1]), 1)
            pygame.draw.line(self.__tile_surf__, line_color,((w + 1)*tile_width - 1, 0), 
            ((w + 1)*tile_width - 1, surf_size[1]), 1)

        for h in range(Settings.TILE_AMOUNTS[1]):
            pygame.draw.line(self.__tile_surf__, line_color,(0, h*tile_height), 
            (surf_size[0], h*tile_height), 1)
            pygame.draw.line(self.__tile_surf__, line_color,(0, (h + 1)*tile_height - 1), 
            (surf_size[0], (h + 1)*tile_height - 1), 1)

    def draw_tile_backgrounds(self, room_array):
        tile_coords = {
            Tile_type.Floor: self.tile_sheet.get_sprite((0, 0)),
            Tile_type.Wall: self.tile_sheet.get_sprite((6, 0)),
            Tile_type.Spikes: self.tile_sheet.get_sprite((5, 0))
        }

        tile_size = tile.define_tile_size()
        for width in range(len(room_array.room_tiles)):
            current_array = room_array.room_tiles[width]
            for height in range(len(current_array)):
                current_tile = current_array[height]
                
                self.__tile_surf__.blit(tile_coords.get(current_tile.get_tile_type(), ""),
                (width*tile_size[0], height*tile_size[1])) #Now that's a line and a half
                    
    def __init__(self):
        #if pygame.display.get_init():
            #return False            
        self.__update_tile_surf__ = True
        self.__update_entity_surf__ = True
        self.__window__ = pygame.display.set_mode(Settings.WINDOW_SIZE)
        self.__tile_surf__ = pygame.Surface(Settings.WINDOW_SIZE)
        self.__entity_surf__ = pygame.Surface(Settings.WINDOW_SIZE).convert_alpha()
        self.__font__ = pygame.font.SysFont(None, 48)
        self.tile_sheet = spritesheet("cave.png", (24, 24))

    def flag_update_tile_surf(self):
        self.__update_tile_surf__ = True

    def flag_update_entity_surf(self):
        self.__update_entity_surf__ = True

    def draw_ent(self, ent):
        location = tile.acquire_tile_boundries(ent.location)
        self.__entity_surf__.blit(ent.get_sprite(), (location[0], location[1]))

    def __draw_hp__(self, ent):
    
        location = tile.acquire_tile_boundries(ent.location)
        new_loc = [location[0], location[1], (location[2] - location[0]), ((location[3] - location[1])/ 10)]
        pygame.draw.rect(self.__entity_surf__, COL_BLACK, new_loc)
        new_loc[2] = new_loc[2] * (ent.HP/ ent.initial_hp)
        pygame.draw.rect(self.__entity_surf__, COL_RED, new_loc)

    def __draw_score__(self, score):
        text_obj = self.__font__.render("Score: " + str(score), 1, COL_WHITE)
        text_rect = text_obj.get_rect()
        self.__window__.blit(text_obj, text_rect)

    def draw_GO(self, score):
        text_obj = self.__font__.render("You died! Your score was : " + str(score) + ". Press any key to exit", 2, (255, 255, 255, 255)) #WHY DOES THE NEWLINE CHARACTER NOT WORK!?!?!?!?!?! AAAAAAAAAAAAAAAAA What even is this font?
        text_rect = text_obj.get_rect()
        screen_size = self.__window__.get_size()
        text_rect[0] = (screen_size[0]/2) - (text_rect[2]/2)
        text_rect[1] = (screen_size[1]/2) - (text_rect[3]/2)
        self.__window__.blit(text_obj, text_rect)
        self.draw_to_screen()

    def __execute_update_entity_surf__(self, room_obj, score):
        self.__window__.blit(self.__tile_surf__,(0,0))
        self.__entity_surf__.fill(COL_WHITE_0_ALPHA)
        self.draw_ent(room_obj.player_ent)
        self.__draw_hp__(room_obj.player_ent)
        self.__draw_score__(score)
    
        for i in room_obj.entity_list:
            self.draw_ent(i)
            self.__draw_hp__(i)

        self.__window__.blit(self.__entity_surf__,(0,0))
        

    def __execute_update_tile_surf__(self, room_array):
        self.__tile_surf__.fill(COL_WHITE_0_ALPHA)
        self.draw_tile_backgrounds(room_array)
        self.draw_tile_borders()
        self.__window__.blit(self.__tile_surf__,(0,0))


    def run_updates(self, room_array, score):
        if self.__update_tile_surf__:
            self.__execute_update_tile_surf__(room_array)
            self.__update_tile_surf__ = False

        if self.__update_entity_surf__:
            self.__execute_update_entity_surf__(room_array, score)
            self.__update_entity_surf__ = False

    def draw_to_screen(self):

        pygame.display.update()
        