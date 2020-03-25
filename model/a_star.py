import copy

from model.board import *
from heapq import *

DICTIONARY = {
	"(0, 1)": "Down",
	"(0, -1)": "Up",
	"(1, 0)": "Right",
	"(-1, 0)": "Left"
}


class AStar:
	def __init__(self, starting_board: Board, goal_board: Board, state_limit):
		self.available_states_heap = []  # max heap
		self.state_limit = state_limit  # limit, where the algorithm will prematurely stop
		self.generated_states_set = set()  # hash set of all generated matrices as strings
		free_x, free_y = goal_board.get_empty()

		starting_state = State(goal_board, starting_board, 0, free_x, free_y, None)
		self.generated_states_set.add(str(starting_state.current_board.matrix))
		heappush(self.available_states_heap, (starting_state.value, 0, starting_state))
		# heap item form: Tuple(state.value, len(all generated states), state)
		# length of all generated states required as a second backup comparison value in case two state values equal

	def expand(self):
		current_state = heappop(self.available_states_heap)[2]
		if current_state.current_board.matrix == current_state.goal_board.matrix:
			return current_state
		current_state.generate_all_states(self.available_states_heap, self.generated_states_set)
		return None

	def __find_final_state(self):
		while True:
			if len(self.available_states_heap) == 0:
				print("No possible solution.")
				return None, False
			final_state: State = self.expand()
			if final_state is not None:
				print("Solution found!")
				return final_state, True
			if len(self.generated_states_set) > self.state_limit:
				print("Prematurely ending. . .")
				return heappop(self.available_states_heap)[2], False

	def find_solution(self):
		current_state, is_solved = self.__find_final_state()
		if current_state is None:
			print("Not solvable.")
			return None, False
		if current_state.prev_state is None:
			print("Wow, does not need solving.")
			return None, False
		return self.backtrack(current_state), is_solved

	@staticmethod
	def backtrack(current_state):
		solution = []
		index = 1
		while True:
			#
			move_coordinates = (current_state.prev_state.free_x - current_state.free_x,
			                    current_state.prev_state.free_y - current_state.free_y)

			solution.append(move_coordinates)
			print(index, DICTIONARY[str(move_coordinates)])
			index += 1
			current_state = current_state.prev_state
			if current_state.prev_state is None:
				return solution


class State:
	def __init__(self, current_board: Board, goal_board: Board, num_steps, x, y, prev_state):
		self.prev_state: State = prev_state
		self.free_x = x
		self.free_y = y
		self.current_board = current_board
		self.goal_board = goal_board
		self.num_steps = num_steps
		self.value = num_steps + self.calculate_weighted_distance_value()

	def get_current_board_copy(self):
		return copy.deepcopy(self.current_board)

	def find_pair_distance(self, wanted_value, current_x, current_y):
		"""
		:param wanted_value: value we are searching for
		:param current_x: x coordinate of the value in self current matrix
		:param current_y: y coordinate of the value in self current matrix
		:return: distance from current value position to goal value position
		"""
		for y in range(self.goal_board.height):
			for x in range(self.goal_board.width):
				if self.goal_board.matrix[y][x] == wanted_value:
					return abs(current_x - x) + abs(current_y - y)

	def calculate_match_value(self):
		# Heuristic num. 1
		board_value = 0
		for y in range(self.current_board.height):
			for x in range(self.current_board.width):
				if self.current_board.matrix[y][x] != self.goal_board.matrix[y][x]:
					board_value += 1
		return board_value

	def calculate_distance_value(self):
		# Heuristic num. 2
		board_value = 0
		for y in range(self.current_board.height):
			for x in range(self.current_board.width):
				board_value += self.find_pair_distance(self.current_board.matrix[y][x], x, y)
		return board_value

	def calculate_weighted_distance_value(self):
		# Heuristic num. 3 (combination of 1. and 2.)
		board_value = 0
		for y in range(self.current_board.height):
			for x in range(self.current_board.width):
				board_value += self.find_pair_distance(self.current_board.matrix[y][x], x, y)
				if self.current_board.matrix[y][x] != self.goal_board.matrix[y][x]:
					board_value += 1
		return board_value

	def generate_state(self, available_states, generated_states_set, x_offset=0, y_offset=0):
		transformed_board = self.get_current_board_copy()  # Important not to pass just a pointer
		transformed_board.swap_values(self.free_x + x_offset, self.free_y + y_offset, self.free_x, self.free_y)
		if str(transformed_board.matrix) in generated_states_set:  # Check if not already generated
			return
		new_state = State(transformed_board,
		                  self.goal_board,
		                  self.num_steps + 1,
		                  self.free_x + x_offset,
		                  self.free_y + y_offset,
		                  self)
		# Add the state to both heap and hash set
		heappush(available_states, (new_state.value, len(generated_states_set), new_state))
		generated_states_set.add(str(transformed_board.matrix))

	def generate_all_states(self, available_states, all_generated_states):
		# check needed, if not out of bounds
		if self.free_y - 1 >= 0:  # checking above
			self.generate_state(available_states, all_generated_states, y_offset=-1)

		if self.free_y + 1 < self.current_board.height:  # checking below
			self.generate_state(available_states, all_generated_states, y_offset=1)

		if self.free_x - 1 >= 0:  # checking left
			self.generate_state(available_states, all_generated_states, x_offset=-1)

		if self.free_x + 1 < self.current_board.width:  # checking right
			self.generate_state(available_states, all_generated_states, x_offset=1)



