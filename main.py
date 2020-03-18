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


def init_test(file_name):
	file = open(file_name, "r")
	dimensions = file.readline().split()
	dimensions = [int(i) for i in dimensions]  # [0] width [1] height
	width = dimensions[0]
	height = dimensions[1]
	primary_matrix = read_file_matrix(file, width, height)
	secondary_matrix = read_file_matrix(file, width, height)
	primary_board = Board(height, width, primary_matrix)
	secondary_board = Board(height, width, secondary_matrix)
	init_gui(primary_board, secondary_board, width=width, height=height)


def read_file_matrix(file, width, height):
	matrix = [[0 for x in range(width)] for y in range(height)]
	print(matrix)
	for y in range(height):
		row = file.readline().split()
		row = [int(i) for i in row]
		matrix[y] = row
	print(matrix[0][1])
	file.readline()  # Separating line
	return matrix


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
			init_test(input())
		init_test(command[1])

