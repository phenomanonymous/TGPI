from constants import *
import random
import math

############################################################
##################### PARTICLE CLASS #######################
############################################################

class Particle():
    def __init__(self, startx, starty, col, which_poof, death_cloud): # starting x position, starting y position, color, whether its an enter or exit poof, whether it is a death cloud or not
        self.x = startx # self.x is the supplied x (sum of where the player is along x, +/- the camera's offset) + half the size of a block, so particles spawn in the middle of the player's block
        self.y = starty # self.y is the supplied y (sum of where the player is along y, +/- the camera's offset) + half the size of a block, so particles spawn in the middle of the player's block
        self.col = col 
        self.init_x = self.x
        self.init_y = self.y
        self.alive = True
        self.which_poof = which_poof
        if death_cloud == True:
            self.death_point = random.randint(100, 1000) # death_cloud's particles go much higher before despawning
        else:
            self.death_point = random.randint(100, 200)

    def move(self, entity):
        if self.which_poof == 0:
            self.x += random.randint(-5, 5) # wider poof
            if math.fabs(self.init_y - self.y) > self.death_point/2:
                self.alive = False
            else:
                self.y -= random.randint(1, 5) * entity.gravity # shorter poof
        elif self.which_poof == 1:
            self.y -= random.randint(1, 10) * entity.gravity# taller poof
            if math.fabs(self.init_y - self.y) > self.death_point:
                self.alive = False
            else:
                self.x+=random.randint(-3, 3)# slimmer poof
        else: #2
            if entity.xvel != 0:
                if entity.xvel > 0:
                    self.x += random.randint(-3, 0)
                elif entity.xvel < 0:
                    self.x += random.randint(0, 3)
                    
            if math.fabs(self.init_y - self.y) > 10:
                self.alive = False
            else:
                self.y -= random.randint(1, 3) * entity.gravity