import time

from view import *
from model import *
from tkinter import *


class Tile:  # inner Tile class
	def __init__(self, x=0, y=0, value=0, size=50):
		self.x = x
		self.y = y
		self.size = size
		self.value = value
		self.background = None
		self.text = None
		self.margin = 10

	def mouse_clicked(self, event, primary_board: Board, secondary_board: Board, canvas):
		direction_x, direction_y = primary_board.interact(self.x, self.y)
		self.move_tile(direction_x, direction_y, canvas, speed=100)
		self.x += direction_x
		self.y += direction_y
		self.check_color(primary_board, secondary_board, canvas)

	def check_color(self, primary_board: Board, secondary_board: Board, canvas: Canvas):
		if primary_board.matrix[self.x][self.y] == secondary_board.matrix[self.x][self.y]:
			canvas.itemconfig(self.background, fill="red")
		else:
			canvas.itemconfig(self.background, fill="black")

	def draw(self, canvas: Canvas, x, y, primary_board: Board, secondary_board: Board = None, size=50, margin=5):
		self.margin = margin
		self.size = size
		if self.value == 0:
			return
		rect_bg = "black"
		real_x = int(x / size)
		real_y = int(y / size)
		if secondary_board is not None:
			if primary_board.matrix[real_x][real_y] == secondary_board.matrix[real_x][real_y]:
				rect_bg = "red"
		self.background = canvas.create_rectangle(x, y, x + size, y + size, fill=rect_bg, width=0)
		center_x = x + (size / 2)
		center_y = y + (size / 2)
		self.text = canvas.create_text(center_x, center_y, text=str(self.value), fill="white", font="100")
		canvas.tag_bind(self.background, "<Button-1>",
		                lambda event: self.mouse_clicked(event,
		                                                 primary_board,
		                                                 secondary_board,
		                                                 canvas))
		canvas.tag_bind(self.text, "<Button-1>", lambda event: self.mouse_clicked(event,
		                                                                          primary_board,
		                                                                          secondary_board,
		                                                                          canvas))

	def move_tile(self, direction_x, direction_y, canvas, speed=100, rect_bg="black"):
		speed = 0.05 / speed
		if self.value == 0:
			return
		for offset in range(0, self.size + self.margin):
			time.sleep(speed)
			canvas.move(self.background, direction_x, direction_y)
			canvas.move(self.text, direction_x, direction_y)
			canvas.update()


class GraphicBoard:
	def __init__(self, primary_board: Board, secondary_board: Board, canvas):
		self.primary_board = primary_board
		self.secondary_board = secondary_board
		self.canvas = canvas
		self.tiles: List(List(Tile)) = [[Tile() for i in range(self.primary_board.height)]
		                                for j in range(self.primary_board.width)]

	def debug(self):
		output = ""
		for y in range(self.primary_board.height):
			for x in range(self.primary_board.width):
				output += " " + str(self.tiles[x][y].value)
			print(output)
			output = ""

	def swap_tiles(self, x1, y1, x2, y2):
		print("Swapping: ", x1, y1, " for ", x2, y2)
		tmp = self.tiles[x1][y1]
		self.tiles[x1][y1] = self.tiles[x2][y2]
		self.tiles[x2][y2] = tmp

		self.tiles[x1][y1].x = x1
		self.tiles[x1][y1].y = y1
		self.tiles[x2][y2].x = x2
		self.tiles[x2][y2].y = y2

	def move_empty(self, coordinates):
		x, y = self.primary_board.get_empty()
		directions = self.primary_board.interact(x + coordinates[0], y + coordinates[1])
		self.tiles[x + coordinates[0]][y + coordinates[1]].move_tile(directions[0], directions[1], self.canvas, speed=100)
		self.swap_tiles(x, y, x + coordinates[0], y + coordinates[1])
		self.tiles[x][y].check_color(self.primary_board, self.secondary_board, self.canvas)
		# print(self.tiles[x + coordinates[0]][y + coordinates[1]].x, self.tiles[x + coordinates[0]][y + coordinates[1]].y)

	def draw_tiles(self, size, margin=5, goal_board: Board = None):
		tiles = [[None for i in range(self.primary_board.height)] for j in range(self.primary_board.width)]
		for y in range(self.primary_board.height):
			for x in range(self.primary_board.width):
				new_tile = Tile(x, y, self.primary_board.matrix[x][y])
				new_tile.draw(self.canvas,
				              (x * size) + (x * margin),
				              (y * size) + (y * margin),
				              self.primary_board,
				              secondary_board=goal_board,
				              size=size,
				              margin=margin)
				tiles[x][y] = new_tile
		self.tiles = tiles




