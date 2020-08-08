from alghoritms import BruteForce, RandomSolver, SmartSolver
import time
# 0,001
#sample = "000004670009200801007613049050100284010000396496800050300061020085400060900078000"
# 70
sample = "000801000000000043500000000000070800000000100020030000600000075003400000000200600"
# 1,9
#sample = "850002400720000009004000000000107002305000900040000000000080070017000000000036040"
# 0,01
#sample = "080701030409000000050060418700009000800610500035000029060407090100008004020050073"
# 0,4
sample = "400500602000000000061007009000100063150000000807902000000400057500210000000003200"
# lb 0 b
#sample = "600079032000060500209008700906305001850000300473001250042680900000013427090200600"


class Board:
    """stores board state and methods"""
    board = None

    def __init__(self):
        """Data input for console version.
        Input format: left to right, line by line number sequence where 0 is empty cell"""

        # board_sequence = input("Insert board state (left to right, line by line in 1 line:\n")
        board_sequence = sample

        self.board = [int(char) for char in board_sequence]
        print(self.board)

    def draw(self):
        """Draw current state of board"""

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
        self.board = BruteForce.start(board=self.board)

    def less_brutal_solution(self):
        self.board = SmartSolver.create_markup(self.board)
    def random_solution(self):
        self.board = RandomSolver.randemonium(self.board)

    def smart_solution(self):
        """Implementation of James Crook alghoritm"""
        pass

if __name__ == "__main__":
    a = Board()
    a.draw()
    input("Press any key to start")
    start = time.time()
    #a.brutal_solution()
    #a.random_solution()
    a.less_brutal_solution()
    print(SmartSolver.markup)
    stop = time.time()
    a.draw()
    print(stop - start)
