from pygame import *
from lib.constants import *
############################################################
###################### ENTITY CLASS ########################
############################################################

class Entity(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.xvel = 0
        self.yvel = 0
        self.colliding = False
        self.colliding_xvel = False
        self.colliding_yvel = False
        self.gravity = 1
        self.rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)