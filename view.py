import time
from graphic_board import *
from tkinter import *


def init_gui(board):
	root = Tk()
	root.geometry('680x680')

	canvas = Canvas(root, width=680, height=680, bg="white")
	canvas.pack()

	x = 5
	y = 5
	size = 75
	# canvas.create_rectangle(x, y, x + size, y + size, fill='black')

	board.draw_tiles(canvas, size, margin=5)
	root.mainloop()


