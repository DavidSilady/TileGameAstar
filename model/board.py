import random
from typing import List


class Board:
	def __init__(self, width, height, matrix=None):
		self.width = width
		self.height = height
		if matrix is None:
			self.matrix: List[List[int]] = self.generate_tiles()
		else:
			self.matrix = matrix

	def get_empty(self):
		"""
		:return: coordinates of empty space in the matrix (0)
		"""
		for y in range(self.height):
			for x in range(self.width):
				if self.matrix[y][x] == 0:
					return x, y

	def print_tiles(self):
		for y in range(self.height):
			output = ""
			for x in range(self.width):
				output += " " + str(self.matrix[y][x])
			print(output)

	def swap_values(self, x1, y1, x2, y2):
		tmp = self.matrix[y1][x1]
		self.matrix[y1][x1] = self.matrix[y2][x2]
		self.matrix[y2][x2] = tmp

	def interact(self, x, y):
		"""
		Simulates interaction of a tile
		:param x: x coordinate of the interacted tile
		:param y: y coordinate of the interacted tile
		:return: coordinate offset to which side the tile will move
		"""
		# Check whether the interacted tile is not an empty one
		if self.matrix[y][x] == 0:
			return 0, 0
		# Check if possible movement is not out of boundaries
		if x - 1 >= 0 and self.matrix[y][x - 1] == 0:  # attempt movement: left
			self.swap_values(x, y, x - 1, y)
			x_offset = - 1
			y_offset = 0
			return x_offset, y_offset
		if x + 1 < self.width and self.matrix[y][x + 1] == 0:  # attempt movement: right
			self.swap_values(x, y, x + 1, y)
			x_offset = 1
			y_offset = 0
			return x_offset, y_offset
		if y - 1 >= 0 and self.matrix[y - 1][x] == 0:  # attempt movement: up
			self.swap_values(x, y, x, y - 1)
			x_offset = 0
			y_offset = -1
			return x_offset, y_offset
		if y + 1 < self.height and self.matrix[y + 1][x] == 0:  # attempt movement: down
			self.swap_values(x, y, x, y + 1)
			x_offset = 0
			y_offset = 1
			return x_offset, y_offset
		return 0, 0

	def generate_tiles(self):
		"""
		Generates an ascending list (0..Width x Height), Which is shuffled and put into matrix
		:return: generated matrix
		"""
		matrix: List[List[int]] = [[0 for x in range(self.width)] for y in range(self.height)]
		shuffled_values = list(range(0, self.width * self.height))
		random.shuffle(shuffled_values)
		index = 0
		for y in range(self.height):
			for x in range(self.width):
				matrix[y][x] = shuffled_values[index]
				index += 1
		return matrix



