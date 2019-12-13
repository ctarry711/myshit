import pprint
import random
import pygame
pp = pprint.PrettyPrinter(indent=1)

# TO DO:

### GRAPHICS ###

# - Need Player planting animation
# - Need log jumping animation
# - Road graphics doesn't really match the rest
# - Change Movement Dots to something better
# - Make planted trees look better
# - Make vertical logs
#   Sun should be colored better to get darker at end of day
# - Get truck sprite
# - I think UI would look better without the full bar. Use just little frames for each bit of information needed

### Coding ###

# - Sun is currently applied over UI, should be only the playable area
# - add random mossy logs
# - Make it actually playable as a game: Set time limit for different star quotas
# - Clean up all the old code from the old map setup
# - Find a better way to detect the boundaries of the block
#      - This will need to work for not just square boundaries (maybe don't need to detect at all)
# - Add truck driving by to drop you off, and pick up


def gen_map(raw_map, num_logs):
    #returns the map with added logs (notated -2) of random length between 2-3, orientation and location
    
    #Initialize the array with all zeros
    map_array = raw_map
       
    left = 7
    right = 18
    top = 8
    bot = 16

    for y in range(len(map_array)):
        for x in range(len(map_array[0])):
            if map_array[y][x] >= 98:
                map_array[y][x] = -7
            else:
                map_array[y][x] = 0
            
    #Add the random logs
    for ii in range(num_logs):
        length = 2 if random.random() > .333 else 3
        orient = 0 #if random.random() > .5 else 1
        open = False
        while open == False:
            pos_loc_x = random.randint(left, right - 3)
            pos_loc_y = random.randint(top, bot - 3)
            if map_array[pos_loc_y][pos_loc_x] == 0:
                if orient == 0:
                    if map_array[pos_loc_y][pos_loc_x+1] == 0 and (map_array[pos_loc_y][pos_loc_x+2]) * (length - 2) == 0:
                        map_array[pos_loc_y][pos_loc_x] = -3
                        map_array[pos_loc_y][pos_loc_x+1] = -2
                        if length == 3 and map_array[pos_loc_y][pos_loc_x+2] == 0:
                            map_array[pos_loc_y][pos_loc_x] = -4
                            map_array[pos_loc_y][pos_loc_x+2] = -2
                        open = True
                else:
                    if map_array[pos_loc_y+1][pos_loc_x] == 0 and (map_array[pos_loc_y+2][pos_loc_x]) * (length - 2) == 0:
                        map_array[pos_loc_y][pos_loc_x] = -5
                        map_array[pos_loc_y+1][pos_loc_x] = -2
                        if length == 3 and map_array[pos_loc_y+2][pos_loc_x] == 0:
                            map_array[pos_loc_y][pos_loc_x] = -6
                            map_array[pos_loc_y+2][pos_loc_x] = -2
                        open = True
        
    start_location = (left, bot)
    
    return (map_array, start_location)

def txt_to_array(file_url):
    #file url should be like: r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Map Layers\day_one.txt"
    map_txt = open(file_url,"r")
    map_str = map_txt.readlines()
    map_str = map_str[6:]
    map_str2 = []
    map_str3 = []
    map_str4 = []
    map_str5 = []
    for y in map_str:
        map_str2.append(y[:-1])
    for y in map_str2:
        map_str3.append(y.split(","))
    for y in map_str3:
        map_str4.append(y[:-1])
    for y in range(len(map_str4)):
        map_str5.append([])
        for x in range(len(map_str4[y])):
            map_str5[y].append(int(map_str4[y][x]))
    return map_str5[:-1]


def tree_footprint(x, y):
    footprint = []
    footprint.append((x+1, y))
    footprint.append((x+2, y))
    footprint.append((x-1, y))
    footprint.append((x-2, y))
    footprint.append((x, y+1))
    footprint.append((x, y+2))
    footprint.append((x, y-1))
    footprint.append((x, y-2))
    footprint.append((x+1, y+1))
    footprint.append((x-1, y+1))
    footprint.append((x+1, y-1))
    footprint.append((x-1, y-1))
    return footprint


"""
Map Key:
0 = empty
1 = planted trees
-2 = logs
-3 = start of short log
-4 = start of long log
-5 = start of short vertical log
-6 = start of long vertical log
-7 = big tree
3 = road
4 = left road end
6 = right road end
5 = Cache

"""


### GAME LOOP ###
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    MOUSEBUTTONDOWN,
    QUIT,
    K_SPACE,
    K_LSHIFT
)


#Initialize Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
BLACK_50 = (169,175,143)
GREEN = (0,255,0)
YELLOW = (0,255,255)
RED = (255,0,0)
BROWN = (150,75,0)
GRASS = (139,214,74)
GRIDLINES = (55,153,63)

#Initialize Window
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 704
SCALE = 32

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def game_loop():
    pygame.init()

    
    #Initialize Sprites
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.UP = [pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Player1\hero-up-{0}.png.png".format(ii)).convert() for ii in range(1,5)]
            for frame in self.UP:
                frame.set_colorkey(WHITE, RLEACCEL)
            self.DOWN = [pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Player1\hero - down-{0}.png.png".format(ii)).convert() for ii in range(1,5)]
            for frame in self.DOWN:
                frame.set_colorkey(WHITE, RLEACCEL) 
            self.LEFT = [pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Player1\hero-left-{0}.png.png".format(ii)).convert() for ii in range(1,5)]
            for frame in self.LEFT:
                frame.set_colorkey(WHITE, RLEACCEL) 
            self.RIGHT = [pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Player1\hero-right-{0}.png.png".format(ii)).convert() for ii in range(1,5)]
            for frame in self.RIGHT:
                frame.set_colorkey(WHITE, RLEACCEL)
            self.PLANT = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Player1\hero-plant.png").convert()
            self.PLANT.set_colorkey(WHITE, RLEACCEL)
            self.surf = self.UP[-1]
            self.rect = self.surf.get_rect()
        
        def check_pos_open(self, x, y):
            self.open = -10
            try:
                if x >= 0 and y >= 0:
                    self.open = game_map[y][x]
            except IndexError:
                self.open = -10
            return self.open
        
    class Sun(pygame.sprite.Sprite):
        def __init__(self):
            super(Sun, self).__init__()
            self.sungif = [pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Sun1\sun1_Imported animation_{0}.gif.png".format(ii)).convert() for ii in range(0,61)]
            for frame in self.sungif:
                frame.set_alpha(50)
            self.surf = self.sungif[0]
            self.rect = self.surf.get_rect()
    
    class Tree(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Tree, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\tree1.png").convert()
            self.surf.set_colorkey((0, 0, 0, 0), RLEACCEL)
            self.rect = (loc[0]+8, loc[1]+4)
    
    class Dot(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Dot, self).__init__()
            self.RED = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\red_dot.png").convert()
            self.RED.set_colorkey((0, 0, 0, 0), RLEACCEL)
            self.BLACK = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\black_dot.png").convert()
            self.BLACK.set_colorkey((255, 255, 255, 0), RLEACCEL)
            self.surf = self.RED
            self.rect = loc
            
    class Log(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Log, self).__init__()
            
            self.SHORT = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Logs\short_log.png").convert()
            self.SHORT.set_colorkey((0,0,0,0), RLEACCEL)
            self.LONG = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Logs\long_log.png").convert()
            self.LONG.set_colorkey((0,0,0,0), RLEACCEL)
            self.LONGVERT = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\long_log_vert.png").convert()
            self.LONGVERT.set_colorkey((0,0,0,0), RLEACCEL)
            self.SHORTVERT = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\short_log_vert.png").convert()
            self.SHORTVERT.set_colorkey((0,0,0,0), RLEACCEL)
            self.surf = self.SHORT
            self.rect = loc
    
    class Cache(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Cache, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\cache.png").convert()
            self.surf.set_colorkey((0, 0, 0, 0), RLEACCEL)
            self.rect = loc
    
    class Background_grass(pygame.sprite.Sprite):
        def __init__(self):
            super(Background_grass, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Map Layers\Map_Background.png").convert()
            self.surf.set_colorkey((0, 0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect()
            
    class Background_forest(pygame.sprite.Sprite):
        def __init__(self):
            super(Background_forest, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Map Layers\Map_Forest.png").convert()
            self.surf.set_colorkey((0, 0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect()
    
    class Background_road(pygame.sprite.Sprite):
        def __init__(self):
            super(Background_road, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Map Layers\Map_Road.png").convert()
            self.surf.set_colorkey((0, 0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect()
    
    class Background_UI(pygame.sprite.Sprite):
        def __init__(self):
            super(Background_UI, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Map Layers\Map_UI.png").convert()
            TRANSCOLOR = self.surf.get_at((0,0))
            self.surf.set_colorkey(TRANSCOLOR, RLEACCEL)
            self.rect = self.surf.get_rect()
    
    class Hearts(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Hearts, self).__init__()
            self.THREE = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\heart_3.png").convert()
            self.THREE.set_colorkey(WHITE, RLEACCEL)
            self.TWO = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\heart_2.png").convert()
            self.TWO.set_colorkey(WHITE, RLEACCEL)
            self.ONE = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\heart_1.png").convert()
            self.ONE.set_colorkey(WHITE, RLEACCEL)
            self.surf = self.THREE
            self.rect = loc
    
    #Movement Queue
    class Queue(object):
        def __init__(self):
            self.storage = []

        def enqueue(self, new_element):
            self.storage.append(new_element)
            new_dot = new_element[1]
            dots.add(new_dot)
            
        def peek_front(self):
            return self.storage[0]
        
        def peek_back(self):
            return self.storage[-1]

        def dequeue(self):
            self.storage[0][1].kill()
            return self.storage.pop(0)
        
        def undo(self):
            self.storage[-1][1].kill()
            return self.storage.pop()
        
    #Text drawing functions
    def text_objects(text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()
    
    def message_display(text, loc):
        smallText = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = text_objects(text, smallText)
        TextRect.center = loc
        screen.blit(TextSurf, TextRect)
    
    screen_width = 24
    screen_height = 22
    num_logs = 5
    raw_map = txt_to_array(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\Map Layers\day_one.txt")
    game_map_total = gen_map(raw_map, num_logs)
    game_map = game_map_total[0]
    tree_array = [[0 for x in range(screen_width)] for y in range(screen_height)]
    
    min_density = 1 #int(block_width * block_height * (2/9) * .9)
    
    #Add sprite groups
    trees = pygame.sprite.Group()
    logs = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    big_trees = pygame.sprite.Group()
    background_sprites = pygame.sprite.Group()
    UI_sprites = pygame.sprite.Group()
    user = pygame.sprite.Group()
    
    #Draws map background
    back_grass = Background_grass()
    back_road = Background_road()
    back_forest = Background_forest()
    back_ui = Background_UI()
    sun = Sun()
    
    background_sprites.add(back_grass)
    background_sprites.add(back_road)
    big_trees.add(back_forest)
    UI_sprites.add(back_ui)
    UI_sprites.add(sun)
    
    x_gridlines = []
    y_gridlines = []
    y_index = 0
    for yy in game_map:
        x_index = 0
        for xx in yy: 
            if xx == -3:
                new_log = Log((x_index*SCALE, y_index*SCALE))
                new_log.surf = new_log.SHORT
                logs.add(new_log)
                logs.add(new_log)
            elif xx == -4:
                new_log = Log((x_index*SCALE, y_index*SCALE))
                new_log.surf = new_log.LONG
                logs.add(new_log)
                logs.add(new_log)
            elif xx == -5:
                new_log = Log((x_index*SCALE+8, y_index*SCALE))
                new_log.surf = new_log.SHORTVERT
                logs.add(new_log)
                logs.add(new_log)
            elif xx == -6:
                new_log = Log((x_index*SCALE, y_index*SCALE))
                new_log.surf = new_log.LONGVERT
                logs.add(new_log)
                logs.add(new_log)
            x_gridlines.append([(0, y_index*SCALE), (SCREEN_WIDTH, y_index*SCALE)])
            y_gridlines.append([((y_index)*SCALE, 0), ((y_index)*SCALE, SCREEN_HEIGHT-SCALE*2)])
            x_index += 1
        y_index += 1
    y_index = 0
    
        
    #Moves the starting player position to the bottom left of screen and draws it there
    player = Player()
    x_cursor, y_cursor = game_map_total[1]
    x_player_position, y_player_position = x_cursor, y_cursor
    player.rect[0], player.rect[1] = SCALE*x_cursor, SCALE*y_cursor
    player_direction = "UP"
    user.add(player)
    
    #Adds cache to the bottom left
    CACHE_X, CACHE_Y = (x_cursor, y_cursor)
    cache = Cache((CACHE_X*SCALE, CACHE_Y*SCALE))
    game_map[CACHE_Y][CACHE_X] = 5
    background_sprites.add(cache)
    
    #Add hearts
    hearts_x = SCREEN_WIDTH - 160
    hearts_y = SCREEN_HEIGHT - 49
    hearts_sprite = Hearts((hearts_x, hearts_y))
    UI_sprites.add(hearts_sprite)

    #Initialize game parameters
    trees_in_bag = 0
    bagup_size = 40
    move_queue = Queue()
    MOVESPEED = 1 #The amount of seconds to move through each tile
    FRAMERATE = 32
    maxframecount = int(FRAMERATE * MOVESPEED)
    framecount = 60
    is_moving = False
    jump_timer = 0
    jump_time = FRAMERATE * .5
    hearts = 3
    trees_planted = 0
    total_time_in_day = 60
    time_in_day = 0
    
    #Creates movement timer event
    PLAYER_MOVE = pygame.USEREVENT + 1
    
    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()
    
    #Main Loop
    running = True
    
    while running:

        for event in pygame.event.get():
            
            pressed_keys = pygame.key.get_pressed()
            
            if event.type == PLAYER_MOVE:
                if len(move_queue.storage) > 0:
                    player.rect[0], player.rect[1] = SCALE*x_player_position, SCALE*y_player_position
                    framecount = 0
                    MOVESPEED = 1
                    pygame.time.set_timer(PLAYER_MOVE, 1000*MOVESPEED)
                    direction = move_queue.dequeue()[0]
                    if direction == (0, -2) or direction == (0, 2) or direction == (2, 0) or direction == (-2, 0):
                        MOVESPEED = 3
                        pygame.time.set_timer(PLAYER_MOVE, 1000*MOVESPEED)
                    maxframecount = int(FRAMERATE * MOVESPEED)
                    print(maxframecount)
                    x_player_position += direction[0]
                    y_player_position += direction[1]
                    if direction[1] < 0:
                        player_direction = "UP"
                    elif direction[1] > 0:
                        player_direction = "DOWN"
                    elif direction[0] > 0:
                        player_direction = "RIGHT"
                    elif direction[0] < 0:
                        player_direction = "LEFT"
                    elif direction == (0,0):
                        player_direction = "PLANT"
                        new_tree = Tree((player.rect[0], player.rect[1]))
                        trees.add(new_tree)
                        trees_in_bag -= 1
                        trees_planted += 1
                        
                        #Check if there's a too close
                        if tree_array[y_player_position][x_player_position] == 2:
                            hearts -= 1
                        tree_array[y_player_position][x_player_position] = 1
                        footprint = tree_footprint(x_player_position, y_player_position)
                        for cooridinate in footprint:
                            try:
                                tree_array[cooridinate[1]][cooridinate[0]] = 2
                            except IndexError:
                                pass
                                
                      
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
                #Movement commands
                if event.key == K_UP and player.check_pos_open(x_cursor, y_cursor-1) >= 0:
                    if not is_moving:
                        pygame.time.set_timer(PLAYER_MOVE, 1)
                    y_cursor -= 1
                    move_queue.enqueue([(0, -1), Dot((x_cursor*SCALE, y_cursor*SCALE))])

                if event.key == K_DOWN and player.check_pos_open(x_cursor, y_cursor+1) >= 0:
                    if not is_moving:
                        pygame.time.set_timer(PLAYER_MOVE, 1)
                    y_cursor += 1
                    move_queue.enqueue([(0, 1), Dot((x_cursor*SCALE, y_cursor*SCALE))])

                if event.key == K_LEFT and player.check_pos_open(x_cursor-1, y_cursor) >= 0:
                    if not is_moving:
                        pygame.time.set_timer(PLAYER_MOVE, 1)
                    x_cursor -= 1
                    move_queue.enqueue([(-1, 0), Dot((x_cursor*SCALE, y_cursor*SCALE))])

                if event.key == K_RIGHT and player.check_pos_open(x_cursor+1, y_cursor) >= 0:
                    if not is_moving:
                        pygame.time.set_timer(PLAYER_MOVE, 1)
                    x_cursor += 1
                    move_queue.enqueue([(1, 0), Dot((x_cursor*SCALE, y_cursor*SCALE))])
                
                #Plant tree command
                if event.key == K_SPACE:
                    if trees_in_bag > 0 and player.check_pos_open(x_cursor, y_cursor) == 0:
                        new_dot = Dot((x_cursor*SCALE, y_cursor*SCALE))
                        new_dot.surf = new_dot.BLACK
                        move_queue.enqueue([(0, 0), new_dot])
                    if player.check_pos_open(x_cursor, y_cursor) == 5:
                        trees_in_bag = bagup_size
                if event.key == K_LSHIFT:
                    if len(move_queue.storage) > 1:
                        undo = move_queue.undo()
                        x_cursor -= undo[0][0]
                        y_cursor -= undo[0][1]
                        
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
                    jump_timer = 0
            elif event.type == QUIT:
                running = False
        
        #Jump over log commands
        
        #Jump UP
        if player.check_pos_open(x_cursor, y_cursor - 1) < 0 and player.check_pos_open(x_cursor, y_cursor - 2) >= 0: 
            if pressed_keys[K_UP]:
                jump_timer += 1
            if jump_timer >= jump_time:
                y_cursor -= 2
                move_queue.enqueue([(0, -2), Dot((x_cursor*SCALE, y_cursor*SCALE))])
                jump_timer = 0
            
        #Jump Down
        if player.check_pos_open(x_cursor, y_cursor + 1) < 0 and player.check_pos_open(x_cursor, y_cursor + 2) >= 0: 
            if pressed_keys[K_DOWN]:
                jump_timer += 1
            if jump_timer >= jump_time:
                y_cursor += 2
                move_queue.enqueue([(0, 2), Dot((x_cursor*SCALE, y_cursor*SCALE))])
                jump_timer = 0
        
        #Jump Right
        if player.check_pos_open(x_cursor + 1, y_cursor) < 0 and player.check_pos_open(x_cursor + 2, y_cursor) >= 0:
            if pressed_keys[K_RIGHT]:
                jump_timer += 1
            if jump_timer >= jump_time:
                x_cursor += 2
                move_queue.enqueue([(2, 0), Dot((x_cursor*SCALE, y_cursor*SCALE))])
                jump_timer = 0
        
        #Jump Left
        if player.check_pos_open(x_cursor - 1, y_cursor) < 0 and player.check_pos_open(x_cursor - 2, y_cursor) >= 0:
            if pressed_keys[K_LEFT]:
                jump_timer += 1
            if jump_timer >= jump_time:
                x_cursor -= 2
                move_queue.enqueue([(-2, 0), Dot((x_cursor*SCALE, y_cursor*SCALE))])
                jump_timer = 0
            

        if framecount < maxframecount:
            
            is_moving = True
            
            if player_direction == "UP":
                player.surf = player.UP[(framecount//3)%4]
                player.rect[1] = SCALE*y_player_position - SCALE*direction[1] + int(framecount/maxframecount*SCALE*direction[1])
                framecount += 1
                
            if player_direction == "DOWN":
                player.surf = player.DOWN[(framecount//3)%4]
                player.rect[1] = SCALE*y_player_position - SCALE*direction[1] + int(framecount/maxframecount*SCALE*direction[1])
                framecount += 1
                    
            if player_direction == "LEFT":
                player.surf = player.LEFT[(framecount//3)%4]
                player.rect[0] = SCALE*x_player_position - SCALE*direction[0] + int(framecount/maxframecount*SCALE*direction[0])
                framecount += 1
                
            if player_direction == "RIGHT":
                player.surf = player.RIGHT[(framecount//3)%4]
                player.rect[0] = SCALE*x_player_position - SCALE*direction[0] + int(framecount/maxframecount*SCALE*direction[0])
                framecount += 1
            
            if player_direction == "PLANT":
                player.surf = player.PLANT
                
            print(framecount)
        else:
            is_moving = False
        
        if hearts == 3:
            hearts_sprite.surf = hearts_sprite.THREE
        elif hearts == 2:
            hearts_sprite.surf = hearts_sprite.TWO
        elif hearts == 1:
            hearts_sprite.surf = hearts_sprite.ONE
        
        for entity in background_sprites:
            screen.blit(entity.surf, entity.rect)
        
        #If you want gridlines
        for x in x_gridlines:
            pygame.draw.lines(screen, GRIDLINES, False, x)
        for y in y_gridlines:
            pygame.draw.lines(screen, GRIDLINES, False, y)
        sun.surf = sun.sungif[(total_time_in_day//60)*time_in_day]
            
        for entity in logs:
            screen.blit(entity.surf, entity.rect)
        
        for entity in dots:
            screen.blit(entity.surf, entity.rect)
            
        for entity in user:
            screen.blit(entity.surf, entity.rect)
        
        for entity in trees:
            screen.blit(entity.surf, entity.rect)
        
        for entity in big_trees:
            screen.blit(entity.surf, entity.rect)
        
        for entity in UI_sprites:
            screen.blit(entity.surf, entity.rect)
        
        time_in_day = pygame.time.get_ticks()//1000
        #print("Seconds passed:", time_in_day)
        
        message_display("Trees left in bag: %s" % trees_in_bag, (SCALE*20, SCALE*2))
        message_display("Trees Planted: %s" % trees_planted, (SCALE*20, SCALE*3))
        message_display("Minimum density: %s" % min_density, (SCALE*20, SCALE*4))
        pygame.display.update()
        clock.tick(FRAMERATE)
        
    pygame.quit()

def menu_loop():
    pygame.init()
    
    class Start(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Start, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\start_text_only.png").convert()
            TRANSCOLOR = self.surf.get_at((0,0))
            self.surf.set_colorkey(TRANSCOLOR, RLEACCEL)
            self.rect = loc
    
    class Border(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Border, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\start_border.png").convert()
            TRANSCOLOR = self.surf.get_at((0,0))
            self.surf.set_colorkey(TRANSCOLOR, RLEACCEL)
            self.rect = loc
            
    menu_sprites = pygame.sprite.Group()
    
    #initialize the start button 
    start = Start((0,0))
    start_width, start_height = start.surf.get_width(), start.surf.get_height()
    start.rect = ((SCREEN_WIDTH-start_width)/2, (SCREEN_HEIGHT-start_height)/2, start_width, start_height)
    menu_sprites.add(start)
    start_loc = start.rect
    mouse_on_start = False
    
    #Initialize the hover border
    border = Border((start_loc[0], start_loc[1]))
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        
        #Determine mouse position, which buttons are being pressed, and whether it is on the start button or not
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed
        
        if start_loc[0] < mouse_pos[0] < start_loc[0] + start_loc[2] and start_loc[1] < mouse_pos[1] < start_loc[1] + start_loc[3]:
            mouse_on_start = True
        else:
            mouse_on_start = False
        
        if mouse_on_start:
            menu_sprites.add(border)
        else:
            menu_sprites.remove(border)
        
        #Events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and mouse_on_start:
                    running = False
                    level_screen_loop()
        
            elif event.type == QUIT:
                running = False
            
        
            
        
        #Draw all the menu sprites
        screen.fill(BLACK)
        
        for entity in menu_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pygame.display.update()
        clock.tick(32)
    
    pygame.quit()
    
def level_screen_loop():
    pygame.init()
    
    class Level(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Level, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\level1.png").convert()
            TRANSCOLOR = self.surf.get_at((0,0))
            self.surf.set_colorkey(TRANSCOLOR, RLEACCEL)
            self.rect = loc
    
    class Border(pygame.sprite.Sprite):
        def __init__(self, loc):
            super(Border, self).__init__()
            self.surf = pygame.image.load(r"C:\Users\ctarr\Documents\Thonny Programs\Planting Game\Sprites\level_border.png").convert()
            TRANSCOLOR = self.surf.get_at((0,0))
            self.surf.set_colorkey(TRANSCOLOR, RLEACCEL)
            self.rect = loc
            
    level_sprites = pygame.sprite.Group()
    
    #initialize the level buttons
    level1 = Level((0,0))
    level_width, level_height = level1.surf.get_width(), level1.surf.get_height()
    level1.rect = (128, 128, level_width, level_height)
    level_sprites.add(level1)
    level1_loc = level1.rect
    mouse_on_level1 = False
    
    #Initialize the hover border
    border = Border(level1_loc)
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        
        #Determine mouse position, which buttons are being pressed, and whether it is on the start button or not
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed
        
        if level1_loc[0] < mouse_pos[0] < level1_loc[0] + level1_loc[2] and level1_loc[1] < mouse_pos[1] < level1_loc[1] + level1_loc[3]:
            mouse_on_level1 = True
        else:
            mouse_on_level1 = False
        
        if mouse_on_level1:
            level_sprites.add(border)
        else:
            level_sprites.remove(border)
        
        #Events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and mouse_on_level1:
                    running = False
                    game_loop()
        
            elif event.type == QUIT:
                running = False
        
        #Draw all the menu sprites
        screen.fill(BLACK)
        
        for entity in level_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pygame.display.update()
        clock.tick(32)
    
    pygame.quit()

#menu_loop()
game_loop()
