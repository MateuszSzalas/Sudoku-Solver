from algorithms import BruteForce, SmartSolver
import time


# Examples
# Easy
# sample = "000004670009200801007613049050100284010000396496800050300061020085400060900078000"
# Hard. Slowly solved by bruteforce but fast by smarter alghorithm
sample = "000801000000000043500000000000070800000000100020030000600000075003400000000200600"
# Hard, designed against bruteforce. Very slow solution using bruteforce but fast solved using smarter algorithm
# sample = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"


class Board:
    """stores board state and methods
    board: (list) Representation of the board. List of 81 ints, one for each cell, starting in left top corner then
    going right in row and go to next row. 0 = empty cell """
    board = None

    def __init__(self, board_sequence):
        """Transformation of input string into list of int"""

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
        solver = BruteForce(self.board)
        solver.start()
        self.board = solver.board

    def less_brutal_solution(self):
        """Fill part of the board (or whole in easier puzzles) using James Crook Occupancy theorem and fill rest using
        bruteforce"""
        solver = SmartSolver(self.board)
        solver.start()
        self.board = solver.board

    def smart_solution(self):
        """Implementation of James Crook algorithm. TBD later"""
        pass


def input_from_console():
    """Takes input from user using console and check if it is correct. Return board squence (string)."""
    board_sequence = ""
    line_counter = 1
    print("Insert board state (from left to right, 'Enter' after every line)\nif cell is empty type '0'")
    while True:
        line = input(f"line {line_counter}: ")

        if len(line) != 9:
            print(f"line must contain 9 digits. Input line {line_counter} again.\nNote: type '0' for empty cell")
            continue
        elif line.isdecimal() is False:
            print(f"line must contain only digits. Input line {line_counter} again.\nNote: type '0' for empty cell")
            continue
        else:
            line_counter += 1
            board_sequence += line

        if line_counter == 10:
            if input_validation(board_sequence) is True:
                return board_sequence
            else:
                print("Input is not valid. Try again.")
                line_counter = 1


def input_validation(board_sequence):
    """Validation of user input. Be aware that function checks only repetition of number in rows, columns and squares
        not the solvability of puzzle. Return True if input is valid, else return False"""

    counter_line = 0
    counter_col = 0

    for i in range(9):
        line = set()
        column = set()
        for _ in range(9):

            # line check
            if board_sequence[counter_line] != "0":
                if board_sequence[counter_line] not in line:
                    line.add(board_sequence[counter_line])
                else:
                    return False
            counter_line += 1

            # column check
            if board_sequence[counter_col] != "0":
                if board_sequence[counter_col] not in column:
                    column.add(board_sequence[counter_col])
                else:
                    return False
            counter_col += 9
        counter_col -= 80
    return True


def start_here():
    """Start program"""
    # input from console or sample
    #board_sequence = input_from_console()
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

    # input("Press any key to start")
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