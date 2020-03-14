from a_star import AStar
from graphic_board import *
from tkinter import *
from model import Board


def solve(primary_board, secondary_board):
	a_star = AStar(primary_board, secondary_board)
	solution = a_star.find_solution()


def new_button(canvas: Canvas, primary_board, secondary_board, size=130, x=0, y=0, text="Solve"):
	def on_enter(e):
		canvas.itemconfig(rectangle, fill="red")

	def on_leave(e):
		canvas.itemconfig(rectangle, fill="black")

	rectangle = canvas.create_rectangle(x, y, x + size, y + size/2, fill="Black", width=0)
	center_x = x + (size / 2)
	center_y = y + (size / 4)
	text = canvas.create_text(center_x, center_y, text=text, fill="white", font="100")

	canvas.tag_bind(rectangle, "<Button-1>", lambda event: solve(primary_board, secondary_board))
	canvas.tag_bind(text, "<Button-1>", lambda event: solve(primary_board, secondary_board))

	canvas.tag_bind(rectangle, "<Enter>", on_enter)
	canvas.tag_bind(text, "<Enter>", on_enter)
	canvas.tag_bind(rectangle, "<Leave>", on_leave)


def init_gui(primary_board=None, size=75, width=3, height=3, margin=5):
	canvas_width = width * (margin + size)
	root_width = (canvas_width * 2) + size * 2
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

	control_canvas = Canvas(root, width=root_width, height=root_height)
	control_canvas.pack(side='top')
	new_button(control_canvas, primary_board, secondary_board, size=(2*size)-(3*margin))

	primary_graphic_board = GraphicBoard(primary_board, secondary_board, primary_canvas)
	primary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=secondary_board)

	secondary_graphic_board = GraphicBoard(secondary_board, primary_board, secondary_canvas)
	secondary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=primary_board)

	root.mainloop()
