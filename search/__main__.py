import sys
import json

from search.util import print_move, print_boom, print_board


def boom(board_dict, start_p):
    """
    This function will find the board status after boom at the start stack position (x, y)

    Arguments:
    board_dict -- A dictionary with (x, y) tuples as keys (x, y in range(8))
        and printable objects (e.g. strings, numbers) as values. This function
        will arrange these printable values on the grid and output the result.
        Note: At most the first 3 characters will be printed from the string
        representation of each value.
    start_p -- A 2D position (x, y) means that the original starting point of boom.
    """
    delete_stack(board_dict, start_p)
    for stack in board_dict.keys():
        if check_in33(start_p, stack) and int(board_dict[stack][1:]) != 0:
            boom(board_dict, stack)


def delete_stack(board_dict, del_position):
    if del_position in board_dict.keys():
        board_dict[del_position] = board_dict[del_position][0] + "0"


def check_in33(stack_a, stack_b):
    """Check whether stack_b is near around stack_a. """
    if abs(stack_a[0]-stack_b[0]) <= 1 and abs(stack_a[1]-stack_b[1]) <= 1:
        return True
    return False


def check_black_exist(board_dict):
    """Check whether there is black color on the board."""
    for key in board_dict.keys():
        if board_dict[key][0] == "B":
            return True
    return False


def initial_board(data):
    """
    Initial the board dictionary from the json file 's format {"white":(n, x, y)} to
    the format {(x,y): "Wn"}
    """
    board_dict = {}
    for stack in data["white"]:
        board_dict[(stack[1], stack[2])] = "W" + str(stack[0])

    for stack in data["black"]:
        board_dict[(stack[1], stack[2])] = "B" + str(stack[0])

    return board_dict


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    board_dict = initial_board(data)
    print_board(board_dict)
    boom(board_dict, (1, 1))
    print_board(board_dict)

if __name__ == '__main__':
    main()
