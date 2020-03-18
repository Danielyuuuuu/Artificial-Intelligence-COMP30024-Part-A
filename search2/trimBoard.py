import copy


# To trim the four sides of the board that do not have any stack
def trim_board(board_dict):

    trimmed_board = {}

    # Trim top left of the board
    continue_to_trim = True
    for y in range(7, 3, -1):

        if not continue_to_trim:
            break

        for x in range(4):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimmed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                continue_to_trim = False
                break
    
    # Trim top right of the board
    continue_to_trim = True
    for y in range(7, 3, -1):

        if not continue_to_trim:
            break
        
        for x in range(7, 3, -1):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimmed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                continue_to_trim = False
                break

    # Trim bottom left of the board
    continue_to_trim = True
    for y in range(4):

        if not continue_to_trim:
            break

        for x in range(4):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimmed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                continue_to_trim = False
                break

    # Trim bottom right of the 
    continue_to_trim = True
    for y in range(4):

        if not continue_to_trim:
            break

        for x in range(7, 3, -1):
            if (x, y) not in board_dict:
                if not check_any_stack_arround(board_dict, (x, y)):
                    trimmed_board[(x, y)] = 'X0'
                    
                else:
                    break
            else:
                continue_to_trim = False
                break


    # Trim the four borders of the board
    for x in range(8):
        for y in range(8):
            if (x, y) not in board_dict:
                if x in [0, 7] or y in [0, 7]:
                    if not check_any_stack_arround(board_dict, (x, y)):
                        trimmed_board[(x, y)] = 'X0'
                else:
                    continue


    trimmed_board = delete_trim_if_it_make_the_board_disconnected(trimmed_board)
    
    
    return trimmed_board


""" 
To make sure that the trimmed board is not disconnected, and does not
trap any stacks in the corner
"""
def delete_trim_if_it_make_the_board_disconnected(trimmed_board):

    rows_that_have_been_cut_entirely = []
    # Check from bottom up
    for y in range(8):
        row_has_been_cut_entirely = True
        for x in range(8):
            if (((x, y) in trimmed_board) and trimmed_board[(x, y)] != 'X0') or (x, y) not in trimmed_board:
                row_has_been_cut_entirely = False
                break
        if row_has_been_cut_entirely:
            rows_that_have_been_cut_entirely.append(y)


    columns_that_have_been_cut_entirely = []

    # Check from left to right
    for x in range(8):
        column_has_been_cut_entirely = True
        for y in range(8):
            if (((x, y) in trimmed_board) and trimmed_board[(x, y)] != 'X0') or (x, y) not in trimmed_board:
                column_has_been_cut_entirely = False
                break
        if column_has_been_cut_entirely:
            columns_that_have_been_cut_entirely.append(x)

    
    rows_that_have_been_cut_entirely = lines_that_separate_the_board(rows_that_have_been_cut_entirely)
    columns_that_have_been_cut_entirely = lines_that_separate_the_board(columns_that_have_been_cut_entirely)
    
    
    # Delete the trimmed position that has disconnected the board
    if len(rows_that_have_been_cut_entirely) != 0:
        line = find_line_that_has_the_least_trimmed_positions(trimmed_board, True)
        for y in range(8):
            if ((line, y) in trimmed_board) and trimmed_board[(line, y)] == 'X0':
                del trimmed_board[(line, y)]

    if len(columns_that_have_been_cut_entirely) != 0:
        line = find_line_that_has_the_least_trimmed_positions(trimmed_board, False)
        for x in range(8):
            if ((x, line) in trimmed_board) and trimmed_board[(x, line)] == 'X0':
                del trimmed_board[(x, line)]

    
    for x in range(7):
        for y in range(7):
            pos_down_left = (x, y)
            pos_down_right = (x + 1, y)
            pos_up_left = (x, y + 1)
            pos_up_right = (x + 1, y + 1)

            if pos_down_left in trimmed_board and pos_up_right in trimmed_board:
                if trimmed_board[pos_down_left] == "X0" and trimmed_board[pos_up_right] == "X0":
                    if pos_down_right not in trimmed_board and pos_up_left not in trimmed_board:
                        del trimmed_board[pos_down_left]
                        del trimmed_board[pos_up_right]
            
            elif pos_down_right in trimmed_board and pos_up_left in trimmed_board:
                if trimmed_board[pos_down_right] == "X0" and trimmed_board[pos_up_left] == "X0":
                    if pos_down_left not in trimmed_board and pos_up_right not in trimmed_board:
                        del trimmed_board[pos_down_right]
                        del trimmed_board[pos_up_left]


    return trimmed_board


# Find the row or colomn that has disconnected the board
def lines_that_separate_the_board(lines_that_have_been_cut_entirely):
    if len(lines_that_have_been_cut_entirely) != 0:
        for i in range(8):
            if i in lines_that_have_been_cut_entirely:
                lines_that_have_been_cut_entirely.remove(i)
            else:
                break
        for i in range(7, -1, -1):
            if i in lines_that_have_been_cut_entirely:
                lines_that_have_been_cut_entirely.remove(i)
            else:
                break
    return lines_that_have_been_cut_entirely


# Fine the row or column that has the least trimmed positions
def find_line_that_has_the_least_trimmed_positions(trimmed_board, is_column):
    
    line_number = None
    min_number_of_trimmed_positions = 9
    if is_column:
        for x in range(8):
            current_number_of_trimmed_positions = 0
            breaked = False
            for y in range(8):

                #!!!!!!!!!!!!!
                if y in [0, 7] and (x, y) in trimmed_board and trimmed_board[(x, y)] == 'X0':
                
                    breaked = True
                    break
                elif (x, y) in trimmed_board and trimmed_board[(x, y)] == 'X0':
                    current_number_of_trimmed_positions += 1
            if current_number_of_trimmed_positions < min_number_of_trimmed_positions and not breaked:
                line_number = x
                min_number_of_trimmed_positions = current_number_of_trimmed_positions
                
        
    else:
        for y in range(8):
            current_number_of_trimmed_positions = 0
            breaked = False
            for x in range(8):

                #!!!!!!!!!!!!!!
                if x in [0, 7] and (x, y) in trimmed_board and trimmed_board[(x, y)] == 'X0':
                    breaked = True
                    break

                elif (x, y) in trimmed_board and trimmed_board[(x, y)] == 'X0':
                    current_number_of_trimmed_positions += 1

            if current_number_of_trimmed_positions < min_number_of_trimmed_positions and not breaked:
                line_number = x
                min_number_of_trimmed_positions = current_number_of_trimmed_positions
        
    return line_number   


# Check if there is any stack around the potential trimming position
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
    down_left = (current_pos[0] - 1, current_pos[1] - 1)
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


# Check if there is any stack in a given position
def check_position_has_stack(board_dict, position, check_white_stack):
    if 0 <= position[0] < 8 and 0 <= position[1] < 8:
        if check_white_stack:
            if position in board_dict:
                if board_dict[position][0] == 'W':
                    return True
        else:
            if position in board_dict:
                return True
    return False