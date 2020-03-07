from random import *
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
		self.tiles: List[List[int]] = generate_tiles(width, height)

	def print_tiles(self):
		for y in range(self.height):
			output = ""
			for x in range(self.width):
				output += " " + str(self.tiles[x][y].value)
			print(output)




