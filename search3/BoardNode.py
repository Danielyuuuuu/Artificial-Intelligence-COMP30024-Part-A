import copy
from search.util import print_move, print_boom, print_board


class BoardNode:
    father_node = []  # only one father node!
    children_nodes = []  # many nodes

    current_board_dict = {}
    board_mark_dict = {}

    potential_behaviors = []
    history_behaviors = []

    def __init__(self, current_board_dict):
        self.current_board_dict = current_board_dict
        self.board_mark_dict = self.cal_mark()
        self.potential_behaviors = self.find_potential_behaviors()

    def refresh(self):

        if self.history_behaviors[-1][0] == "boom":
            self.board_mark_dict = self.cal_mark()
        else:
            self.board_mark_dict = self.father_node[0].board_mark_dict

        self.potential_behaviors = self.find_potential_behaviors()

    def stimulate_step(self):
        for behavior in self.potential_behaviors:
            tmp_node = self.stimulate_behavior(behavior)
            self.children_nodes.append(tmp_node)

    def get_color(self, position): return self.current_board_dict[position][0]

    def get_num(self, position): return int(self.current_board_dict[position][1:])

    def potential_ways(self, white_pos):
        """
        This function is to find all the valid moves for a current white position
        self.current_board_dict -- same as before
        white_pos -- the (x, y) form of the position need to be find.
        """
        num_white = self.get_num(white_pos)
        potential_aims = []

        # try each distance, and different divide way
        for distance in range(1, num_white + 1):
            for num_go in range(1, num_white + 1):

                right = (white_pos[0] + distance, white_pos[1])
                if right[0] <= 7:
                    if right not in self.current_board_dict:
                        potential_aims.append([right, num_go])
                    elif self.get_color(right) != "B":
                        potential_aims.append([right, num_go])

                left = (white_pos[0] - distance, white_pos[1])
                if left[0] >= 0:
                    if left not in self.current_board_dict:
                        potential_aims.append([left, num_go])
                    elif self.get_color(left) != "B":
                        potential_aims.append([left, num_go])

                up = (white_pos[0], white_pos[1] + distance)
                if up[1] <= 7:
                    if up not in self.current_board_dict:
                        potential_aims.append([up, num_go])
                    elif self.get_color(up) != "B":
                        potential_aims.append([up, num_go])

                down = (white_pos[0], white_pos[1] - distance)
                if down[1] >= 0:
                    if down not in self.current_board_dict:
                        potential_aims.append([down, num_go])
                    elif self.get_color(down) != "B":
                        potential_aims.append([down, num_go])

        return potential_aims

    def boom(self, start_p):
        """
        This function will find the board status after boom at the start stack position (x, y)

        Arguments:
        self.current_board_dict -- A dictionary with (x, y) tuples as keys (x, y in range(8))
            and printable objects (e.g. strings, numbers) as values. This function
            will arrange these printable values on the grid and output the result.
            Note: At most the first 3 characters will be printed from the string
            representation of each value.
        start_p -- A 2D position (x, y) means that the original starting point of boom.
        """
        if start_p in self.current_board_dict:
            del self.current_board_dict[start_p]
        for stack_position in list(self.current_board_dict.keys()):
            if BoardNode.check_in33(start_p, stack_position) and (stack_position in self.current_board_dict):
                self.boom(stack_position)

    def check_black_exist(self):
        """Check whether there is black color on the board."""
        for position in self.current_board_dict.keys():
            if self.get_color(position) == "B":
                return True
        return False

    def move_stack(self, initial_pos, final_pos, num_go):
        if final_pos not in self.current_board_dict:
            self.current_board_dict[final_pos] = "W0"

        num_aim = self.get_num(final_pos) + num_go
        num_init = self.get_num(initial_pos) - num_go

        self.current_board_dict[final_pos] = "W" + str(num_aim)
        if num_init == 0:
            self.current_board_dict.pop(initial_pos)
        else:
            self.current_board_dict[initial_pos] = "W" + str(num_init)

    def cal_mark(self):
        """
        Calculate the mark for each position on the board that can boom. For a position (1,1) has mark 2, meaning that
        if a white boom on (1,1), it will destroy 2 stacks of black.
        """
        mark_dict = {}
        black_node = copy.deepcopy(self)
        black_dict = black_node.current_board_dict

        for key in list(black_dict.keys()):
 
            if black_dict[key][0] == "W":
                del black_dict[key]
    
        for x in range(8):
            for y in range(8):
                tmp_board_node = copy.deepcopy(black_node)
              
            
                if (x, y) in black_dict.keys():             
                    continue
       
                tmp_board_node.boom((x, y))
           
                tmp_mark = BoardNode.compare_boom(black_node.current_board_dict, tmp_board_node.current_board_dict)
              
              
                if tmp_mark:
                    mark_dict[(x, y)] = tmp_mark
        print_board(mark_dict, "markDict")
        return mark_dict

    def find_potential_behaviors(self):

        # should have format [[behavior_type, original_position, potential_ways], ....]

        potential_behaviors = []
        for position in self.current_board_dict:
            if self.get_color(position) == "B":
                continue
            if position in self.board_mark_dict:
                potential_behaviors.append(["boom", position])
            for potential_way in self.potential_ways(position):
                if self.history_behaviors and \
                        self.history_behaviors[-1] == ["move", potential_way[0], position, potential_way[1]]:
                    continue
                potential_behaviors.append(["move", position, potential_way[0], potential_way[1]])
        return potential_behaviors

    def stimulate_behavior(self, behavior):
        tmp_node = copy.deepcopy(self)
        tmp_node.history_behaviors.append(behavior)
        tmp_node.father_node = self
        if behavior[0] == "boom":
            tmp_node.boom(behavior[1])
        else:
            tmp_node.move_stack(behavior[1], behavior[2], behavior[3])

        tmp_node.refresh()
        return tmp_node

    @staticmethod
    def check_in33(stack_a, stack_b):
        """Check whether stack_b is near around stack_b. """
        if abs(stack_a[0]-stack_b[0]) <= 1 and abs(stack_a[1]-stack_b[1]) <= 1:
            return True
        return False

    @staticmethod
    def compare_boom(board_dict, new_dict):
        """
        calculate how may black stacks was destroyed by comparing the original board.
        """
        return -(len(new_dict) - len(board_dict))


