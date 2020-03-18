from view.gui_init import *


def init_test(file_name):
	print(file_name)


if __name__ == '__main__':
	command = input()
	command = command.split()
	if command[0] == "gui":
		init_gui(width=3, height=3)
	if command[0] == "file":
		init_test(command[1])

