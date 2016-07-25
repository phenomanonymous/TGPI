#! /usr/bin/python
# Written by Frank McCormick
# 7/7/14
######################################################
###################### IMPORTS #######################
######################################################
import os
import lib
import menus

from lib.blocks import *
from lib.entities import *
from lib.constants import *
from lib.functions import *
from lib.player import *
from lib.camera import *
from lib.spritesheet import *
from lib.level import *

from menus.menu import *
from menus.title import *
from menus.pause import *

from pygame import *

######################################################
def main():
    global screen, title_screen, pause_screen
    global title_menu, pause_menu
    global timer, myfont, game_start_time, deaths, display_debug, curr_level_number, total_time_elapsed
    global background_image

    screen = main_init()

    set_menus()

    # background_image = pygame.image.load("assets/graphics/registeel.png")

    deaths = 0
    display_debug = False
    curr_level_number = 0
    total_time_elapsed = 0
    timer = pygame.time.Clock()
    myfont = pygame.font.SysFont("monospace", 15) # set up the font to be used in all text displayed on the game screen
    make_labels(myfont) # makes all static labels such as game over, continue, so on
    play_bg_music("assets/audio/background/Those of Us Who Fight.wav") # plays the sound file supplied
    game_start_time = pygame.time.get_ticks()
    game_loop(1) # the main game loop. most everything is handled here. 1 is supplied to start at level 1

def set_menus():
    global title_menu, pause_menu
    global title_screen, pause_screen
    global player_name

    pause_screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    player_name = display_title_screen(screen)

def make_level(level_number):
    global player, camera, bg, entities, platforms, falling_platforms, moving_platforms, particles, total_level_width, total_level_height
    bg, entities, particles, platforms, falling_platforms, moving_platforms, player, camera, total_level_width, total_level_height = setup_level(True, Color("#000000"), level_number)

def game_loop(level_number):
    global display_debug, deaths, curr_level_number, level_time_elapsed, total_time_elapsed, player_name, level_deaths

    if level_number != curr_level_number:
        level_time_elapsed = 0
        level_deaths = 0
        curr_level_number = level_number

    make_level(level_number)

    pygame.display.update()

    up = down = left = right = running = boost = False # all initial movements variables are false
    pause_timer = 0
    added_death = False
    life_time_elapsed = 0

    music_paused = False
    gameRunning = True

    while gameRunning: # while the player has not yet hit a game-end condition
        timer.tick(60) # tick at no more than 60 frames per second

        if player.alive: # if the player has not yet hit a win or lose condition (exit or death block)
            for e in pygame.event.get(): # for all input events the user sends
            ############################################################
            ####################### KEY DOWNS ##########################
            ############################################################
                #TESTING SHORTCUTS
                if e.type == KEYDOWN and e.key == K_BACKSLASH:
                    display_debug = not display_debug # toggles debug display
                if e.type == KEYDOWN and e.key == K_r:
                    game_loop(level_number)  # reset level
                if e.type == KEYDOWN and e.key == K_i:
                    player.invincible = not player.invincible  # reset level
                if e.type == KEYDOWN and e.key == K_n:
                    level_number += 1
                    game_loop(level_number) # go forward a level
                if e.type == KEYDOWN and e.key == K_b:
                    if level_number > 1:
                        level_number-=1
                    game_loop(level_number) # go back a level
                if e.type == KEYDOWN and e.key == K_g:
                    invert_gravity(player) # invert gravity
                    for p in falling_platforms:
                        invert_gravity(p)
                if e.type == KEYDOWN and e.key == K_k:
                    player.alive = False # kill self
                if e.type == KEYDOWN and (e.key == K_p or e.key == K_ESCAPE):
                    up = down = left = right = running = boost = False
                    display_pause_screen(screen, pause_screen)
                    pause_timer = 1
                if e.type == KEYDOWN and e.key == K_m: # pause/unpause music
                    if music_paused:
                        pygame.mixer.music.unpause()
                        music_paused = False
                    else:
                        pygame.mixer.music.pause()
                        music_paused = True
                if e.type == QUIT: # if they hit the x button of the window
                    raise SystemExit, "QUIT" # quit the game and print "QUIT"
                #if e.type == KEYDOWN and e.key == K_ESCAPE: raise SystemExit, "ESCAPE" # if they hit the escape key, quit the game and print "ESCAPE"
                if e.type == KEYDOWN and (e.key == K_w or e.key == K_UP): # if they're holding down the w or up key
                    up = True
                if e.type == KEYDOWN and (e.key == K_s or e.key == K_DOWN): # if they're holding down the s or down key
                    down = True
                if e.type == KEYDOWN and (e.key == K_a or e.key == K_LEFT): # if they're holding down the a or left key
                    left = True
                if e.type == KEYDOWN and (e.key == K_d or e.key == K_RIGHT): # if they're holding down the d or right key
                    right = True
                #if e.type == KEYDOWN and e.key == K_LSHIFT:
                 #   running = True
                if e.type == KEYDOWN and e.key == K_SPACE: # if they're holding down the space key (holding down this key does nothing different than simply pressing it once)
                    if player.xvel == 0 and not player.on_moving_block: # if they're not moving in the x direction, don't teleport
                        boost = False
                    else: # if they are moving in the x direction, teleport
                        boost = True
                ############################################################
                ######################## KEY UPS ###########################
                ############################################################
                if e.type == KEYUP and (e.key == K_w or e.key == K_UP): # if they let go of the w or up key
                    up = False
                if e.type == KEYUP and (e.key == K_s or e.key == K_DOWN): # if they let go of the s or down key
                    down = False
                if e.type == KEYUP and (e.key == K_a or e.key == K_LEFT): # if they let go of the a or left key
                    left = False
                if e.type == KEYUP and (e.key == K_d or e.key == K_RIGHT): # if they let go of the d or right key
                    right = False
                #if e.type == KEYUP and e.key == K_LSHIFT:
                 #   running = False
                if e.type == KEYUP and e.key == K_SPACE: # if they let go of the space key
                    boost = False

#############################################################################################################################################################
################################################################       LEVEL COMPLETE       #################################################################
#############################################################################################################################################################
        elif not player.alive and player.beat_level: # if they hit an exit block and won the level
            player.yvel += 0.1
            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit, "QUIT" # if they hit the x button of the window, quit the game and print "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE: # if they hit the escape key, quit the game and print "ESCAPE"
                    raise SystemExit, "ESCAPE"
                if e.type == KEYDOWN and e.key == K_RETURN: # if they hit space, advance to the next level
                    check_hiscores(level_number, level_time_elapsed, life_time_elapsed, level_deaths, player_name)
                    game_loop(level_number+1)

#############################################################################################################################################################
#################################################################       PLAYER DEATH       ##################################################################
#############################################################################################################################################################
        else: # the only case that should hit this else should be if they died
            if not added_death:
                deaths += 1
                level_deaths += 1
                added_death = True
            player.yvel += 0.1
            display_death_cloud(player, camera, particles)
            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit, "QUIT" # if they hit the x button of the window, quit the game and print "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE: # if they hit the escape key, quit the game and print "ESCAPE"
                    raise SystemExit, "ESCAPE"
                if e.type == KEYDOWN and e.key == K_RETURN: # if they hit space, reset the level
                    game_loop(level_number)


        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        # screen.blit(background_image, (0,0))


############################################################
################### MOVE MOVING BLOCKS #####################
############################################################
        for p in falling_platforms:
            p.update(total_level_height)
            if not p.alive:
                falling_platforms.remove(p)

        for p in moving_platforms:
            p.move()

        for e in entities: # for all the entities in the level, blit their image onto the screen and apply the camera difference to them i guess? idk. fucking camera.
            screen.blit(e.image, camera.apply(e))

        for p in particles: # for all the particles that exist, if any
            p.move(player) # move them
            if not p.alive: # if they're dead, kill them
                particles.remove(p)
            else: # otherwise, draw them in their new position
                pygame.draw.circle(screen, p.col, (p.x, p.y), 2)

        # update player, draw everything else
        player.update(up, down, left, right, boost, platforms, camera, particles, total_level_width, total_level_height) # update the player's position and do collision detection on them
        
        camera.update(player) # again, not sure how camera works. i THINK this causes the camera to center on wherever the player is

        screen.blit(player.image, camera.apply(player))
#############################################################################################################################################################
######################################################       BEGIN DEBUGGING INFORMATION DISPLAY       ######################################################
#############################################################################################################################################################
        if display_debug:
            #########################
            """ CAMERA STATE INFO """
            #########################
            camera_top_label = myfont.render("camera_top = " + str(camera.state.top), 1, (255,255,0))
            screen.blit(camera_top_label, (573, 32))
            camera_left_label = myfont.render("camera_left = " + str(camera.state.left), 1, (255,255,0))
            screen.blit(camera_left_label, (564, 44))
            camera_bottom_label = myfont.render("camera_bottom = " + str(camera.state.bottom), 1, (255,255,0))
            screen.blit(camera_bottom_label, (546, 56))
            camera_right_label = myfont.render("camera_right = " + str(camera.state.right), 1, (255,255,0))
            screen.blit(camera_right_label, (555, 68))

            #####################################
            """ GAME VARIABLES AND DEBUG INFO """
            #####################################
            xpos_label = myfont.render("xPos = " + str(player.rect.x), 1, (255,255,0))
            screen.blit(xpos_label, (32, 32))
            ypos_label = myfont.render("yPos = " + str(player.rect.y), 1, (255,255,0))
            screen.blit(ypos_label, (32, 44))
            xvel_label = myfont.render("xVel = " + str(player.xvel), 1, (255,255,0))
            screen.blit(xvel_label, (32, 56))
            yvel_label = myfont.render("yVel = " + str(player.yvel), 1, (255,255,0))
            screen.blit(yvel_label, (32, 68))
            onGround_label = myfont.render("onGround = " + str(player.onGround), 1, (255,255,0))
            screen.blit(onGround_label, (32, 80))
            moving_label = myfont.render("moving = " + str(player.moving), 1, (255,255,0))
            screen.blit(moving_label, (32, 92))
            gravity_label = myfont.render("gravity = " + str(player.gravity), 1, (255,255,0))
            screen.blit(gravity_label, (32, 104))
            sticky_label = myfont.render("sticky = " + str(player.sticky), 1, (255,255,0))
            screen.blit(sticky_label, (32, 116))
            colliding_label = myfont.render("colliding = " + str(player.colliding), 1, (255,255,0))
            screen.blit(colliding_label, (32, 128))
            colliding_xvel_label = myfont.render("colliding w/ x = " + str(player.colliding_xvel), 1, (255,255,0))
            screen.blit(colliding_xvel_label, (32, 140))
            colliding_yvel_label = myfont.render("colliding w/ y = " + str(player.colliding_yvel), 1, (255,255,0))
            screen.blit(colliding_yvel_label, (32, 152))
            up_label = myfont.render("up = " + str(up), 1, (255,255,0))
            screen.blit(up_label, (32, 164))
            down_label = myfont.render("down = " + str(down), 1, (255,255,0))
            screen.blit(down_label, (32, 176))
            left_label = myfont.render("left = " + str(left), 1, (255,255,0))
            screen.blit(left_label, (32, 188))
            right_label = myfont.render("right = " + str(right), 1, (255,255,0))
            screen.blit(right_label, (32, 200))
            jumps_label = myfont.render("jumps left = " + str(player.jumps), 1, (255,255,0))
            screen.blit(jumps_label, (32, 248))
            can_teleport_label = myfont.render("canTeleport = " + str(player.canTeleport), 1, (255,255,0))
            screen.blit(can_teleport_label, (32, 260))

        else: # display debug is false

            if player.alive:
                if pause_timer > 0:
                    pause_timer = -1
                    time_since_last_tick = timer.get_time()
                elif pause_timer == -1:
                    pause_timer = 0
                    time_since_last_tick = 0
                else:
                    time_since_last_tick = timer.get_time()

                total_time_elapsed += time_since_last_tick
                level_time_elapsed += time_since_last_tick
                life_time_elapsed += time_since_last_tick

            death_count_label = myfont.render("Total Deaths: " + str(deaths), 1, (255,255,0))
            screen.blit(death_count_label, (32, 32))

            level_death_count_label = myfont.render("Deaths this level: " + str(level_deaths), 1, (255,255,0))
            screen.blit(level_death_count_label, (32, 44))

            total_time_elapsed_label = myfont.render("Total: " + str(convert_time(total_time_elapsed)), 1, (255,255,0))
            screen.blit(total_time_elapsed_label, (622, 32))
            
            level_time_elapsed_label = myfont.render("Level: " + str(convert_time(level_time_elapsed)), 1, (255,255,0))
            screen.blit(level_time_elapsed_label, (622, 44))

            life_time_elapsed_label = myfont.render("Life: " + str(convert_time(life_time_elapsed)), 1, (255,255,0))
            screen.blit(life_time_elapsed_label, (631, 56))

#############################################################################################################################################################
#######################################################       END DEBUGGING INFORMATION DISPLAY       #######################################################
#############################################################################################################################################################

        ##########################
        """ MESSAGES TO PLAYER """ # i really need a more graceful way to do this....is there even a way?
        ##########################
        if level_number == 1:
            screen.blit(how_to_teleport_label, (2368 + camera.state.left, 96 + camera.state.top)) # tell the player how to teleport

        if not player.alive and not player.beat_level: # if the player died
            up = down = left = right = boost = False # prevent further movement
            screen.blit(game_over_label, [game_over_label_x, game_over_label_y]) # display game over text
            screen.blit(reset_label, [reset_label_x, reset_label_y]) # display instructions to reset

        if not player.alive and player.beat_level: # if the player hit an exit block and won
            up = down = left = right = boost = False # prevent futher movement
            screen.blit(win_label, [win_label_x, win_label_y]) # display win screen test
            screen.blit(advance_label, [advance_label_x, advance_label_y]) # display instructions to continue


        pygame.display.update() # actually update the display after blitting everything onto the screen

    #handle post-death here?
    pygame.quit() # quit the program after gameRunning becomes false

############################################################
#### FUNCTIONS TO BE SEPARATED INTO OTHER PYTHON FILES #####
############################################################

def make_labels(font):
    global game_over_label, game_over_label_x, game_over_label_y
    global reset_label, reset_label_x, reset_label_y
    global win_label, win_label_x, win_label_y
    global advance_label, advance_label_x, advance_label_y
    global how_to_teleport_label

    game_over_label = font.render("You are dead!", True, red)
    game_over_label_rect = game_over_label.get_rect()
    game_over_label_x = screen.get_width() / 2 - game_over_label_rect.width / 2
    game_over_label_y = screen.get_height() / 2 - game_over_label_rect.height / 2 - 60

    reset_label = font.render("Hit Enter to restart.", True, white)
    reset_label_rect = reset_label.get_rect()
    reset_label_x = screen.get_width() / 2 - reset_label_rect.width / 2
    reset_label_y = screen.get_height() / 2 - reset_label_rect.height / 2 + 12 - 60

    win_label = font.render("Level Complete!", True, green)
    win_label_rect = win_label.get_rect()
    win_label_x = screen.get_width() / 2 - win_label_rect.width / 2
    win_label_y = screen.get_height() / 2 - win_label_rect.height / 2 - 60

    advance_label = font.render("Hit Enter to advance.", True, white)
    advance_label_rect = advance_label.get_rect()
    advance_label_x = screen.get_width() / 2 - advance_label_rect.width / 2
    advance_label_y = screen.get_height() / 2 - advance_label_rect.height / 2 + 12 - 60

    how_to_teleport_label = font.render("Try spacebar while moving!", 1, (0,255,0))

if __name__ == "__main__":
    main()
