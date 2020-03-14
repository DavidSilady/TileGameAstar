from a_star import AStar
from graphic_board import *
from tkinter import *
from model import Board


def solve(primary_board, secondary_board, primary_graphic_board: GraphicBoard):
	start = time.time()
	a_star = AStar(primary_board, secondary_board)
	solution = a_star.find_solution()

	if solution is not None:
		for coordinates in solution:
			primary_graphic_board.move_empty(coordinates)
	end = time.time()
	print("Time elapsed: ", end - start)


def hint(primary_board, secondary_board, primary_graphic_board: GraphicBoard):
	a_star = AStar(primary_board, secondary_board)
	solution = a_star.find_solution()

	if solution is not None:
		primary_graphic_board.move_empty(solution[0])


def shuffle_board(primary_graphic_board, secondary_board, canvas, size=75, margin=5):
	canvas.delete("all")
	canvas.update()
	time.sleep(1)
	primary_board = Board(secondary_board.width, secondary_board.height)
	primary_graphic_board = GraphicBoard(secondary_board, primary_board, canvas)
	primary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=secondary_board)


def new_button(canvas: Canvas, size, x, y, text):
	rectangle = canvas.create_rectangle(x, y, x + size, y + size/2, fill="Black", width=0)
	center_x = x + (size / 2)
	center_y = y + (size / 4)
	text = canvas.create_text(center_x, center_y, text=text, fill="white", font="100")
	return rectangle, text


def generate_buttons(canvas: Canvas, primary_canvas, primary_board, secondary_board, graphic_board, size=130, x=0, y=0):
	def on_enter(e, button):
		canvas.itemconfig(button, fill="red")

	def on_leave(e, button):
		canvas.itemconfig(button, fill="black")

	solve_rectangle, solve_text = new_button(canvas, size, x, y, "Solve")
	canvas.tag_bind(solve_rectangle, "<Button-1>", lambda event: solve(primary_board, secondary_board, graphic_board))
	canvas.tag_bind(solve_text, "<Button-1>", lambda event: solve(primary_board, secondary_board, graphic_board))
	canvas.tag_bind(solve_rectangle, "<Enter>", lambda event: on_enter(event, solve_rectangle))
	canvas.tag_bind(solve_text, "<Enter>", lambda event: on_enter(event, solve_rectangle))
	canvas.tag_bind(solve_rectangle, "<Leave>", lambda event: on_leave(event, solve_rectangle))

	hint_rectangle, hint_text = new_button(canvas, size, x, y + (size / 2) + 15, "Hint")
	canvas.tag_bind(hint_rectangle, "<Button-1>", lambda event: hint(primary_board, secondary_board, graphic_board))
	canvas.tag_bind(hint_text, "<Button-1>", lambda event: hint(primary_board, secondary_board, graphic_board))

	canvas.tag_bind(hint_rectangle, "<Enter>", lambda event: on_enter(event, hint_rectangle))
	canvas.tag_bind(hint_text, "<Enter>", lambda event: on_enter(event, hint_rectangle))
	canvas.tag_bind(hint_rectangle, "<Leave>", lambda event: on_leave(event, hint_rectangle))
	'''
	shuffle_rectangle, shuffle_text = new_button(canvas, size, x, y + size + 30, "Randomize")
	canvas.tag_bind(shuffle_rectangle, "<Button-1>", lambda event: shuffle_board(graphic_board,
	                                                                             secondary_board,
	                                                                             primary_canvas))
	canvas.tag_bind(shuffle_text, "<Button-1>", lambda event: shuffle_board(graphic_board,
	                                                                        secondary_board,
	                                                                        primary_canvas))
	canvas.tag_bind(shuffle_rectangle, "<Enter>", lambda event: on_enter(event, shuffle_rectangle))
	canvas.tag_bind(shuffle_text, "<Enter>", lambda event: on_enter(event, shuffle_rectangle))
	canvas.tag_bind(shuffle_rectangle, "<Leave>", lambda event: on_leave(event, shuffle_rectangle))
	'''



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

	primary_graphic_board = GraphicBoard(primary_board, secondary_board, primary_canvas)
	primary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=secondary_board)

	secondary_graphic_board = GraphicBoard(secondary_board, primary_board, secondary_canvas)
	secondary_graphic_board.draw_tiles(size=size, margin=margin, goal_board=primary_board)

	generate_buttons(control_canvas,
	                 primary_canvas,
	                 secondary_board,
	                 primary_board,
	                 primary_graphic_board,
	                 size=(2 * size) - (3 * margin))

	root.mainloop()
