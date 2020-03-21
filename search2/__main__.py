import sys
import json
import copy
import time
from search2.trimBoard import  trim_board
from search.util import print_move, print_boom, print_board

trim_board_dict = {}
mark_dict = {}
history_board_list = []
highest_mark_positions = {}


class BoardNode:
    current_board_dict = {}
    mark_dict = {}
    history_behaviors = []
    potential_behaviors = []
    next_nodes = []

    def __init__(self, board_dict, history, behavior):
        self.current_board_dict = board_dict

        if not history:
            self.history_behaviors += [behavior]
        else:
            self.history_behaviors = copy.copy(history)
            self.history_behaviors.append(behavior)
        self.potential_behaviors = find_potential_behaviors(board_dict, self.history_behaviors)

    def stimulate_step(self):

        self.next_nodes = []
        global history_board_list

        for behavior in self.potential_behaviors:
            tmp_board_dict = stimulate_behavior(self.current_board_dict, behavior)
            if tmp_board_dict in history_board_list:
                continue
            history_board_list.append(tmp_board_dict)

            tmp_node = BoardNode(tmp_board_dict,
                                 self.history_behaviors, behavior)
            self.next_nodes.append(tmp_node)


def check_direction(board_dict, behavior):
    for position in board_dict:
        if board_dict[position][0] == "B":
            if square_distance(position, behavior[1]) - square_distance(position, behavior[2]) > 0:

                return True
    return False


def square_distance(p1, p2):
    return (p1[0]-p2[0])**2 - (p1[1]-p2[1])**2


def find_potential_behaviors(board_dict, history_behaviors):

    # should have format [[behavior_type, original_position, potential_ways], ....]
    potential_behaviors = []
    global mark_dict
    global trim_board_dict

    for position in board_dict:
        if board_dict[position][0] == "B":
            continue
        if position in mark_dict:
            potential_behaviors.append(["boom", position])

        for potential_way in potential_ways(board_dict, position):
            #print(position, potential_way)
            if history_behaviors and \
                    history_behaviors[-1] == ["move", potential_way[0], position, potential_way[1]]:
                continue
            if potential_way[0] in trim_board_dict:
                # print("potential_way[0]", potential_way[0])
                # print("potential_way[0]", trim_board_dict[potential_way[0]])
                # print("was remove! potential behaviors:", position, potential_way)
                continue
            potential_behaviors.append(["move", position, potential_way[0], potential_way[1]])

    return potential_behaviors


def stimulate_behavior(board_dict, behavior):
    new_board_dict = copy.copy(board_dict)
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
    global mark_dict
    mark_dict = {}

    black_dict = copy.copy(board_dict)

    for key in list(black_dict.keys()):
        if black_dict[key][0] == "W":
            del black_dict[key]

    for x in range(8):
        for y in range(8):
            if (x, y) in black_dict:
                continue

            tmp_board = copy.copy(black_dict)
            boom(tmp_board, (x, y))
            tmp_mark = compare_boom(black_dict, tmp_board)
            if tmp_mark:
                mark_dict[(x, y)] = tmp_mark

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


def get_highest_mark_positions():
    global mark_dict
    global highest_mark_positions

    highest_mark_positions = {}
    max_num = 0
    for position in mark_dict:
        if mark_dict[position] >= max_num:
            max_num = mark_dict[position]
    for position in mark_dict:
        if mark_dict[position] == max_num:
            highest_mark_positions[position] = max_num
    return highest_mark_positions


def accidental_injury(board_dict, behavior):
    global mark_dict
    total_stack = len(board_dict)
    total_stack_after = len(stimulate_behavior(board_dict, behavior))
    # print("\n\n\n\ntotal stack", total_stack)
    # print("after", total_stack_after)
    # print("mark dict", mark_dict[behavior[1]])
    if int(board_dict[behavior[1]][1]) == 1:
        if total_stack - total_stack_after == mark_dict[behavior[1]] + 1:
            return False

    return True


def BFS(board_tree):

    node_list = [board_tree]
    global highest_mark_positions
    global mark_dict
    global trim_board_dict
    # history_dict = []

    for turn in range(240):
        node_list_next = []
        # print("\n\n\n\n\n\n\nTurns:  ", turn, "        length of checking list:  ", len(node_list))
        for node_list_index in range(0, len(node_list)):
            tmp_node = node_list[node_list_index]
            if not check_black_exist(tmp_node.current_board_dict):
                return tmp_node.history_behaviors

            # if tmp_node.current_board_dict in history_dict:
            #     continue
            # print("Turns: ",turn)
            # print(node_list_index)

            # print(len(node_list))

            node_list_next.append(tmp_node)
            # history_dict.append(tmp_node.current_board_dict)

        node_list = []
        break_value = False
        for node_index in range(0, len(node_list_next)):
            # print_board(node_list_next[node_index].current_board_dict)
            # time_start = time.time()

            for behavior in node_list_next[node_index].potential_behaviors:
                if behavior[0] == "boom" and behavior[1] in highest_mark_positions:
                    if not accidental_injury(node_list_next[node_index].current_board_dict, behavior):

                        # print_board(node_list_next[node_index].current_board_dict)
                        # print(behavior)
                        node_list_next[node_index].potential_behaviors = [behavior]
                        break_value = True
                        node_list = []
                        break

            node_list_next[node_index].stimulate_step()
            # print("potential_behaviors: ", node_list_next[node_index].potential_behaviors)
            # time_end = time.time()
            # print('stimulate_step time cost', time_end - time_start, 's')
            stimulate_node = node_list_next[node_index].next_nodes
            node_list += stimulate_node
            if break_value:
                trim_board_dict = trim_board(node_list[0].current_board_dict)
                # print_board(trim_board_dict)
                mark_dict = cal_mark(node_list[0].current_board_dict)
                highest_mark_positions = get_highest_mark_positions()
                break


def print_history_behaviors(history_behaviors_list):
    for behavior in history_behaviors_list:
        if behavior:
            if behavior[0] == "boom":
                print_boom(behavior[1][0], behavior[1][1])
            else:
                print_move(behavior[3], behavior[1][0], behavior[1][1], behavior[2][0], behavior[2][1])


def main(file_path):

    # with open(sys.argv[1]) as file:
    #     data = json.load(file)
    with open(file_path) as file:
        data = json.load(file)
    print("Test case path:     ", file_path)

    # TODO: find and print winning action sequence
    global mark_dict
    global trim_board_dict
    global history_board_list
    global highest_mark_positions

    mark_dict = {}
    trim_board_dict = {}
    history_board_list = []
    highest_mark_positions = {}

    time_start = time.time()
    board_dict = initial_board(data)
    print_board(board_dict)
    mark_dict = cal_mark(board_dict)

    trim_board_dict = trim_board(board_dict)

    # print_board(board_dict, "initial")
    # print_board(mark_dict, "initial_mark")
    # print_board(trim_board_dict, "initial_trim")
    get_highest_mark_positions()

    board_tree = BoardNode(board_dict, [], [])

    history = BFS(board_tree)
    time_end = time.time()
    print('Search time cost', time_end - time_start, 's')
    print_history_behaviors(history)
    print("")
    return history


if __name__ == '__main__':

    main("2020-part-a-test-cases/test-level-1.json")
    main("2020-part-a-test-cases/test-level-2.json")
    main("2020-part-a-test-cases/test-level-3.json")
    main("2020-part-a-test-cases/test-level-4.json")
    main("2020-part-a-test-cases/test-level-5.json")
    main("2020-part-a-test-cases/test-level-6.json")
    main("2020-part-a-test-cases/test-level-7.json")
    main("2020-part-a-test-cases/test-level-8.json")
    main("2020-part-a-test-cases/test-level-9.json")
    main("2020-part-a-test-cases/test-level-10.json")
    main("2020-part-a-test-cases/test-level-11.json")


