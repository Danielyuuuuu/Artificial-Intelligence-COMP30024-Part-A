import sys
import json
import copy
from search.util import print_move, print_boom, print_board


class BoardNode:
    current_board_dict = {}
    history_board_list = []
    potential_behaviors = []
    next_nodes = []

    def __init__(self, board_dict, history):
        self.current_board_dict = board_dict
        self.potential_behaviors = find_potential_behaviors(board_dict)
        if not history:
            self.history_board_list.append(board_dict)
        else:
            self.history_board_list = copy.deepcopy(history)
            self.history_board_list.append(board_dict)

    def stimulate_step(self):
        for behavior in self.potential_behaviors:
            tmp_node = BoardNode(stimulate_behavior(self.current_board_dict, behavior), self.history_board_list)
            self.next_nodes.append(tmp_node)


def find_potential_behaviors(board_dict):

    # should have format [[behavior_type, original_position, potential_ways], ....]
    potential_behaviors = []
    for position in board_dict:
        if board_dict[position][0] == "B":
            continue
        potential_behaviors.append(["boom", position])
        for potential_way in potential_ways(board_dict, position):
            potential_behaviors.append(["move", position, potential_way[0], potential_way[1]])
    return potential_behaviors


def stimulate_behavior(board_dict, behavior):
    new_board_dict = copy.deepcopy(board_dict)
    if behavior[0] == "boom":
        boom(new_board_dict, behavior[1])
    else:
        move_stack(new_board_dict, behavior[1], behavior[2], behavior[3])
    return new_board_dict


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
    if start_p in board_dict:
        del board_dict[start_p]
    for stack in list(board_dict.keys()):
        if check_in33(start_p, stack) and (stack in board_dict):
            boom(board_dict, stack)


def potential_ways(board_dict, white_pos):
    """
    This function is to find all the valid moves for a current white position
    board_dict -- same as before
    white_pos -- the (x, y) form of the position need to be find.
    """
    num_white = int(board_dict[white_pos][1:])
    potential_aims = []

    # try each distance, and different divide way
    for distance in range(1, num_white + 1):
        for num_go in range(1, num_white + 1):
            right = (white_pos[0] + distance, white_pos[1])
            left = (white_pos[0] - distance, white_pos[1])
            up = (white_pos[0], white_pos[1] + distance)
            down = (white_pos[0], white_pos[1] - distance)

            if right[0] <= 7:
                if right not in board_dict:
                    potential_aims.append([right, num_go])
                elif board_dict[right][0] != "B":
                    potential_aims.append([right, num_go])
            if left[0] >= 0:
                if left not in board_dict:
                    potential_aims.append([left, num_go])
                elif board_dict[left][0] != "B":
                    potential_aims.append([left, num_go])
            if up[1] <= 7:
                if up not in board_dict:
                    potential_aims.append([up, num_go])
                elif board_dict[up][0] != "B":
                    potential_aims.append([up, num_go])
            if down[1] >= 0:
                if down not in board_dict:
                    potential_aims.append([down, num_go])
                elif board_dict[down][0] != "B":
                    potential_aims.append([down, num_go])

    return potential_aims


def cal_mark(board_dict):
    """
    Calculate the mark for each position on the board that can boom. For a position (1,1) has mark 2, meaning that
    if a white boom on (1,1), it will destroy 2 stacks of black.
    """
    mark_dict = {}
    black_dict = copy.deepcopy(board_dict)

    for key in list(black_dict.keys()):
        if black_dict[key][0] == "W":
            del black_dict[key]

    for x in range(8):
        for y in range(8):
            if (x, y) in black_dict:
                mark_dict[(x, y)]= 0
                continue
            tmp_board = copy.deepcopy(black_dict)
            boom(tmp_board, (x, y))
            mark_dict[(x, y)] = compare_boom(black_dict, tmp_board)
    return mark_dict


def compare_boom(board_dict, new_dict):
    """
    calculate how may black stacks was destroyed by comparing the original board.
    """
    number_b_original = 0
    number_new = 0
    for position in board_dict.keys():
        if board_dict[position][0] == "B":
            number_b_original += 1
    for position in new_dict.keys():
        if board_dict[position][0] == "B":
            number_new += 1
    return number_b_original - number_new


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


def move_stack(board_dict, initial_pos, final_pos, num_go):
    if final_pos not in board_dict:
        board_dict[final_pos] = "W0"

    num_aim = int(board_dict[final_pos][1:]) + num_go
    num_init = int(board_dict[initial_pos][1:]) - num_go

    board_dict[final_pos] = "W" + str(num_aim)
    if num_init == 0:
        board_dict.pop(initial_pos)
    else:
        board_dict[initial_pos] = "W" + str(num_init)


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    board_dict = initial_board(data)
    mark_dict = cal_mark(board_dict)

    # print_board(mark_dict)
    print_board(board_dict, "initial")

    board_tree = BoardNode(board_dict, [])
    print_board(board_tree.current_board_dict)
    node_list = [board_tree]

    history_dict = []

    a = 0
    for turn in range(240):
        node_list_next = []

        for node_list_index in range(0, len(node_list)):
            tmp_node = node_list[node_list_index]
            if not check_black_exist(tmp_node.current_board_dict):
                print("win!!!!!!!!!")
                print_board(tmp_node.history_board_list[-2])
                return "Win!!!!!!!!!!!!!!!!!"
            if tmp_node.current_board_dict in history_dict:
                continue
            print("Turns: ",turn)
            print(node_list_index)
            a += 1
            print("a :",a)
            print(len(node_list))

            node_list_next.append(tmp_node)
            history_dict.append(tmp_node.current_board_dict)

        node_list = []
        for node_index in range(0, len(node_list_next)):
            node_list_next[node_index].stimulate_step()
            stimulate_node = node_list_next[node_index].next_nodes
            node_list += stimulate_node


if __name__ == '__main__':
    main()
