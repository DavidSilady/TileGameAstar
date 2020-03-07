from model import *
from heapq import *


class AStar:
	def __init__(self, starting_board: Board, goal_board: Board):
		self.available_states = []  # max heap
		free_x = -1
		free_y = -1
		for y in range(starting_board.height):
			for x in range(starting_board.width):
				if starting_board[x][y] == 0:
					free_x = x
					free_y = y
					break
		starting_state = State(starting_board, goal_board, 0, free_x, free_y)
		heappush(self.available_states, (starting_state.value, starting_state))


class State:
	def __init__(self, current_board: Board, goal_board: Board, num_steps, x, y):
		self.free_x = x
		self.free_y = y
		self.value = self.calculate_value() - num_steps
		self.current_board = current_board
		self.goal_board = goal_board
		self.num_steps = num_steps

	def calculate_value(self):
		board_value = 0
		for y in range(self.current_board.height):
			for x in range(self.current_board.width):
				if self.current_board.matrix[x][y] == self.goal_board.matrix[x][y]:
					board_value += 1
		return board_value

	def generate_states(self, available_states):
		if self.free_y - 1 >= 0:
			up_state = State(self.current_board, self.goal_board, self.num_steps + 1, self.free_x, self.free_y - 1)
			heappush(available_states, (-up_state.value, up_state))  # all values must be negated to form a max heap in heapq
		if self.free_y + 1 < self.current_board.height:
			down_state = State(self.current_board, self.goal_board, self.num_steps + 1, self.free_x, self.free_y + 1)
			heappush(available_states, (-down_state.value, down_state))  # all values must be negated to form a max heap in heapq
		if self.free_x - 1 >= 0:
			left_state = State(self.current_board, self.goal_board, self.num_steps + 1, self.free_x - 1, self.free_y)
			heappush(available_states, (-left_state.value, left_state))  # all values must be negated to form a max heap in heapq
		if self.free_x + 1 < self.current_board.width:
			right_state = State(self.current_board, self.goal_board, self.num_steps + 1, self.free_x + 1, self.free_y)
			heappush(available_states, (-right_state.value, right_state))  # all values must be negated to form a max heap



