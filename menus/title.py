import pygame
from pygame import *
from lib.functions import *
from lib.input import *
from menus.menu import *
import fileinput

def display_title_screen(screen):
    title_screen = Surface(DISPLAY)
    title_menu = create_menu(['Start','Hiscores','Quit'], title_screen, (51,51,51), (51,51,51))
    title_menu.draw()
    screen.blit(title_screen, (0,0))
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    on_title = True
    while on_title:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    title_menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN or event.key == K_s:
                    title_menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN or event.key == K_SPACE:
                    if title_menu.list[title_menu.get_position()] == "Start":
                        retval = get_player_name(screen)
                        if retval == "ESCAPE":
                            pass
                        else:
                            on_title = False
                            return retval
                    elif title_menu.list[title_menu.get_position()] == "Hiscores":
                        #on_title = False
                        display_hiscores_menu(screen, title_screen, title_menu)
                        title_menu = create_menu(['Start','Hiscores','Quit'], title_screen, (51,51,51), (51,51,51))
                    elif title_menu.list[title_menu.get_position()] == "Quit":
                        raise SystemExit, "QUIT"                       
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    raise SystemExit, "ESCAPE"
                title_menu.draw()
                screen.blit(title_screen, (0,0))
                pygame.display.update()
            elif event.type == QUIT: raise SystemExit, "QUIT" 
        pygame.time.wait(8)

def get_player_name(screen):
    name_entry_screen = Surface(DISPLAY)
    name_entry_screen.fill((51,51,51))
    screen.blit(name_entry_screen, (0,0))
    return ask(screen, "Name")

def display_hiscores_menu(screen, title_screen, title_menu):
    hiscores_menu_screen = Surface(DISPLAY)
    hiscores_menu = create_menu(['Fastest Time','Fastest in 1 Life','Least Deaths', 'Back'], hiscores_menu_screen, (51,51,51), (51,51,51))
    screen.blit(hiscores_menu_screen, (0,0))
    pygame.display.update()
    on_hiscores = True
    while on_hiscores:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    hiscores_menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN or event.key == K_s:
                    hiscores_menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN or event.key == K_SPACE:
                    if hiscores_menu.list[hiscores_menu.get_position()] == "Fastest Time":
                        display_timetrial_hiscores(screen)
                        hiscores_menu = create_menu(['Fastest Time','Fastest in 1 Life','Least Deaths', 'Back'], hiscores_menu_screen, (51,51,51), (51,51,51))
                    elif hiscores_menu.list[hiscores_menu.get_position()] == "Fastest in 1 Life":
                        #on_hiscores = False
                        display_life_timetrial_hiscores(screen)
                        hiscores_menu = create_menu(['Fastest Time','Fastest in 1 Life','Least Deaths', 'Back'], hiscores_menu_screen, (51,51,51), (51,51,51))
                    elif hiscores_menu.list[hiscores_menu.get_position()] == "Least Deaths":
                        #on_hiscores = False
                        display_least_deaths_hiscores(screen)
                        hiscores_menu = create_menu(['Fastest Time','Fastest in 1 Life','Least Deaths', 'Back'], hiscores_menu_screen, (51,51,51), (51,51,51))
                    elif hiscores_menu.list[hiscores_menu.get_position()] == "Back":
                        on_hiscores = False
                        return "Back"                      
                if event.key == K_ESCAPE:
                        on_hiscores = False
                        return "Back"
                screen.blit(hiscores_menu_screen, (0,0))
                pygame.display.update()
            elif event.type == QUIT: raise SystemExit, "QUIT" 
        pygame.time.wait(8)



def display_least_deaths_hiscores(screen):
    scores = []
    menu_height = 0
    menu_width = 0
    i = 0
    with open("assets/hiscores/hiscores_least_deaths.txt", "r") as infile:
        lines = infile.readlines()
        for line in lines:
            scores.append(Field())
            line_array = line.split(':')
            scores[i].level = line_array[0]
            scores[i].score = line_array[1]
            scores[i].name = line_array[2]
            scores[i].text = scores[i].level + " :  " +  scores[i].score + " : " + scores[i].name
            scores[i].field = scores[i].font.render(scores[i].text, 1, scores[i].color_text)
            scores[i].field_rect = scores[i].field.get_rect()
            menu_height += scores[i].field_rect.height
            if menu_width < scores[i].field_rect.width:
                menu_width = scores[i].field_rect.width
            i += 1

    life_hiscore_screen = Surface(DISPLAY)
    menu = pygame.Surface((menu_width, menu_height))
    menu.fill((0,0,0))

    height = 0
    for i in xrange(len(lines)):
        menu.blit(scores[i].field, (scores[i].field_rect.x, scores[i].field_rect.y + height))
        height += scores[i].field_rect.height

    x = life_hiscore_screen.get_rect().centerx - menu_width / 2
    y = life_hiscore_screen.get_rect().centery - menu_height / 2

    for i in xrange(len(lines)):
        life_hiscore_screen.blit(menu, (x,y))
    back_button = Field()
    back_button.text = "Back"
    back_button.field = back_button.font.render(back_button.text, 1, back_button.color_text)
    back_button.field_rect = back_button.field.get_rect()
    life_hiscore_screen.blit(back_button.field, (0,0))
    screen.blit(life_hiscore_screen, (0,0))
    pygame.display.update()
    
    on_hiscores = True
    while on_hiscores:
        for event in pygame.event.get():
            if event.type == KEYDOWN:                    
                if event.key == K_ESCAPE or event.key == K_RETURN or event.key == K_SPACE:
                    on_hiscores = False
                    return "Back"
                else:
                    screen.blit(hiscore_screen, (0,0))
                    pygame.display.update()
            elif event.type == QUIT: raise SystemExit, "QUIT" 
        pygame.time.wait(8)


def display_life_timetrial_hiscores(screen):
    scores = []
    menu_height = 0
    menu_width = 0
    i = 0
    with open("assets/hiscores/hiscores_life_timetrials.txt", "r") as infile:
        lines = infile.readlines()
        for line in lines:
            scores.append(Field())
            line_array = line.split(':')
            scores[i].level = line_array[0]
            scores[i].score = convert_time(int(line_array[1]))
            scores[i].name = line_array[2]
            scores[i].text = scores[i].level + " :  " +  scores[i].score + " : " + scores[i].name
            scores[i].field = scores[i].font.render(scores[i].text, 1, scores[i].color_text)
            scores[i].field_rect = scores[i].field.get_rect()
            menu_height += scores[i].field_rect.height
            if menu_width < scores[i].field_rect.width:
                menu_width = scores[i].field_rect.width
            i += 1

    life_hiscore_screen = Surface(DISPLAY)
    menu = pygame.Surface((menu_width, menu_height))
    menu.fill((0,0,0))

    height = 0
    for i in xrange(len(lines)):
        menu.blit(scores[i].field, (scores[i].field_rect.x, scores[i].field_rect.y + height))
        height += scores[i].field_rect.height

    x = life_hiscore_screen.get_rect().centerx - menu_width / 2
    y = life_hiscore_screen.get_rect().centery - menu_height / 2

    for i in xrange(len(lines)):
        life_hiscore_screen.blit(menu, (x,y))
    back_button = Field()
    back_button.text = "Back"
    back_button.field = back_button.font.render(back_button.text, 1, back_button.color_text)
    back_button.field_rect = back_button.field.get_rect()
    life_hiscore_screen.blit(back_button.field, (0,0))
    screen.blit(life_hiscore_screen, (0,0))
    pygame.display.update()
    
    on_hiscores = True
    while on_hiscores:
        for event in pygame.event.get():
            if event.type == KEYDOWN:                    
                if event.key == K_ESCAPE or event.key == K_RETURN or event.key == K_SPACE:
                    on_hiscores = False
                    return "Back"
                else:
                    screen.blit(hiscore_screen, (0,0))
                    pygame.display.update()
            elif event.type == QUIT: raise SystemExit, "QUIT" 
        pygame.time.wait(8)

def display_timetrial_hiscores(screen):
    scores = []
    menu_height = 0
    menu_width = 0
    i = 0
    with open("assets/hiscores/hiscores_timetrials.txt", "r") as infile:
        lines = infile.readlines()
        for line in lines:
            scores.append(Field())
            line_array = line.split(':')
            scores[i].level = line_array[0]
            scores[i].score = convert_time(int(line_array[1]))
            scores[i].name = line_array[2]
            scores[i].text = scores[i].level + " :  " +  scores[i].score + " : " + scores[i].name
            scores[i].field = scores[i].font.render(scores[i].text, 1, scores[i].color_text)
            scores[i].field_rect = scores[i].field.get_rect()
            menu_height += scores[i].field_rect.height
            if menu_width < scores[i].field_rect.width:
                menu_width = scores[i].field_rect.width
            i += 1

    timetrial_hiscore_screen = Surface(DISPLAY)
    menu = pygame.Surface((menu_width, menu_height))
    menu.fill((0,0,0))

    height = 0
    for i in xrange(len(lines)):
        menu.blit(scores[i].field, (scores[i].field_rect.x, scores[i].field_rect.y + height))
        height += scores[i].field_rect.height

    x = timetrial_hiscore_screen.get_rect().centerx - menu_width / 2
    y = timetrial_hiscore_screen.get_rect().centery - menu_height / 2

    for i in xrange(len(lines)):
        timetrial_hiscore_screen.blit(menu, (x,y))
    back_button = Field()
    back_button.text = "Back"
    back_button.field = back_button.font.render(back_button.text, 1, back_button.color_text)
    back_button.field_rect = back_button.field.get_rect()
    timetrial_hiscore_screen.blit(back_button.field, (0,0))
    screen.blit(timetrial_hiscore_screen, (0,0))
    pygame.display.update()
    
    on_hiscores = True
    while on_hiscores:
        for event in pygame.event.get():
            if event.type == KEYDOWN:                    
                if event.key == K_ESCAPE or event.key == K_RETURN or event.key == K_SPACE:
                    on_hiscores = False
                    return "Back"
                else:
                    screen.blit(hiscore_screen, (0,0))
                    pygame.display.update()
            elif event.type == QUIT: raise SystemExit, "QUIT" 
        pygame.time.wait(8)

class Field:
    font_size = 32
    font_path = 'menus/data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font(font_path, font_size)
    color_text = (255, 255, 153)
    text = ''
    score = ''
    field = pygame.Surface
    field_rect = pygame.Rect