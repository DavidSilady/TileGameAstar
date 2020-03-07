import random
from typing import List


def swap(a, b):
	tmp = a
	a = b
	b = tmp
	return a, b


def generate_tiles(width, height):
	tiles: List[List[int]] = [[0 for i in range(height)] for j in range(width)]
	shuffled_values = list(range(0, width*height))
	random.shuffle(shuffled_values)
	index = 0
	for x in range(width):
		for y in range(height):
			tiles[x][y] = shuffled_values[index]
			index += 1
	return tiles


class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.matrix: List[List[int]] = generate_tiles(width, height)

	def print_tiles(self):
		for y in range(self.height):
			output = ""
			for x in range(self.width):
				output += " " + str(self.matrix[x][y].value)
			print(output)

	def swap_values(self, x1, y1, x2, y2):
		tmp = self.matrix[x1][y1]
		self.matrix[x1][y1] = self.matrix[x2][y2]
		self.matrix[x2][y2] = tmp

	def interact(self, x, y):
		if self.matrix[x][y] == 0:
			return 0, 0
		if y - 1 >= 0 and self.matrix[x][y - 1] == 0:
			self.swap_values(x, y, x, y - 1)
			x_offset = 0
			y_offset = -1
			return x_offset, y_offset
		if y + 1 < self.height and self.matrix[x][y + 1] == 0:
			self.swap_values(x, y, x, y + 1)
			x_offset = 0
			y_offset = 1
			return x_offset, y_offset
		if x - 1 >= 0 and self.matrix[x - 1][y] == 0:
			self.swap_values(x, y, x - 1, y)
			x_offset = -1
			y_offset = 0
			return x_offset, y_offset
		if x + 1 < self.width and self.matrix[x + 1][y] == 0:
			self.swap_values(x, y, x + 1, y)
			x_offset = 1
			y_offset = 0
			return x_offset, y_offset
		return 0, 0



