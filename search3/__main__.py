import sys
import json

from search.util import print_move, print_boom, print_board
from search3.BoardNode import *


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

    # print_board(mark_dict)
    print_board(board_dict, "initial")

    board_tree = BoardNode(board_dict)
    print_board(board_tree.current_board_dict)


if __name__ == '__main__':
    main()
