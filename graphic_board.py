import random
import time
from tkinter import *
from typing import List
from view import *
from model import *


class GraphicBoard:
	def __init__(self, int_board: Board, height, width, canvas):
		self.int_board = int_board
		self.canvas = canvas
		self.height = height
		self.width = width

	def draw_tiles(self, size, margin=5):
		for y in range(self.height):
			for x in range(self.width):
				new_tile = self.Tile(x, y, self.int_board.matrix[x][y])
				new_tile.draw(self.canvas,
				              (x * size) + (x * margin),
				              (y * size) + (y * margin),
				              self.int_board.matrix,
				              size,
				              margin)

	class Tile:  # inner Tile class
		def __init__(self, x=0, y=0, value=0, size=50):
			self.x = x
			self.y = y
			self.size = size
			self.value = value
			self.background = None
			self.text = None
			self.margin = 5

		def mouse_clicked(self, event, model_board, canvas):
			if self.value == 0:
				return
			if self.y - 1 >= 0 and model_board[self.x][self.y - 1].value == 0:
				model_board[self.x][self.y - 1].y += 1
				model_board[self.x][self.y - 1], model_board[self.x][self.y] = swap(model_board[self.x][self.y - 1],
				                                                                    model_board[self.x][self.y])
				self.move_up(canvas, 30)
			elif self.y + 1 < len(model_board[0]) and model_board[self.x][self.y + 1].value == 0:
				model_board[self.x][self.y + 1].y -= 1
				model_board[self.x][self.y + 1], model_board[self.x][self.y] = swap(model_board[self.x][self.y + 1],
				                                                                    model_board[self.x][self.y])
				self.move_down(canvas, 30)
			elif self.x - 1 >= 0 and model_board[self.x - 1][self.y].value == 0:
				model_board[self.x - 1][self.y].x += 1
				model_board[self.x - 1][self.y], model_board[self.x][self.y] = swap(model_board[self.x - 1][self.y],
				                                                                    model_board[self.x][self.y])
				self.move_left(canvas, 30)
			elif self.x + 1 < len(model_board) and model_board[self.x + 1][self.y].value == 0:
				model_board[self.x + 1][self.y].x -= 1
				model_board[self.x + 1][self.y], model_board[self.x][self.y] = swap(model_board[self.x + 1][self.y],
				                                                                    model_board[self.x][self.y])
				self.move_right(canvas, 30)

		def draw(self, canvas: Canvas, x, y, model_board, size=50, margin=5):
			self.margin = margin
			self.size = size
			if self.value == 0:
				return
			self.background = canvas.create_rectangle(x, y, x + size, y + size, fill="black")
			center_x = x + (size / 2)
			center_y = y + (size / 2)
			self.text = canvas.create_text(center_x, center_y, text=str(self.value), fill="white", font="100")
			canvas.tag_bind(self.background, "<Button-1>", lambda event: self.mouse_clicked(event, model_board, canvas))
			canvas.tag_bind(self.text, "<Button-1>", lambda event: self.mouse_clicked(event, model_board, canvas))

		def move_up(self, canvas: Canvas, speed=10):
			self.move_tile(0, -1, canvas, speed)
			self.y -= 1

		def move_down(self, canvas: Canvas, speed=10):
			self.move_tile(0, 1, canvas, speed)
			self.y += 1

		def move_right(self, canvas: Canvas, speed=10):
			self.move_tile(1, 0, canvas, speed)
			self.x += 1

		def move_left(self, canvas: Canvas, speed=10):
			self.move_tile(-1, 0, canvas, speed)
			self.x -= 1

		def move_tile(self, direction_x, direction_y, canvas, speed=10):
			speed = 0.1 / speed
			if self.value == 0:
				return
			for offset in range(0, self.size + self.margin):
				time.sleep(speed)
				canvas.move(self.background, direction_x, direction_y)
				canvas.move(self.text, direction_x, direction_y)
				canvas.update()


BOARD = Board(5, 6)
init_gui(BOARD)


