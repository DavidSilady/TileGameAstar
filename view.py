from graphic_board import *
from tkinter import *


def init_gui(starting_board=None, size=75, width=3, height=3, margin=5):
	canvas_width = width * (margin + size)
	root_width = (canvas_width * 2) + size
	root_height = height * (margin + size)
	root_dimensions = str(root_width) + "x" + str(root_height)
	root = Tk()
	root.geometry(root_dimensions)

	starting_board = Board(width, height)
	goal_board = Board(width, height)

	work_canvas = Canvas(root, width=canvas_width, height=root_height)
	work_canvas.pack(side='left')

	goal_canvas = Canvas(root, width=canvas_width, height=root_height)
	goal_canvas.pack(side='right')

	graphic_work_board = GraphicBoard(starting_board, work_canvas)
	graphic_work_board.draw_tiles(size=size, margin=margin)

	graphic_goal_board = GraphicBoard(goal_board, goal_canvas)
	graphic_goal_board.draw_tiles(size=size, margin=margin)

	root.mainloop()


