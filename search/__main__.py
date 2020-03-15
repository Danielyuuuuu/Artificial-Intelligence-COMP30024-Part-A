import sys
import json
import copy
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
    if start_p in board_dict:
        del board_dict[start_p]
    for stack in list(board_dict.keys()):
        if check_in33(start_p, stack) and (stack in board_dict):
            boom(board_dict, stack)


def potential_way(board_dict, white_pos):
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


def move_stack(board_dict, initial_pos, final_pos):
    board_dict[final_pos] = board_dict[initial_pos]
    board_dict.pop(initial_pos)


def dijsktra(original_board_dict, initial_pos, final_pos):

    paths_dict = {initial_pos: (initial_pos, 0)}
    current_pos = initial_pos
    visited_pos = set()

    board_dict = copy.deepcopy(original_board_dict)
    num_of_stack = original_board_dict[initial_pos]
    board_dict.pop(initial_pos)

    # Keeps iterating until it reaches the final position
    while current_pos != final_pos:
        board_dict[current_pos] = num_of_stack
        visited_pos.add(current_pos)

        potential_moves = potential_way(board_dict, current_pos)
        
        if len(potential_moves) != 0:
            # Try all the potential moves and check which one has the least cost
            for potential_move in potential_moves:
                potential_move = potential_move[0]
                cost = distance_between_positions(current_pos, potential_move) + paths_dict[current_pos][1]

                if potential_move not in paths_dict:
                    paths_dict[potential_move] = (current_pos, cost)
                else:
                    if paths_dict[potential_move][1] > cost:
                        paths_dict[potential_move] = (current_pos, cost)
        
        
        # To find a position with the least cost
        min_cost = float('inf')
        min_position = None
        for position in paths_dict:
            if position != paths_dict[position][0] and position not in visited_pos:
                if paths_dict[position][1] < min_cost:
                    min_cost = paths_dict[position][1]
                    min_position = position

        # Check of there is any unexplored position
        if min_position is None:
            print("Stack can't be moved to the destination")
            return
        else:
            current_pos = min_position


    shortest_path = []

    # Back tracking the shortest path
    while current_pos is not initial_pos:
        shortest_path.append(current_pos)
        previous_pos = paths_dict[current_pos][0]
        current_pos = previous_pos
    shortest_path.append(initial_pos)
    print(shortest_path[::-1])


def distance_between_positions(position_one, position_two):
    return abs(position_one[0] - position_two[0]) + abs(position_one[1] - position_two[1])


def trim_board(board_dict):

    trimed_board = copy.deepcopy(board_dict)

    # Trim top left of the board
    for y in range(7, -1, -1):
        for x in range(8):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                break
    
    # Trim top right of the board
    for y in range(7, -1, -1):
        for x in range(7, -1, -1):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                break

    # Trim bottom left of the board
    for y in range(8):
        for x in range(8):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                break

    # Trim bottom right of the board
    for y in range(8):
        for x in range(7, -1, -1):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                break
    return trimed_board
        

def check_if_board_are_disconnected(trimed_board):

    rows_that_have_been_cut_entirely = []
    # Check from bottom up
    for y in range(8):
        row_has_been_cut_entirely = True
        for x in range(8):
            if (((x, y) in trimed_board) and trimed_board[(x, y)] != 'X0') or (x, y) not in trimed_board:
                row_has_been_cut_entirely = False
                break
        if row_has_been_cut_entirely:
            rows_that_have_been_cut_entirely.append(y)


    columns_that_have_been_cut_entirely = []

    # Check from left to right
    for x in range(8):
        column_has_been_cut_entirely = True
        for y in range(8):
            if (((x, y) in trimed_board) and trimed_board[(x, y)] != 'X0') or (x, y) not in trimed_board:
                column_has_been_cut_entirely = False
                break
        if column_has_been_cut_entirely:
            columns_that_have_been_cut_entirely.append(y)
    
    print(rows_that_have_been_cut_entirely)  
    print(columns_that_have_been_cut_entirely) 

def check_any_stack_arround(board_dict, current_pos):
    right = (current_pos[0] + 1, current_pos[1])
    left = (current_pos[0] - 1, current_pos[1])
    up = (current_pos[0], current_pos[1] + 1)
    down = (current_pos[0], current_pos[1] - 1)
    right_right = (current_pos[0] + 2, current_pos[1])
    left_left = (current_pos[0] - 2, current_pos[1])
    up_up = (current_pos[0], current_pos[1] + 2)
    down_down = (current_pos[0], current_pos[1] - 2)
    up_left = (current_pos[0] - 1, current_pos[1] + 1)
    up_right = (current_pos[0] + 1, current_pos[1] + 1)
    down_left = (current_pos[0] -1, current_pos[1] - 1)
    down_right = (current_pos[0] + 1, current_pos[1] - 1)

    if check_position_has_stack(board_dict, right, False):
        return True
    elif check_position_has_stack(board_dict, left, False):
        return True
    elif check_position_has_stack(board_dict, up, False):
        return True
    elif check_position_has_stack(board_dict, down, False):
        return True
    elif check_position_has_stack(board_dict, right_right, True):
        return True
    elif check_position_has_stack(board_dict, left_left, True):
        return True
    elif check_position_has_stack(board_dict, up_up, True):
        return True
    elif check_position_has_stack(board_dict, down_down, True):
        return True
    elif check_position_has_stack(board_dict, up_left, False):
        return True
    elif check_position_has_stack(board_dict, up_right, False):
        return True
    elif check_position_has_stack(board_dict, down_left, False):
        return True
    elif check_position_has_stack(board_dict, down_right, False):
        return True
    return False


def check_position_has_stack(board_dict, position, check_white_stack):
    if (0 <= position[0] < 8 and 0 <=  position[1] < 8):
        if check_white_stack:
            if position in board_dict:
                if board_dict[position][0] == 'W':
                    return True
        else: 
            if position in board_dict:
                return True
    return False    


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    board_dict = initial_board(data)
    mark_dict = cal_mark(board_dict)

    print_board(mark_dict)
    print_board(board_dict)
    #print(potential_way(board_dict, (1, 0)))


    dijsktra(board_dict, (1, 0), (3, 3))

    trimed_board = trim_board(board_dict)
    print_board(trimed_board)

    check_if_board_are_disconnected(trimed_board)

if __name__ == '__main__':
    main()

