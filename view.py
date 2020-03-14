from a_star import AStar
from graphic_board import *
from tkinter import *
from model import Board


def init_gui(primary_board=None, size=75, width=3, height=3, margin=5):
	canvas_width = width * (margin + size)
	root_width = (canvas_width * 2) + size
	root_height = height * (margin + size)
	root_dimensions = str(root_width) + "x" + str(root_height)
	root = Tk()
	root.geometry(root_dimensions)

	primary_board = Board(width, height)
	secondary_board = Board(width, height)

	primary_canvas = Canvas(root, width=canvas_width, height=root_height)
	primary_canvas.pack(side='left')

	secondary_canvas = Canvas(root, width=canvas_width, height=root_height)
	secondary_canvas.pack(side='right')

	primary_graphic_board = GraphicBoard(primary_board, secondary_board, primary_canvas)
	primary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=secondary_board)

	secondary_graphic_board = GraphicBoard(secondary_board, primary_board, secondary_canvas)
	secondary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=primary_board)

	a_star = AStar(primary_board, secondary_board)
	a_star.find_solution()

	root.mainloop()


