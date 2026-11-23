import pygame
from tkinter import filedialog, messagebox

pygame.init()

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

# P= Player, W = Wall, G = Green lock, K = Green keycard, S = Spikeball, E = Exit
MAP = ["WWWWWWWWWWWWWWWWWWWWWWWWW",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W--------P--------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------E",
       "W-----------------------W",
       "W-----------------------W",
       "W-----------------------W",
       "WWWWWWWWWWWWWWWWWWWWWWWWW"]

NEW_MAP = MAP
TILE_SIZE = 32
GRID_WIDTH = 25
GRID_HEIGHT = 18
TILES = ["W", "G", "K", "S", "E", "P", "O", "R"]
TILE_ICONS = [WALL_SPRITE, LOCK_SPRITE, BOX_SPRITE, SPIKEBALL_SPRITE, EXIT_SPRITE, P_DOWN_SPRITE, POINT_SPRITE, ROBOT_DOWN_SPRITE]
current_tile = 0

icon = pygame.image.load("sprites/icon-editor.png")
icon.set_colorkey("white")
pygame.display.set_icon(icon)
pygame.display.set_caption("Boxed - Level Editor - Version 1.0")
screen = pygame.display.set_mode((800, 700))

def screen_coords(x, y):
    return (x * TILE_SIZE, y * TILE_SIZE)

def draw_level():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = MAP[y][x]
            if tile == "W":
                screen.blit(WALL_SPRITE, screen_coords(x, y))
            elif tile == "G":
                screen.blit(LOCK_SPRITE, screen_coords(x, y))
            elif tile == "S":
                screen.blit(SPIKEBALL_SPRITE, screen_coords(x, y))
            elif tile == "E":
                screen.blit(EXIT_SPRITE, screen_coords(x, y))
            elif tile == "K":
                screen.blit(BOX_SPRITE, screen_coords(x, y))
            elif tile == "P":
                screen.blit(P_DOWN_SPRITE, screen_coords(x, y))
            elif tile == "O":
                screen.blit(POINT_SPRITE, screen_coords(x, y))
            elif tile == "R":
                screen.blit(ROBOT_DOWN_SPRITE, screen_coords(x, y))

def draw_level_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (18, 18, 18), rect, 1)

def draw_text(text, x, y, size=15):
    font = pygame.font.Font("fonts/Ldfcomicsans.ttf", size)
    text_surface = font.render(text, True, "white")
    screen.blit(text_surface, (x, y))

def check_level_validity():
    has_player = any("P" in row for row in MAP)
    has_exit = any("E" in row for row in MAP)
    n_players = sum(row.count("P") for row in MAP)
    return has_player and has_exit and n_players == 1

running = True
while running:
    screen.fill("black")
    draw_level_grid()
    draw_level()

    draw_text("LMB to place tile, RMB to remove tile. Q to change tile. S to save, L to load and N to start a new level", 10, 630, 16)
    draw_text("Current tile: ", 10, 665, 16)
    screen.blit(TILE_ICONS[current_tile], (110, 660))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE

            if event.button == 1:  # Left click
                MAP[grid_y] = MAP[grid_y][:grid_x] + TILES[current_tile] + MAP[grid_y][grid_x + 1:]

            elif event.button == 3:  # Right click
                MAP[grid_y] = MAP[grid_y][:grid_x] + "-" + MAP[grid_y][grid_x + 1:]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # Cycle through tiles
                current_tile += 1
                if current_tile >= len(TILES):
                    current_tile = 0
            if event.key == pygame.K_n:
                MAP = NEW_MAP
                pygame.display.set_caption("Boxed - Level Editor - Version 1.0")
            
            if event.key == pygame.K_s:
                if check_level_validity():
                    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Boxed level", "*.txt")])
                    if file_path:
                        with open(file_path, "w") as f:
                            for line in MAP:
                                f.write(line + "\n")
                        messagebox.showinfo("Saved", "Level saved successfully!")
                else:
                    messagebox.showerror("Error", "Level must contain a player (P) and an exit (E) to be saved. Only one player is allowed.")
            
            if event.key == pygame.K_l:
                file_path = filedialog.askopenfilename(filetypes=[("Boxed level", "*.txt")])
                if file_path:
                    with open(file_path, "r") as f:
                        loaded_map = [line.strip() for line in f.readlines()]
                        if len(loaded_map) == GRID_HEIGHT and all(len(row) == GRID_WIDTH for row in loaded_map):
                            MAP = loaded_map
                            messagebox.showinfo("Loaded", "Level loaded successfully!")
                            pygame.display.set_caption("Boxed - Level Editor - Version 1.0 - " + file_path)
                        else:
                            messagebox.showerror("Error", "This is not a valid Boxed level")

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()