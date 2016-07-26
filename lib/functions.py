from pygame import *
from lib.constants import *
from lib.particle import *
from lib.entities import *
from lib.blocks import *
import pygame
import lib.camera
import fileinput

def main_init():
    pygame.init() # initialize the pygame library (i think?)
    pygame.font.init() # initializes the font system apparently?
    pygame.mixer.init() # initializes the audio
    pygame.display.set_caption("Test Grid, Please Ignore.") # set title of game
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) # set up the screen size and other variables
    return screen

def check_hiscores(level, level_time, life_time, deaths, name):
    check_time_trials(level, level_time, name)
    check_life_time_trials(level, life_time, name)
    check_least_deaths(level, deaths, name)

def check_least_deaths(level, deaths, name):
    with open("assets/hiscores/hiscores_least_deaths.txt", "r") as infile:
        lines = infile.readlines()
    found = False
    if level < 10:
        level = str(level) + " "
    level_number = "level" + str(level)
    with open("assets/hiscores/hiscores_least_deaths.txt", "w") as infile:
        i = 0
        for line in lines:
            if level_number in line:
                score = line.split(':')[1]
                if int(deaths) < int(score):
                    lines[i] = str(level_number) + ":" + str(deaths) + ":" + name + "\n"
                else:
                    lines[i] = (line)
                found = True
            i += 1
        if not found:
            lines.append(str(level_number) + ":" + str(deaths) + ":" + name + "\n")
        infile.writelines(lines)


def check_life_time_trials(level, time, name):
    with open("assets/hiscores/hiscores_life_timetrials.txt", "r") as infile:
        lines = infile.readlines()
    found = False
    if level < 10:
        level = str(level) + " "
    level_number = "level" + str(level)
    with open("assets/hiscores/hiscores_life_timetrials.txt", "w") as infile:
        i = 0
        for line in lines:
            if level_number in line:
                score = line.split(':')[1]
                if int(time) < int(score):
                    lines[i] = str(level_number) + ":" + str(time) + ":" + name + "\n"
                else:
                    lines[i] = (line)
                found = True
            i += 1
        if not found:
            lines.append(str(level_number) + ":" + str(time) + ":" + name + "\n")
        infile.writelines(lines)


def check_time_trials(level, time, name):
    with open("assets/hiscores/hiscores_timetrials.txt", "r") as infile:
        lines = infile.readlines()
    found = False
    if level < 10:
        level = str(level) + " "
    level_number = "level" + str(level)
    with open("assets/hiscores/hiscores_timetrials.txt", "w") as infile:
        i = 0
        for line in lines:
            if level_number in line:
                score = line.split(':')[1]
                if int(time) < int(score):
                    lines[i] = str(level_number) + ":" + str(time) + ":" + name + "\n"
                else:
                    lines[i] = (line)
                found = True
            i += 1
        if not found:
            lines.append(str(level_number) + ":" + str(time) + ":" + name + "\n")
        infile.writelines(lines)


def convert_time(milliseconds):
    minutes = milliseconds / 1000 / 60
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    seconds = (milliseconds / 1000) % 60
    if seconds < 10:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
    milli = milliseconds % 1000
    if milli < 10:
        milli = "00" + str(milli)
    elif milli < 100:
        milli = "0" + str(milli)
    else:
        milli = str(milli)
    return minutes + ":" + seconds + "." + milli

def invert_gravity(entity):
    entity.gravity *= -1
    entity.yvel = 0.1 * entity.gravity
    
def teleport(entity, camera, particles, left, right, platforms):
    display_enter_poof(entity, camera, particles, left, right)
    #####################################
    if not entity.boosting: # if not still holding teleport key after the initial teleport
        if left or right: # if moving along the x-axis
            entity.boosting = True # flip boosting flag to true so the player doesn't keep infinitely teleporting while holding the teleport key
            entity.canTeleport = False # flip canTeleport flag to false so they can't teleport again until hitting the ground
            if left: # if moving left
                exit_loc = get_exit_location(entity, entity.rect.x - TELEPORT_DISTANCE, platforms, -1) # teleport to the left
                if exit_loc < entity.rect.x:
                    entity.rect.x = exit_loc
            elif right: # if moving right
                exit_loc = get_exit_location(entity, entity.rect.x + TELEPORT_DISTANCE, platforms, 1) # teleport to the right
                if exit_loc > entity.rect.x:
                    entity.rect.x = exit_loc
            else:
                print "this should never happen what the fuck" #somehow left or right is true, but we didnt hit either left or right individually
        else:  # player is holding space while not moving along the x-axis
            entity.boosting = False
    #####################################
    display_exit_poof(entity, camera, particles, left, right)

def get_exit_location(entity, target_location, platforms, direction):
    ghost = Entity(target_location, entity.rect.y)
    return ghost_collide(ghost, platforms, direction)


def ghost_collide(ghost, platforms, direction):
    for p in platforms:
        if sprite.collide_rect(ghost, p):
            if isinstance(p, TrickBlock):
                pass
            else:
                if direction > 0:
                    ghost.rect.right = p.rect.left
                    ghost_collide(ghost, platforms, direction)
                elif direction < 0:
                    ghost.rect.left = p.rect.right
                    ghost_collide(ghost, platforms, direction)
                else:
                    print "how the fuck did this happen"
    return ghost.rect.x

def display_enter_poof(entity, camera, particles, left, right):
    if not entity.particles_displayed: # don't continuously display more particles
        for part in range(1, 100):
            if part % 2 > 0: 
                col = red
            else: 
                col = grey
            if camera.state.left < 0:
                if left:
                    part_x = entity.rect.centerx + camera.state.left + TELEPORT_DISTANCE
                elif right:
                    part_x = entity.rect.centerx + camera.state.left - TELEPORT_DISTANCE
                else: # this shouldn't happen but somehow it did once
                    part_x = entity.rect.centerx
            else:
                part_x = entity.rect.centerx + camera.state.left
            part_y = entity.rect.centery + camera.state.top
            particle = Particle(part_x, part_y, col, 0, False) # 0 for enter poof, False for non-death poof
            particles.append(particle)

def display_exit_poof(entity, camera, particles, left, right):
    if not entity.particles_displayed: # don't continuously display more particles
        for part in range(1, 100):
            if part % 2 > 0: 
                col = blue
            else: 
                col = grey
            part_x = entity.rect.centerx + camera.state.left
            if camera.state.left < 0:
                if left:
                    part_x = entity.rect.centerx + camera.state.left + TELEPORT_DISTANCE
                elif right:
                    part_x = entity.rect.centerx + camera.state.left - TELEPORT_DISTANCE
                
            part_y = entity.rect.centery + camera.state.top
            particle = Particle(part_x, part_y, col, 1, False) # 1 for exit poof
            particles.append(particle)
        entity.particles_displayed = True

def display_death_cloud(entity, camera, particles):
    if len(particles) < 1000:
        for part in range(1, 10):
            if part % 2 > 0: 
                col = green
            else: 
                col = yellow
            part_x = entity.rect.centerx + camera.state.left
            part_y = entity.rect.centery + camera.state.top
            particle = Particle(part_x, part_y, col, 0, True) # true for death poof
            particles.append(particle)
        entity.particles_displayed = True

def display_running_dirt_cloud(entity, camera, particles):
    if entity.xvel != 0:
        if len(particles) < 1000:
            for part in range(1,10):
                if part % 2 > 0:
                    col = grey
                else:
                    col = white
                if entity.xvel > 0:
                    part_x = entity.rect.left + camera.state.left
                elif entity.xvel < 0:
                    part_x = entity.rect.right + camera.state.left
                part_y = entity.rect.bottom + camera.state.top
                particle = Particle(part_x, part_y, col, 2, False) # 2 for dirt cloud
                particles.append(particle)
            entity.particles_displayed = True 

def stay_in_the_map(entity, total_level_width, total_level_height):
    if entity.rect.left < BLOCK_SIZE:
        entity.rect.left = BLOCK_SIZE
    if entity.rect.right > total_level_width - BLOCK_SIZE:
        entity.rect.right = total_level_width - BLOCK_SIZE
    if entity.rect.top < BLOCK_SIZE:
        entity.rect.top = BLOCK_SIZE
    if entity.rect.bottom > total_level_height - BLOCK_SIZE:
        entity.rect.bottom = total_level_height - BLOCK_SIZE

def make_bg(isColor, background):
    bg = Surface((BLOCK_SIZE,BLOCK_SIZE)) # bg is a one-block-size surface to be repeated across the background of the map
    bg.convert() # not sure why this is necessary
    if isColor:
        bg.fill(background) # fill the background in black
    else:
        bg = background
    return bg

def play_bg_music(sound):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(loops=-1)