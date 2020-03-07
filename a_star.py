from model import *


class State:
	def __init__(self, current_board: Board, goal_board: Board, num_steps, prev_state):
		self.value = self.calculate_value() - num_steps
		self.current_board = current_board
		self.goal_board = goal_board
		self.prev_state = prev_state

	def calculate_value(self):
		board_value = 0
		for y in range(self.current_board.height):
			for x in range(self.current_board.width):
				if self.current_board.matrix[x][y] == self.goal_board.matrix[x][y]:
					board_value += 1
		return board_value




