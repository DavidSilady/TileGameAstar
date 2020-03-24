from view.gui_init import *

# File format:
# 3 3
# 0 1 2
# 3 4 5
# 6 7 8
#
# 8 6 7
# 2 5 4
# 3 0 1


def init_file(file_name):
	file = open(file_name, "r")
	primary_board, secondary_board, width, height = read_file_setup(file)
	init_gui(primary_board, secondary_board, width=width, height=height)


def read_file_setup(file):
	dimensions = file.readline().split()
	dimensions = [int(i) for i in dimensions]  # [0] width [1] height
	width = dimensions[0]
	height = dimensions[1]
	primary_matrix = read_file_matrix(file, width, height)
	secondary_matrix = read_file_matrix(file, width, height)
	primary_board = Board(width, height, primary_matrix)
	secondary_board = Board(width, height, secondary_matrix)
	return primary_board, secondary_board, width, height


def read_file_matrix(file, width, height):
	matrix = [[0 for x in range(width)] for y in range(height)]
	for y in range(height):
		row = file.readline().split()
		row = [int(i) for i in row]
		matrix[y] = row
	file.readline()  # Separating line
	print(matrix)
	return matrix


def init_test(file_name):
	file = open(file_name, "r")
	num_games = int(file.readline())
	total_time = 0
	total_states = 0
	for i in range(num_games):
		primary_board, secondary_board, width, height = read_file_setup(file)
		a_star = AStar(primary_board, secondary_board, 200000)
		start = time.time()
		solution = a_star.find_solution()
		end = time.time()
		print("Generated states: ", len(a_star.all_generated_states))
		print("Time elapsed: ", end - start)
		total_time += end - start
		total_states += len(a_star.all_generated_states)
	print("Total time elapsed: ", total_time)
	print("Total generated states: ", total_states - 181440)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		command = input()
		command = command.split()
	else:
		command = sys.argv[1:]
	print(command)
	if command[0] == "gui":
		init_gui(width=3, height=3)
	if command[0] == "file":
		if len(command) == 1:
			init_file(input())
		init_file(command[1])
	if command[0] == "test":
		if len(command) == 1:
			init_test(input())
		init_test(command[1])


