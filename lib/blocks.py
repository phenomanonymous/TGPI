from pygame import *
from lib.entities import *
from lib.constants import *
############################################################
#################### PLATFORM CLASSES ######################
############################################################

class Platform(Entity): # basic Platform class, nothing special about it. Used for basic blocks or as a base class for special blocks to extend
    def __init__(self, x, y, skin):
        Entity.__init__(self, x, y)
        self.image = Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.convert()
        self.image = skin.convert()
        self.xvel = 0
        self.yvel = 0

    def update(self):
        pass

class BouncyBlock(Platform): # bouncy blocks cause the player to bounce in the reverse y direction that it was hit and multiply speed by 1.1
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = bncy_sprite.convert()

class GravityBlock(Platform):
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = grav_sprite.convert()

class VanishingBlock(Platform):
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        self.image.fill(Color("#551A8B"))
        self.start_falling = False
        self.delay = 5
        self.yvel = 0
        self.alive = True

    def update(self, total_level_height):
        if self.start_falling and self.delay > 0:
            self.delay -= 1
        if self.delay <= 0:
            self.yvel += 0.3 * self.gravity
            self.rect.y += self.yvel
            if self.rect.y > total_level_height or self.rect.y < 0:
                self.alive = False

class StickyBlock(Platform): # sticky blocks cause the player to stick to them, defying gravity
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = stky_sprite.convert()

class FastBlock(Platform): # fast blocks multiply the users x movement speed by 1.5
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = fast_sprite.convert()

class TrickBlock(Platform): # trick blocks are not solid at all, they only look it
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)

class InvisBlock(Platform): # invis blocks are completely solid, but are invisible against the black background
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        self.image.fill(Color("#000000"))

class OneWayUpBlock(Platform): # oneWayUp blocks are only solid when attempting to pass through from the top
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = owup_sprite.convert() 

class OneWayDownBlock(Platform): # oneWayDown blocks are only solid when attempting to pass through from the bottom
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = owdn_sprite.convert()

class DeathBlock(Platform): # death blocks cause the player to die
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = lava_sprite.convert()

class MovingHorizontalDeathBlock(Platform): # moving horizontal death blocks move a parameterized distance in either x direction, and cause death
    def __init__(self, x, y, skin, leash):
        Platform.__init__(self, x, y, skin)
        self.startx = x
        self.xvel = -2
        self.leash = leash
        self.move_left = True # start movement to the left by default
        #self.image = lava_sprite.convert()

    def move(self):
        if self.move_left:
            self.rect.x += self.xvel
            if self.rect.x <= self.startx - (self.leash * BLOCK_SIZE): # keep moving left until it hits the end of its leash
                self.move_left = False # start moving right
                self.xvel = 2
        else:
            self.rect.x += self.xvel
            if self.rect.x >= self.startx + (self.leash * BLOCK_SIZE): # keep moving right until it hits the end of its leash
                self.move_left = True # start moving left
                self.xvel = -2

class MovingVerticalDeathBlock(Platform): # moving vertical death blocks move a parameterized distance in either x direction, and cause death
    def __init__(self, x, y, skin, leash):
        Platform.__init__(self, x, y, skin)
        self.starty = y
        self.yvel = -2
        self.leash = leash
        self.move_up = True # start movement to the right by default
        #self.image = lava_sprite.convert()

    def move(self):
        if self.move_up:
            self.rect.y += self.yvel
            if self.rect.y <= self.starty - (self.leash * BLOCK_SIZE): # keep moving up until it hits the end of its leash
                self.move_up = False # start moving down
                self.yvel = 2
        else:
            self.rect.y += self.yvel
            if self.rect.y >= self.starty + (self.leash * BLOCK_SIZE): # keep moving down until it hits the end of its leash
                self.move_up = True # start moving up
                self.yvel = -2

class ExitBlock(Platform): # exit blocks cause the player to win the level
    def __init__(self, x, y, skin):
        Platform.__init__(self, x, y, skin)
        #self.image = exit_sprite.convert()