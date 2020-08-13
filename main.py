from algorithms import BruteForce, SmartSolver
import time
# 0,001
#sample = "000004670009200801007613049050100284010000396496800050300061020085400060900078000"
# 63
sample = "000801000000000043500000000000070800000000100020030000600000075003400000000200600"
# 1,9
#sample = "850002400720000009004000000000107002305000900040000000000080070017000000000036040"
# 0,01
#sample = "080701030409000000050060418700009000800610500035000029060407090100008004020050073"
# 0,4
#sample = "400500602000000000061007009000100063150000000807902000000400057500210000000003200"
# lb 0 b 371
#sample = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"

class Board:
    """stores board state and methods
    board: (list) Representation of the board. List of 81 ints, one for each cell, starting in left top corner then
    going right in row and go to next row. 0 = empty cell """
    board = None

    def __init__(self, board_sequence):
        """Data input for console version.
        Input format: left to right, line by line number sequence where 0 is empty cell
        transform input string into list of ints"""

        self.board = [int(char) for char in board_sequence]

    def draw(self):
        """Draw current state of board in human-friendly form"""

        index = 0
        print("-" * 25)
        for _ in range(3):
            for _ in range(3):
                print("| ", end="")
                for _ in range(3):
                    for i in range(3):
                        if self.board[index] != 0:
                            print(self.board[index], end=" ")
                        else:
                            print(" ", end=" ")
                        index += 1
                    print("| ", end="")
                print()
            print("-" * 25)

    def brutal_solution(self):
        """Bruteforce with backtracking. Check every state of board until find correct one"""
        self.board = BruteForce.start(self.board)

    def less_brutal_solution(self):
        """Fill part of the board (or whole in easier puzzles) using James Crook Occupancy theorem and fill rest using
        bruteforce"""
        self.board = SmartSolver.start(self.board)

    def smart_solution(self):
        """Implementation of James Crook algorithm. TBD later"""
        pass


def start_here():
    """Start program"""
    # input from console or sample for testing
    # board_sequence = input("Insert board state (left to right, line by line in 1 line:\n")
    board_sequence = sample

    # initiation of Board instance and draw initial state
    board = Board(board_sequence)
    board.draw()

    # show menu and select algorithm
    while True:
        x = input("1. Brutal solution\n2. Less brutal solution\nChoose solution: ")

        if x != "1" and x != "2":
            print("unknown command. Try again\n")
        else:
            break

    #input("Press any key to start")
    print("Working...")

    if x == "1":
        start = time.time()
        board.brutal_solution()
    elif x == "2":
        start = time.time()
        board.less_brutal_solution()


    stop = time.time()
    board.draw()
    print(f"complete in {stop - start} sec")


if __name__ == "__main__":
    start_here()

