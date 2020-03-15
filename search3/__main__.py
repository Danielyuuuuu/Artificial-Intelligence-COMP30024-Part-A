import sys
import json
import time
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


def BFS(board_tree):

    checking_list = [board_tree]
    history =[]
    for num_turn in range(240):
        # print("Turns：   ", num_turn)
        next_checking_list = []
        print("length of checking list:", len(checking_list))
        for check_node in checking_list:
            if check_node.current_board_dict in history:
                continue

            # print_board(check_node.current_board_dict)
            if check_node.check_win():
                return check_node.history_behaviors

            history.append(check_node.current_board_dict)

            next_checking_list.append(check_node)

        checking_list = []
        for next_check_node in next_checking_list:
            next_check_node.stimulate_step()
            checking_list += next_check_node.children_nodes


    return None


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    board_dict = initial_board(data)

    # print_board(mark_dict)
    print_board(board_dict, "initial")

    board_tree = BoardNode(board_dict)

    time_start = time.time()

    print(BFS(board_tree))
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    return None
    # print_board(board_tree.board_mark_dict)
    # print("potential_behaviors:", board_tree.potential_behaviors)
    # print(board_tree.history_behaviors)
    #
    # board_tree.stimulate_step()
    #
    # print_board(board_tree.children_nodes[1].current_board_dict, "next")
    # print("historyBehaviors", board_tree.children_nodes[1].history_behaviors)
    # print("historyBehaviors", board_tree.children_nodes[1].potential_behaviors)
    # board_tree.children_nodes[1].stimulate_step()
    # print(board_tree.children_nodes[1].children_nodes)
    # print_board(board_tree.children_nodes[1].children_nodes[0].current_board_dict, "nextnext")
    # print(board_tree.children_nodes[1].children_nodes[0].history_behaviors, "nextnext")
    # print_board(board_tree.children_nodes[1].children_nodes[0].board_mark_dict, "nextnext")


if __name__ == '__main__':
    main()
