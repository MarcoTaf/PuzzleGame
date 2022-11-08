import pygame
from Room import room
import Settings
import Renderer
import Entities


def process_player_input(input):
    if input.key == pygame.K_UP or input.key == pygame.K_w:
        return 0
    elif input.key == pygame.K_RIGHT or input.key == pygame.K_d:
        return 1
    elif input.key == pygame.K_DOWN or input.key == pygame.K_s:
        return 2
    elif input.key == pygame.K_LEFT or input.key == pygame.K_a:
        return 3 
   
def generate_new_room(player, renderer):
    new_room = room(player)
    renderer.flag_update_tile_surf()
    return new_room

def show_GO_screen():
    GO_loop = True
    while GO_loop:
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN or i.type == pygame.QUIT:
                GO_loop = False
                break


def play_game():

    run = True
    pygame.init()
    renderer = Renderer.renderer()
    clock = pygame.time.Clock()
    player_ent = Entities.player_entity([0,0])
    last_player_input = None
    make_new_room = False
    score = 0
    #entity_list = Entities.entity_list(Entities.player_entity)

    room_obj = generate_new_room(player_ent, renderer)

    
    while run == True:
        
        clock.tick(Settings.TARGET_FPS)

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                last_player_input = process_player_input(i)

            if i.type == pygame.QUIT:
                run = False
            
        last_player_input, make_new_room, score  = room_obj.execute_entities(last_player_input, score, renderer)

        if make_new_room:
            room_obj = generate_new_room(player_ent, renderer)
    
        renderer.run_updates(room_obj, score)
        renderer.draw_to_screen()   

        if player_ent.HP <= 0:
            renderer.draw_GO(score)
            show_GO_screen()
            run = False
            break

    pygame.quit()

if __name__ == "__main__":
    play_game()