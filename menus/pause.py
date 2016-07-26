import pygame
from pygame import *
from menus.title import *

def display_pause_screen(screen, pause_screen):
    pause_menu = create_menu(['Resume', 'Main Menu', 'Quit'], pause_screen)
    pause_menu.draw()
    screen.blit(pause_screen, (0,0))
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    on_pause = True
    while on_pause:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    pause_menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN or event.key == K_s:
                    pause_menu.draw(1) #here is the Menu class function
                if event.key == K_p or event.key == K_ESCAPE:
                    on_pause = False
                if event.key == K_RETURN or event.key == K_SPACE:
                    if pause_menu.list[pause_menu.get_position()] == "Resume":
                        on_pause = False
                    if pause_menu.list[pause_menu.get_position()] == "Main Menu":
                        on_pause = False
                        # display_title_screen(screen)
                        return "main"
                    elif pause_menu.list[pause_menu.get_position()] == "Quit":
                        raise SystemExit("QUIT")
                screen.blit(pause_screen, (0,0))
                pygame.display.update()
            elif event.type == QUIT:
                raise SystemExit("QUIT")
        pygame.time.wait(8)