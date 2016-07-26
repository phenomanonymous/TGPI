from lib.constants import *
from lib.functions import *
from lib.entities import *
from lib.physics import *
from lib.spritesheet import *
import math

############################################################
###################### PLAYER CLASS ########################
############################################################

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)

        self.sprite_invincible = pygame.image.load("assets/graphics/player/invincible.png").convert()
        self.sprite_invincible.set_colorkey((255,255,255))

        ##############################################

        self.face_left = pygame.image.load("assets/graphics/player/face_left.png").convert()
        self.face_left.set_colorkey((0,0,0))
        self.walk_left = pygame.image.load("assets/graphics/player/walk_left.png").convert()
        self.walk_left.set_colorkey((0,0,0))
        self.face_right = pygame.image.load("assets/graphics/player/face_right_new.png").convert()
        self.face_right.set_colorkey((0,0,0))
        self.walk_right = pygame.image.load("assets/graphics/player/walk_right.png").convert()
        self.walk_right.set_colorkey((0,0,0))

        self.walk_left_array = []
        self.walk_left_array.append(self.face_left)
        self.walk_left_array.append(self.walk_left)

        self.walk_right_array = []
        self.walk_right_array.append(self.face_right)
        self.walk_right_array.append(self.walk_right)
        ##############################################

        self.face_right_inverted = pygame.image.load("assets/graphics/player/face_right_inverted.png").convert()
        self.face_right_inverted.set_colorkey((0,0,0))
        self.walk_right_inverted = pygame.image.load("assets/graphics/player/walk_right_inverted.png").convert()
        self.walk_right_inverted.set_colorkey((0,0,0))
        self.face_left_inverted = pygame.image.load("assets/graphics/player/face_left_inverted.png").convert()
        self.face_left_inverted.set_colorkey((0,0,0))
        self.walk_left_inverted = pygame.image.load("assets/graphics/player/walk_left_inverted.png").convert()
        self.walk_left_inverted.set_colorkey((0,0,0))

        self.walk_left_inverted_array = []
        self.walk_left_inverted_array.append(self.face_left_inverted)
        self.walk_left_inverted_array.append(self.walk_left_inverted)

        self.walk_right_inverted_array = []
        self.walk_right_inverted_array.append(self.face_right_inverted)
        self.walk_right_inverted_array.append(self.walk_right_inverted)
        ##############################################
        self.onGround = False
        #sprite = Surface((BLOCK_SIZE,BLOCK_SIZE))
        sprite = Surface((22, 31))
        sprite = self.face_right
        sprite.set_colorkey((0,0,0))
        self.image = sprite
        self.particles_displayed = False
        self.running = False
        self.boosting = False
        self.canTeleport = True
        self.alive = True
        self.beat_level = False
        self.sticky = False
        self.gravity = 1
        self.moving = False
        self.jumps = 1
        self.on_moving_block = False
        self.animation_step = 0
        self.facing = "right"
        self.change_frame = 0
        self.invincible = False

    def update(self, up, down, left, right, boost, platforms, camera, particles, total_level_width, total_level_height):

        if self.onGround or self.sticky: # only jump if on the ground
            self.jumps = TOTAL_PLAYER_JUMPS
        else:
            self.jumps = 0

        if self.jumps > 0:
            if up:
                self.yvel -= 6 * self.gravity
                self.jumps -= 1
        if down:
            pass
        if left:
            self.xvel = -1 * PLAYER_SPEED
            self.facing = "left"
            self.change_frame += 1
            if self.change_frame > 7:
                self.change_frame = 0
                self.animation_step += 1
            if self.animation_step > 1:
                self.animation_step = 0
            if self.gravity > 0:
                self.image = self.walk_left_array[self.animation_step].convert()
            elif self.gravity < 0:
                self.image = self.walk_left_inverted_array[self.animation_step].convert()
        if right:
            self.xvel = PLAYER_SPEED
            self.facing = "right"
            self.change_frame += 1
            if self.change_frame > 7:
                self.change_frame = 0
                self.animation_step += 1
            if self.animation_step > 1:
                self.animation_step = 0
            if self.gravity > 0:
                self.image = self.walk_right_array[self.animation_step].convert()
            elif self.gravity < 0:
                self.image = self.walk_right_inverted_array[self.animation_step].convert()
        if self.running:
            self.xvel *= 1.5
            display_running_dirt_cloud(self, camera, particles)
        if boost:
            if self.canTeleport:
                teleport(self, camera, particles, left, right, platforms)
        elif not boost:
            self.particles_displayed = self.boosting = False # player let go of teleport key, so boosting and particles displayed flags get set to False
        
        if not(left or right):
            if self.facing == "left":
                if self.gravity > 0:
                    self.image = self.face_left.convert()
                elif self.gravity < 0:
                    self.image = self.face_left_inverted.convert()
            elif self.facing == "right":
                if self.gravity > 0:
                    self.image = self.face_right.convert()
                elif self.gravity < 0:
                    self.image = self.face_right_inverted.convert()
            else:
                print("Somehow not left or right")

        if self.invincible:
            self.image = self.sprite_invincible

        if not(left or right or self.on_moving_block):
            self.xvel = 0

        if self.xvel != 0 or self.yvel != 0:
            self.moving = True
        else:
            self.moving = False

        if self.moving:# and not self.sticky:
            self.onGround = False # this is necessary to make sure the player falls into and collides with the ground
            self.sticky = False

        if not self.onGround or self.on_moving_block: # only accelerate with gravity if in the air
            if self.sticky:
                self.yvel = 1 # this is necessary to cause you to fall off sticky blocks unless holding into them
            if not self.sticky:
                self.yvel += (0.3 * self.gravity)
            if self.yvel > 40: self.yvel = 40 # max falling down speed
            if self.yvel < -40: self.yvel = -40 # max falling up speed

        self.rect.centerx += self.xvel # increment in x direction
        collide(self, self.xvel, 0, platforms) # do x-axis collisions
        
        # the gross line immediately below this is for rounding away from 0
        self.rect.centery += int(float(self.yvel)) + (1 if (self.yvel > 0) else (-1 if (self.yvel < 0) else 0)) # increment in y direction
        collide(self, 0, self.yvel, platforms) # do y-axis collisions

        stay_in_the_map(self, total_level_width, total_level_height) # keeps entity within the bounds of the map