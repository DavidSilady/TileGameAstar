from graphic_board import *
from tkinter import *


def init_gui(board=None):
	board = Board(5, 6)
	root = Tk()
	root.geometry('680x680')

	canvas = Canvas(root, width=680, height=680, bg="white")
	canvas.pack()

	graphic_board = GraphicBoard(board, canvas)
	graphic_board.draw_tiles(75)

	root.mainloop()


