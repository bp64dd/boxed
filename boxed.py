# Import libraries
import pygame
import os
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Window constants
FPS = 30
SCR_WIDTH = 800
SCR_HEIGHT = 600

# Map constans
TILE_SIZE = 32
GRID_WIDTH = 25
GRID_HEIGHT = 18

# P = Player, W = Wall, G = Lock, K = Box, S = Spikeball, E = Exit, R = Robot, O = Point
TEST_MAP = ["WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WP----------------------W",
            "W--W---W--WWWWWW--R-----W",
            "W--WW--W--W----W--------W",
            "W--W-W-W--W----W---R----W",
            "W--W--WW--W----W--------W",
            "W--W---W--WWWWWW----R---W",
            "W-----------------------W",
            "W--W------------W-K-----W",
            "W--W------------W-------W",
            "W--W-K----------W-------W",
            "W--W------------W-------W",
            "W--WWWWW--------WWWWW---W",
            "W-------W------W--------W",
            "W--------W--K-W--------GE",
            "W--K------W--W----------W",
            "W----------WW-----------W",
            "WWWWWWWWWWWWWWWWWWWWWWWWW"]

current_level = 0
def load_level(level_index):
    global current_map

    with open(os.path.join("levels", LEVELS[level_index]), encoding="utf-8") as level_file:
            current_map = [line.rstrip("\r\n") for line in level_file]

try:
    LEVELS = sorted(
        f for f in os.listdir("levels") if os.path.isfile(os.path.join("levels", f)) and f.endswith(".txt")
    )
    load_level(current_level)
except IndexError:
    print("No levels found in the 'levels' directory. Put .txt levels in the levels folder")
    current_map = TEST_MAP  # Fallback to test map if no levels are available

SOLID_TILES = ["W", "G", "S"]
HAZARD_TILES = ["S"]

# Sprites constants
P_LEFT_SPRITE = pygame.image.load("sprites/pidleleft.png")
P_RIGHT_SPRITE = pygame.image.load("sprites/pidleright.png")
P_UP_SPRITE = pygame.image.load("sprites/pidleup.png")
P_DOWN_SPRITE = pygame.image.load("sprites/pidledown.png")
BACK_SPRITE = pygame.image.load("sprites/back.png")
WALL_SPRITE = pygame.image.load("sprites/wall.png")
BOX_SPRITE = pygame.image.load("sprites/box.png")
LOCK_SPRITE = pygame.image.load("sprites/lock.png")
SPIKEBALL_SPRITE = pygame.image.load("sprites/spikeball.png")
EXIT_SPRITE = pygame.image.load("sprites/exit.png")
ROBOT_UP_SPRITE = pygame.image.load("sprites/robotup.png")
ROBOT_DOWN_SPRITE = pygame.image.load("sprites/robotdown.png")
ROBOT_LEFT_SPRITE = pygame.image.load("sprites/robotleft.png")
ROBOT_RIGHT_SPRITE = pygame.image.load("sprites/robotright.png")
POINT_SPRITE = pygame.image.load("sprites/point.png")

# Remove background from sprites
P_LEFT_SPRITE.set_colorkey("white")
P_RIGHT_SPRITE.set_colorkey("white")
P_UP_SPRITE.set_colorkey("white")
P_DOWN_SPRITE.set_colorkey("white")
SPIKEBALL_SPRITE.set_colorkey("white")
BOX_SPRITE.set_colorkey("white")
LOCK_SPRITE.set_colorkey("white")
EXIT_SPRITE.set_colorkey("white")
ROBOT_UP_SPRITE.set_colorkey("white")
ROBOT_DOWN_SPRITE.set_colorkey("white")
ROBOT_LEFT_SPRITE.set_colorkey("white")
ROBOT_RIGHT_SPRITE.set_colorkey("white")
POINT_SPRITE.set_colorkey("white")

# Sounds constants
WIN_SOUND = pygame.mixer.Sound("sounds/win.wav")
LOSE_SOUND = pygame.mixer.Sound("sounds/lose.wav")
CANT_MOVE_SOUND = pygame.mixer.Sound("sounds/cantmove.wav")
MOVE_SOUND = pygame.mixer.Sound("sounds/move.wav")
BOX_SOUND = pygame.mixer.Sound("sounds/box.wav")
POINT_SOUND = pygame.mixer.Sound("sounds/point.wav")

# Initialize window and clock
icon = pygame.image.load("sprites/icon.png")
icon.set_colorkey("white")
pygame.display.set_icon(icon)
pygame.display.set_caption("Boxed - An aMAZEing game!")
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
clock = pygame.time.Clock()

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = ROBOT_DOWN_SPRITE

    def move(self):
        global game_over, px, py, current_map, TILE_SIZE
        global ROBOT_DOWN_SPRITE, ROBOT_LEFT_SPRITE, ROBOT_RIGHT_SPRITE, ROBOT_UP_SPRITE
        if game_over: return

        if random.randint(0, 4) == 0:
            self.move_randomly()
        else:
            if px > self.x and not current_map[self.y // TILE_SIZE][(self.x + TILE_SIZE) // TILE_SIZE] in SOLID_TILES:
                self.x += TILE_SIZE
                self.sprite = ROBOT_RIGHT_SPRITE
            elif px < self.x and not current_map[self.y // TILE_SIZE][(self.x - TILE_SIZE) // TILE_SIZE] in SOLID_TILES:
                self.x -= TILE_SIZE
                self.sprite = ROBOT_LEFT_SPRITE
            elif py > self.y and not current_map[(self.y + TILE_SIZE) // TILE_SIZE][self.x // TILE_SIZE] in SOLID_TILES:
                self.y += TILE_SIZE
                self.sprite = ROBOT_DOWN_SPRITE
            elif py < self.y and not current_map[(self.y - TILE_SIZE) // TILE_SIZE][self.x // TILE_SIZE] in SOLID_TILES:
                self.y -= TILE_SIZE
                self.sprite = ROBOT_UP_SPRITE
            else:
                self.move_randomly()

        self.check_collision(px, py)

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))

    def move_randomly(self):
        moved = False
        while not moved:
            direction = random.randint(0, 3)
            tile_x = self.x // TILE_SIZE
            tile_y = self.y // TILE_SIZE
        
            if direction == 0 and tile_x + 1 < len(current_map[tile_y]) and not current_map[tile_y][tile_x + 1] in SOLID_TILES:
                self.x += TILE_SIZE
                self.sprite = ROBOT_RIGHT_SPRITE
                moved = True
            elif direction == 1 and tile_x > 0 and not current_map[tile_y][tile_x - 1] in SOLID_TILES:
                self.x -= TILE_SIZE
                self.sprite = ROBOT_LEFT_SPRITE
                moved = True
            elif direction == 2 and tile_y + 1 < len(current_map) and not current_map[tile_y + 1][tile_x] in SOLID_TILES:
                self.y += TILE_SIZE
                self.sprite = ROBOT_DOWN_SPRITE
                moved = True
            elif direction == 3 and tile_y > 0 and not current_map[tile_y - 1][tile_x] in SOLID_TILES:
                self.y -= TILE_SIZE
                self.sprite = ROBOT_UP_SPRITE
                moved = True
    
    def check_collision(self, other_x, other_y):
        if self.x == other_x and self.y == other_y:
            lose_game()

class PointPeg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def draw(self):
        if not self.collected: screen.blit(POINT_SPRITE, (self.x, self.y))

    def check_collision(self, other_x, other_y):
        global score

        if self.x == other_x and self.y == other_y and not self.collected:
            self.collected = True
            score += 50
            MOVE_SOUND.stop()
            POINT_SOUND.play()

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def draw(self):
        if not self.collected: screen.blit(BOX_SPRITE, (self.x, self.y))

    def check_collision(self, other_x, other_y):
        global boxes_to_collect

        if self.x == other_x and self.y == other_y and not self.collected:
            self.collected = True
            boxes_to_collect -= 1
            MOVE_SOUND.stop()
            BOX_SOUND.play()

# Define functions
def screen_coords(x, y):
    return (x * TILE_SIZE, y * TILE_SIZE)

def lose_game():
    global game_over, LOSE_SOUND, MOVE_SOUND
    game_over = True
    MOVE_SOUND.stop()
    LOSE_SOUND.play()

def draw_level():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = current_map[y][x]
            if tile == "W":
                screen.blit(WALL_SPRITE, screen_coords(x, y))
            elif tile == "G" and boxes_to_collect > 0:
                screen.blit(LOCK_SPRITE, screen_coords(x, y))
            elif tile == "S":
                screen.blit(SPIKEBALL_SPRITE, screen_coords(x, y))
            elif tile == "E":
                screen.blit(EXIT_SPRITE, screen_coords(x, y))

def move_player(dx, dy):
    global px, py, moves, game_over, has_green_keycard, end_message, player_won
    new_x = px + dx
    new_y = py + dy

    # Check for collisions
    if current_map[new_y // TILE_SIZE][new_x // TILE_SIZE] in HAZARD_TILES:
        lose_game()
    elif current_map[new_y // TILE_SIZE][new_x // TILE_SIZE] == "E":
        end_message = "Nicely done, you won!!"
        game_over = True
        player_won = True
        WIN_SOUND.play()
    elif current_map[new_y // TILE_SIZE][new_x // TILE_SIZE] not in SOLID_TILES or current_map[new_y // TILE_SIZE][new_x // TILE_SIZE] == "G" and boxes_to_collect == 0:
        px = new_x
        py = new_y
        moves += 1
        MOVE_SOUND.play()
        for peg in point_pegs:
            peg.check_collision(px, py)
        for box in boxes:
            box.check_collision(px, py)
        for robot in robots: 
            robot.check_collision(px, py)
            robot.move()
    else:
        CANT_MOVE_SOUND.play()

def draw_text(text, x, y, size=15):
    font = pygame.font.Font("fonts/Ldfcomicsans.ttf", size)
    text_surface = font.render(text, True, "white")
    screen.blit(text_surface, (x, y))

def init_game():
    # Initialize game variables
    global px, py, psprite, moves, game_over, end_message, restart_timer, restart_timer_value
    global player_won, LEVELS, current_level, robots, score, point_pegs, boxes, boxes_to_collect

    px = 32
    py = 32
    psprite = P_DOWN_SPRITE
    moves = 0
    game_over = False
    end_message = "Game over, try again!!"
    restart_timer_value = 4
    restart_timer = 0
    robots = []
    point_pegs = []
    boxes = []
    boxes_to_collect = 0
    score = 0

    if player_won:
        current_level += 1
        if current_level >= len(LEVELS):
            current_level = 0  # Loop back to the first level
        load_level(current_level)
        player_won = False

    # Spawn player and keycard
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if current_map[y][x] == "K":
                boxes.append(Box(x * TILE_SIZE, y * TILE_SIZE))
                boxes_to_collect += 1
            if current_map[y][x] == "P":
                px = x * TILE_SIZE
                py = y * TILE_SIZE
            if current_map[y][x] == "R":
                robots.append(Robot(x * TILE_SIZE, y * TILE_SIZE))
            if current_map[y][x] == "O":
                point_pegs.append(PointPeg(x * TILE_SIZE, y * TILE_SIZE))

dt = 0
player_won = False
init_game()

screen.blit(pygame.image.load("sprites/splash.png"), (0, 0))
draw_text("An aMAZEing game!", 550, 400)
draw_text("Version 1.0", 5, 5)
pygame.display.flip()
pygame.time.delay(3000)

pygame.mixer.music.load("music/puzzleitnes.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

# Main loop
game_running = True
while game_running:
    screen.fill("black")

    # Draw background
    screen.blit(BACK_SPRITE, (0,0))

    # Draw map
    draw_level()

    # Draw entities
    for robot in robots:
        robot.draw()
    for peg in point_pegs:
        peg.draw()
    for box in boxes:
        box.draw()

    # Draw player
    if not game_over: screen.blit(psprite, (px, py))

    # Draw texts
    if not game_over:
        if moves == 0:
            draw_text("Press arrow keys to move", 10, 578, 16)
        else:
            draw_text("Moves: " + str(moves) + " - Boxes to collect: " + str(boxes_to_collect) + " - Score: " + str(score) + " - Level " + str(current_level+1), 10, 578, 16)
    else:
        draw_text(end_message, 10, 578, 16)

    # Check pygame events (keys and window closing)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: # Player just pressed a key?
            # Player movement
            if event.key == pygame.K_DOWN and not game_over:
                move_player(0, TILE_SIZE)
                psprite = P_DOWN_SPRITE
            if event.key == pygame.K_UP and not game_over:
                move_player(0, -TILE_SIZE)
                psprite = P_UP_SPRITE
            if event.key == pygame.K_RIGHT and not game_over:
                move_player(TILE_SIZE, 0)
                psprite = P_RIGHT_SPRITE
            if event.key == pygame.K_LEFT and not game_over:
                move_player(-TILE_SIZE, 0)
                psprite = P_LEFT_SPRITE
            
        if event.type == pygame.QUIT: # Player wants to close the window?
            game_running = False # Exit the main loop, end of the program

    if game_over:
        restart_timer += dt / 1000
        if restart_timer >= restart_timer_value:
            init_game()

    # Update the game window
    pygame.display.update()
    dt = clock.tick(FPS)

pygame.quit()