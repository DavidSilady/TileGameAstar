import copy

from model import *
from heapq import *


class AStar:
	def __init__(self, starting_board: Board, goal_board: Board):
		self.available_states = []  # max heap
		free_x = -1
		free_y = -1
		for y in range(starting_board.height):
			for x in range(starting_board.width):
				if starting_board.matrix[x][y] == 0:
					free_x = x
					free_y = y
					break
		starting_state = State(starting_board, goal_board, 0, free_x, free_y, -1, -1)
		heappush(self.available_states, (starting_state.value, starting_state))

	def expand(self):
		current_state: State = heappop(self.available_states)
		current_state.generate_all_states(self.available_states)


class State:
	def __init__(self, current_board: Board, goal_board: Board, num_steps, x, y, prev_x, prev_y):
		self.prev_x = prev_x
		self.prev_y = prev_y
		self.free_x = x
		self.free_y = y
		self.value = self.calculate_value() + num_steps
		self.current_board = current_board
		self.goal_board = goal_board
		self.num_steps = num_steps

	def get_current_board_copy(self):
		return copy.deepcopy(self.current_board)

	def find_pair_distance(self, wanted_value, value_x, value_y):
		for y in self.goal_board.height:
			for x in self.goal_board.width:
				if self.goal_board.matrix[x][y] == wanted_value:
					return abs(value_x - x) + abs(value_y - y)

	def calculate_value(self):
		board_value = 0
		for y in range(self.current_board.height):
			for x in range(self.current_board.width):
				board_value += self.find_pair_distance(self.current_board.matrix[x][y], x, y)
		return board_value

	def generate_state(self, available_states, x_offset=0, y_offset=0):
		transformed_board = self.get_current_board_copy()
		transformed_board.swap_values(self.free_x + x_offset, self.free_y + y_offset, self.free_x, self.free_y)
		new_state = State(transformed_board,
		                  self.goal_board,
		                  self.num_steps + 1,
		                  self.free_x + x_offset,
		                  self.free_y + y_offset,
		                  self.free_x,
		                  self.free_y)
		heappush(available_states, (-new_state.value, new_state))  # all values must be negated to form a max heap in heapq

	def generate_all_states(self, available_states):  # nobody touch my spaghetti
		if self.free_y - 1 >= 0:  # checking above
			self.generate_state(available_states, y_offset=-1)

		if self.free_y + 1 < self.current_board.height:  # checking below
			self.generate_state(available_states, y_offset=1)

		if self.free_x - 1 >= 0:  # checking left
			self.generate_state(available_states, x_offset=-1)

		if self.free_x + 1 < self.current_board.width:  # checking right
			self.generate_state(available_states, x_offset=1)



