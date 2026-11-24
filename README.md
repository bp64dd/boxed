# Boxed
A 2D puzzle game, similar to [_Chip's Challenge (1989)_](https://en.wikipedia.org/wiki/Chip%27s_Challenge)

_Boxed_ is a little topdown puzzle game where you control Boxy, a box collector, towards a series of mazes with enemies and traps

## Requiements
To run _Boxed_, you need to install Python on your computer, and the install pygame CE by typing in a terminal window `pip install pygame-ce`, or `pip3 install pygame-ce` if you're using a Mac or a Linux system.

You might need to install tkinter to use the built-in level editor (_editor.py_). This may vary depending on the operating system or distribution you are using.

After that, run `boxed.py` to play the game

## How to play
_Boxed_ is a game where you need to guide Boxy through the exit of every maze. You do this by using the `Arrow Keys` on the keyboard. However, when starting a level, the exit may be locked; to unlock it, collect all the boxes in a level. There are also Point Pegs present in the level that increase your score

In the mazes you may find Spikeballs and Robots; Spikeballs are static obstacles, but Robots can follow Boxy. Be sure to avoid them, or you need to play the level from the start

## Extending the game
The levels in _Boxed_ are stored as simple .txt files in the `levels` folders. You can edit the built-in levels or create new ones with any text editor, or you can use the level editor (`editor.py`).