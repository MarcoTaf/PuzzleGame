import pygame
import os
import Settings
from Tile import tile
from Colors import COL_BLACK_0_ALPHA

class spritesheet():
    @staticmethod
    def create_alpha_surf(size):
        surf = pygame.Surface(size).convert_alpha()#WHY DO I HAVE TO DO THIS??? WHY IN THE HELL DO I NOT JUST HAVE THE SURFACE START OUT WITH AN ALPHA OF 0??? WHY????????????????????????????????????????????????????????++
        surf.fill(COL_BLACK_0_ALPHA)
        return surf

    def __init__(self, asset_name, sprite_size):
        self.__sheet__ = pygame.image.load(os.path.join(Settings.FOLDERPATH , "assets" , str(asset_name))).convert_alpha()
        self.__sprite_size__ = sprite_size
        self.__sheet_size__ = (self.__sheet__.get_width(), self.__sheet__.get_height())

    def get_sprite(self, coord):
        
        surf = type(self).create_alpha_surf(self.__sprite_size__)
        surf.blit(self.__sheet__, (-(coord[0] * self.__sprite_size__[0]), -(coord[1] * self.__sprite_size__[1])))
        tras_surf = pygame.transform.scale(surf, tile.define_tile_size())
        return tras_surf