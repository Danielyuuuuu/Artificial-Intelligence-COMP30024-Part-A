COMP30024 Report

Formulate the game as a search problem:

* States: The state is the position of the white and black stacks in the board.

* Actions: White stacks can be moved in one of the four cardinal directions, or initiate a boom action.

* Goal tests: Check if there are any black stacks left in the board. If all the black stacks have been removed from the board, the game ends.

* Path costs: 1 per stack move.

What search algorithm did we use?
We have formulated the game as a BFS problem. This is to find all the possible movements of the white stacks, and check if any of the possible movements lead to zero black stacks on the board.

Why did we choose this algorithm?
The BFS algorithm is complete, this means that we will be able to find a solution even for a tricky test case. 
It can find the shortest path to win the game.
It is also very easy to implement.

Heuristics?
The BFS algorithm will run for a long time if the depth and the branching factor of the problem are high. So, we have implemented the 'trim_board' function to delete all the board positions that do not lead to the desired outcome. This has reduced the branching factor by a huge amount, thus increasing the speed of the BFS algorithm.

What features of the problem and your program’s input impact your program’s time and space requirements?
If the black stacks are located sparsely on the board and there are only certain locations for the white stack to boom a group of black stacks to win, then it is going to take some time to run the algorithm. This is because the 'trim_board' won't be as effective when trimming a board with stacks sparsely located around the board, as it would be too risky to delete too much board positions, and ending up isolating some of the stacks. This leads to a big branching factor and makes the BFS algorithm to run lots of executions as well as an increase in space complexity.
