from functions import *
from blocks import *
from player import *
from camera import *
from spritesheet import *
import os
def setup_level(isColor, background, level_number):
    global entities, platforms, falling_platforms, moving_platforms
    bg = make_bg(isColor, background)
    entities = pygame.sprite.Group() # initialize the entities array
    particles = [] # initialize the particles array
    platforms = [] # initialize the platforms array
    falling_platforms = [] # initialize the falling platforms array
    moving_platforms = [] # initialize the moving platforms array

    create_level(level_number)

    player = Player(BLOCK_SIZE, total_level_height - BLOCK_SIZE) # create the player and place them at the bottom left corner of the map, off the left and bottom by one block size
    camera = Camera(complex_camera, total_level_width, total_level_height) # create the camera. frankly i'm still not sure how this works....
    #entities.add(player) # add the player to the entities in the level

    return bg, entities, particles, platforms, falling_platforms, moving_platforms, player, camera, total_level_width, total_level_height

def create_level(level_number):
    global total_level_height, total_level_width

    pygame.display.set_caption("Level " + str(level_number)) # set title of game

    x = y = 0
    filename = "assets/levels/level" + str(level_number) + ".txt"
    if not os.path.isfile(filename):
        if os.path.isfile("levels/youwin.txt"):
            filename = "levels/youwin.txt"
        else:
            raise SystemExit, "Game Win Level not found"
    make_sprites() # cuts up the sprite sheet and makes individual sprite blocks out of it
    file = open(filename, 'r') # open the text file of the level the player is currently on in order to create the level
    level = file.readlines() # reads in the textfile to a variable
    # build the level
    for row in level: # for each row in the level
        for col in row: # for each column in the row, create a block based on the letter or lackthereof supplied in the textfile
            if col == "P": 
                p = Platform(x, y, plat_sprite)
                platforms.append(p)
                entities.add(p)
            if col == "B":
                b = BouncyBlock(x, y, bncy_sprite)
                platforms.append(b)
                entities.add(b)
            if col == "G":
                g = GravityBlock(x, y, grav_sprite)
                platforms.append(g)
                entities.add(g)
            if col == "V":
                v = VanishingBlock(x, y, plat_sprite)
                platforms.append(v)
                falling_platforms.append(v)
                entities.add(v)
            if col == "S":
                s = StickyBlock(x, y, stky_sprite)
                platforms.append(s)
                entities.add(s)
            if col == "F":
                f = FastBlock(x, y, fast_sprite)
                platforms.append(f)
                entities.add(f)
            if col == "T":
                t = TrickBlock(x, y, plat_sprite)
                platforms.append(t)
                entities.add(t)
            if col == "I":
                i = InvisBlock(x, y, plat_sprite)
                platforms.append(i)
                entities.add(i)
            if col == "U":
                u = OneWayUpBlock(x, y, owup_sprite)
                platforms.append(u)
                entities.add(u)
            if col == "D":
                d = OneWayDownBlock(x, y, owdn_sprite)
                platforms.append(d)
                entities.add(d)
            if col == "X":
                death = DeathBlock(x, y, lava_sprite)
                platforms.append(death)
                entities.add(death)
            if col == "!" or col == "@" or col == "#" or col == "$" or col == "%" or col == "^" or col == "&" or col == "*" or col == "(":
                if col == "!": col = 1
                elif col == "@": col = 2
                elif col == "#": col = 3
                elif col == "$": col = 4
                elif col == "%": col = 5
                elif col == "^": col = 6
                elif col == "&": col = 7
                elif col == "*": col = 8
                else: col = 9
                z = MovingHorizontalDeathBlock(x, y, lava_sprite, col)
                platforms.append(z)
                moving_platforms.append(z)
                entities.add(z)
            if col == "1" or col == "2" or col == "3" or col == "4" or col == "5" or col == "6" or col == "7" or col == "8" or col == "9":
                col = int(col)
                w = MovingVerticalDeathBlock(x, y, lava_sprite, col)
                platforms.append(w)
                moving_platforms.append(w)
                entities.add(w)
            if col == "E":
                e = ExitBlock(x, y, exit_sprite)
                platforms.append(e)
                entities.add(e)
            x += BLOCK_SIZE
        y += BLOCK_SIZE
        x = 0

    total_level_width  = len(level[0])*BLOCK_SIZE # calculate width as the number of blocks on the first line horizontally times the size of each block
    total_level_height = len(level)*BLOCK_SIZE # calculate height as the number of blocks vertically times the size of each block

def make_sprites():
    global lava_sprite, exit_sprite, grav_sprite, plat_sprite, owup_sprite, owdn_sprite, fast_sprite, stky_sprite, bncy_sprite, back_sprite, face_left, walk_left, face_right, walk_right
    lava_sprite = pygame.image.load("assets/graphics/blocks/lava_sprite.png")
    exit_sprite = pygame.image.load("assets/graphics/blocks/exit_sprite.png")
    grav_sprite = pygame.image.load("assets/graphics/blocks/grav_sprite.png")
    plat_sprite = pygame.image.load("assets/graphics/blocks/plat_sprite.png")
    owup_sprite = pygame.image.load("assets/graphics/blocks/owup_sprite.png")
    owdn_sprite = pygame.image.load("assets/graphics/blocks/owdn_sprite.png")
    fast_sprite = pygame.image.load("assets/graphics/blocks/fast_sprite.png")
    stky_sprite = pygame.image.load("assets/graphics/blocks/stky_sprite.png")
    bncy_sprite = pygame.image.load("assets/graphics/blocks/bncy_sprite.png")
    back_sprite = pygame.image.load("assets/graphics/blocks/back_sprite.png")

def cut_up_sprites():
    global lava_sprite, exit_sprite, grav_sprite, plat_sprite, owup_sprite, owdn_sprite, fast_sprite, stky_sprite, bncy_sprite, back_sprite
    ss = spritesheet("assets/graphics/sheet1_2.png")
    lava_sprite = ss.image_at((128, 32, 32, 32))
    pygame.image.save(lava_sprite, "assets/graphics/lava_sprite.png")
    exit_sprite = ss.image_at((64, 96, 32, 32))
    pygame.image.save(exit_sprite, "assets/graphics/exit_sprite.png")
    grav_sprite = ss.image_at((0, 192, 32, 32))
    pygame.image.save(grav_sprite, "assets/graphics/grav_sprite.png")
    plat_sprite = ss.image_at((32, 96, 32, 32))
    pygame.image.save(plat_sprite, "assets/graphics/plat_sprite.png")
    owup_sprite = ss.image_at((224, 192, 32, 32))
    pygame.image.save(owup_sprite, "assets/graphics/owup_sprite.png")
    owdn_sprite = ss.image_at((192, 224, 32, 32))
    pygame.image.save(owdn_sprite, "assets/graphics/owdn_sprite.png")
    fast_sprite = ss.image_at((0, 160, 32, 32))
    pygame.image.save(fast_sprite, "assets/graphics/fast_sprite.png")
    stky_sprite = ss.image_at((64, 128, 32, 32))
    pygame.image.save(stky_sprite, "assets/graphics/stky_sprite.png")
    bncy_sprite = ss.image_at((128, 64, 32, 32))
    pygame.image.save(bncy_sprite, "assets/graphics/bncy_sprite.png")
    back_sprite = ss.image_at((0, 128, 32, 32))
    pygame.image.save(back_sprite, "assets/graphics/back_sprite.png")