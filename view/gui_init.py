import time

from model.a_star import AStar
from view.graphic_board import *
from tkinter import *
from model.board import Board


def init_gui(primary_board=None, secondary_board=None, size=75, width=3, height=3, margin=5):
	canvas_width = width * (margin + size)
	root_width = (canvas_width * 2) + size * 2
	root_height = height * (margin + size)
	root_dimensions = str(root_width) + "x" + str(root_height)
	root = Tk()
	root.geometry(root_dimensions)

	primary_canvas = Canvas(root, width=canvas_width, height=root_height)
	primary_canvas.pack(side='left')

	secondary_canvas = Canvas(root, width=canvas_width, height=root_height)
	secondary_canvas.pack(side='right')

	control_canvas = Canvas(root, width=root_width, height=root_height)
	control_canvas.pack(side='top')

	draw_boards(primary_canvas, secondary_canvas, control_canvas, width, height, size, margin,
	            primary_board,
	            secondary_board)

	root.mainloop()


def solve(primary_board, secondary_board, primary_graphic_board: GraphicBoard, secondary_graphic_board: GraphicBoard):
	start = time.time()
	a_star = AStar(primary_board, secondary_board)
	solution, is_solved = a_star.find_solution()

	if solution is not None and is_solved:
		for coordinates in solution:
			primary_graphic_board.move_empty(coordinates)
	elif solution is not None and not is_solved:
		solution.reverse()
		for coordinates in solution:
			coordinates = (-coordinates[0], -coordinates[1])
			secondary_graphic_board.move_empty(coordinates)
	end = time.time()
	print("Time elapsed: ", end - start)


def hint(primary_board, secondary_board, primary_graphic_board: GraphicBoard):
	a_star = AStar(primary_board, secondary_board)
	solution, is_solved = a_star.find_solution()

	if solution is not None and is_solved:
		primary_graphic_board.move_empty(solution[0])


def new_button(canvas: Canvas, size, x, y, text):
	rectangle = canvas.create_rectangle(x, y, x + size, y + size/2, fill="Black", width=0)
	center_x = x + (size / 2)
	center_y = y + (size / 4)
	text = canvas.create_text(center_x, center_y, text=text, fill="white", font="100")
	return rectangle, text


def draw_buttons(canvas: Canvas, primary_canvas, secondary_canvas,
                 primary_board, secondary_board, graphic_board, sec_graphic_board, size=130, x=0, y=0):
	def on_enter(e, button):
		canvas.itemconfig(button, fill="red")

	def on_leave(e, button):
		canvas.itemconfig(button, fill="black")

	solve_rectangle, solve_text = new_button(canvas, size, x, y, "Solve")
	canvas.tag_bind(solve_rectangle, "<Button-1>", lambda event: solve(primary_board, secondary_board, graphic_board,
	                                                                   sec_graphic_board))
	canvas.tag_bind(solve_text, "<Button-1>", lambda event: solve(primary_board, secondary_board, graphic_board,
	                                                              sec_graphic_board))
	canvas.tag_bind(solve_rectangle, "<Enter>", lambda event: on_enter(event, solve_rectangle))
	canvas.tag_bind(solve_text, "<Enter>", lambda event: on_enter(event, solve_rectangle))
	canvas.tag_bind(solve_rectangle, "<Leave>", lambda event: on_leave(event, solve_rectangle))

	hint_rectangle, hint_text = new_button(canvas, size, x, y + (size / 2) + 15, "Hint")
	canvas.tag_bind(hint_rectangle, "<Button-1>", lambda event: hint(primary_board, secondary_board, graphic_board))
	canvas.tag_bind(hint_text, "<Button-1>", lambda event: hint(primary_board, secondary_board, graphic_board))
	canvas.tag_bind(hint_rectangle, "<Enter>", lambda event: on_enter(event, hint_rectangle))
	canvas.tag_bind(hint_text, "<Enter>", lambda event: on_enter(event, hint_rectangle))
	canvas.tag_bind(hint_rectangle, "<Leave>", lambda event: on_leave(event, hint_rectangle))

	shuffle_rect, shuffle_text = new_button(canvas, size, x, y + size + 30, "Shuffle")
	canvas.tag_bind(shuffle_rect, "<Button-1>", lambda event: draw_boards(primary_canvas,
	                                                                      secondary_canvas,
	                                                                      canvas,
	                                                                      primary_board.width,
	                                                                      primary_board.height,
	                                                                      graphic_board.tiles[0][0].size,
	                                                                      graphic_board.tiles[0][0].margin))
	canvas.tag_bind(shuffle_text, "<Button-1>", lambda event: draw_boards(primary_canvas,
	                                                                      secondary_canvas,
	                                                                      canvas,
	                                                                      primary_board.width,
	                                                                      primary_board.height,
	                                                                      graphic_board.tiles[0][0].size,
	                                                                      graphic_board.tiles[0][0].margin))

	canvas.tag_bind(shuffle_rect, "<Enter>", lambda event: on_enter(event, shuffle_rect))
	canvas.tag_bind(shuffle_text, "<Enter>", lambda event: on_enter(event, shuffle_rect))
	canvas.tag_bind(shuffle_rect, "<Leave>", lambda event: on_leave(event, shuffle_rect))


def draw_boards(primary_canvas, secondary_canvas, control_canvas, width, height, size, margin,
                primary_board=None,
                secondary_board=None):
	primary_canvas.delete("all")
	secondary_canvas.delete("all")
	control_canvas.delete("all")
	if primary_board is None:
		primary_board = Board(width, height)
	if secondary_board is None:
		secondary_board = Board(width, height)

	primary_graphic_board = GraphicBoard(primary_board, secondary_board, primary_canvas)
	secondary_graphic_board = GraphicBoard(secondary_board, primary_board, secondary_canvas)

	primary_graphic_board.draw_tiles(size=size,
	                                 sister_g_board=secondary_graphic_board,
	                                 margin=margin,
	                                 goal_board=secondary_board)
	secondary_graphic_board.draw_tiles(size=size,
	                                   sister_g_board=primary_graphic_board,
	                                   margin=margin,
	                                   goal_board=primary_board)

	draw_buttons(control_canvas, primary_canvas, secondary_canvas, primary_board, secondary_board,
	             primary_graphic_board, secondary_graphic_board)




