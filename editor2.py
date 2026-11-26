# THIS LEVEL EDITOR IS A WIP!!!!
# FOR NOW, USE editor.py INSTEAD

import tkinter as tk
from tkinter import messagebox as msb

TILE_SIZE = 32
GRID_WIDTH = 25
GRID_HEIGHT = 18

TILES = ["W", "G", "K", "S", "E", "P", "O", "R", "-"]
# TILE_ICONS = [WALL_SPRITE, LOCK_SPRITE, BOX_SPRITE, SPIKEBALL_SPRITE, EXIT_SPRITE, P_DOWN_SPRITE, POINT_SPRITE, ROBOT_DOWN_SPRITE, ERASER_SPRITE]
TILE_NAMES = ["Wall", "Lock", "Box", "Spikeball", "Exit", "Player", "Point peg", "Robot", "Eraser"]
current_tile = 8

root = tk.Tk()
root.geometry("800x650")
root.title("Boxed Level Editor 2 - <new>")
root.resizable(False, False)

def create_level_grid(canvas):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            canvas.create_rectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, outline="grey")

def draw_tile(event):
    mouse_x, mouse_y = event.x, event.y
    grid_x = mouse_x // TILE_SIZE
    grid_y = mouse_y // TILE_SIZE

def ask_quit():
    a = msb.askyesnocancel("Pay attention!", "Do you want to save this level before quitting?")
    root.destroy()

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_separator()
file_menu.add_command(label="Save level")
file_menu.add_command(label="Load level")
file_menu.add_separator()
file_menu.add_command(label="Quit", command=ask_quit)

tile_menu = tk.Menu(menubar, tearoff=0)
tile_menu.add_command(label="Player")
tile_menu.add_separator()
tile_menu.add_command(label="Eraser")

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Contents")
help_menu.add_separator()
help_menu.add_command(label="About...")

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Tile Palette", menu=tile_menu)
menubar.add_cascade(label="Help", menu=help_menu)

canvas = tk.Canvas(root, background="black", width=800, height=600)
canvas.pack()
create_level_grid(canvas)

tile_label = tk.Label(root, text="Current tile: " + TILE_NAMES[current_tile])
tile_label.pack()

root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()