from algorithms import BruteForce, CombinedSolver, SmartSolver
from settings import Settings
import time
import typing


# Examples. Take user input by uncomment line 148 and commend line 149 to take input from user
# Easy
#sample = "000004670009200801007613049050100284010000396496800050300061020085400060900078000"
# Hard. Slowly solved by bruteforce but fast by smarter alghorithm
sample = "000801000000000043500000000000070800000000100020030000600000075003400000000200600"
# Hard, designed against bruteforce. Very slow solution using bruteforce but fast solved using smarter algorithm
#sample = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"


class Game:
    """stores board state and methods
    board: (nested list of rows) Representation of the board. 0 = empty cell
    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8]]"""

    board: typing.List[typing.List[int]] = []

    def __init__(self, input_sequence: typing.AnyStr):
        """Transformation of input string into list of int"""
        position_counter = 0

        for _ in range(Settings.row_number):
            row = []
            for _ in range(Settings.column_number):
                row.append(int(input_sequence[position_counter]))
                position_counter += 1
            self.board.append(row)

    def draw(self):
        """Draw current state of board in human-friendly form"""

        row_counter = 0
        column_counter = 0

        print("-" * Settings.screen_width)

        for row in self.board:
            print("| ", end="")
            for cell in row:
                if cell != 0:
                    print(cell, end=" ")
                else:
                    print(" ", end=" ")
                row_counter += 1
                if row_counter == 3:
                    print("| ", end="")
                    row_counter = 0
            column_counter += 1
            if column_counter == 3:
                print("\n", "-" * Settings.screen_width, sep="")
                column_counter = 0
            else:
                print()

    def brutal_solution(self):
        """Bruteforce with backtracking. Check every state of board until find correct one"""
        solver = BruteForce(self.board)
        self.board = solver.solve()

    def less_brutal_solution(self):
        """Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using
        bruteforce"""
        solver = CombinedSolver(self.board)
        self.board = solver.solve()

    def smart_solution(self):
        """Implementation of James Crook algorithm."""
        solver = SmartSolver(self.board)
        self.board = solver.solve()


def input_from_console() -> typing.AnyStr:
    """Takes input from user using console and check if it is correct.
    :returns: board sequence (string)."""
    board_sequence = ""
    line_counter = 1
    print("Insert board state (from left to right, without space, 'Enter' after every line)\nif cell is empty type '0'")
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


def input_validation(board_sequence: typing.AnyStr) -> bool:
    """Validation of user input. Be aware that function checks only repetition of number in rows, columns and squares
        not the solvability of puzzle. Return True if input is valid, else return False
        :param board_sequence: Inserted interpretation of board
        :return: True if sequence is correct otherwise False"""

    counter_line = 0
    counter_col = 0

    for _ in range(Settings.row_number):
        line = set()
        column = set()
        for _ in range(Settings.column_number):

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
    # input from console or sample. Uncomment line 148 and commend line 149 to take input from user
    # board_sequence = input_from_console()
    board_sequence = sample

    # initiation of Board instance and draw initial state
    game = Game(board_sequence)
    game.draw()

    # show menu and select algorithm
    while True:
        x = input("1. Brutal solution\n2. Less brutal solution\n3. Smart solution\nChoose solution: ")

        if x != "1" and x != "2" and x != "3":
            print("unknown command. Try again\n")
        else:
            break

    print("Working...")

    if x == "1":
        start = time.time()
        game.brutal_solution()
    elif x == "2":
        start = time.time()
        game.less_brutal_solution()
    elif x == "3":
        start = time.time()
        game.smart_solution()

    stop = time.time()
    game.draw()
    print(f"complete in {stop - start} sec")


if __name__ == "__main__":
    start_here()
