from copy import copy, deepcopy

class Parent:
    """Parent class with methods and arguments common for all algorithms
    board_map:
        dict: key = (int) identificator of row (1x), column (2x) and square (3x) where x is number of this row, col or square
              value = (set of ints) set with all numbers in that row, col or square
    squares - mapping positions with squares:
        list of tuples: [(pos, square), ...] sorted by squares
    pos_map - match position with its row, collumn and square
        dict: key = (int) position
              value = [row, column, square] identificators same as in board_map
    unchangable:
        set: set which contain all possitions with fixed board numbers (clues or values found by algorithm)
    board:
        list: list representation of current board state (list index = position of cell)
    """
    board_map = None
    squares = {}  # list of tuples: [(pos, square), ...] sorted by squares
    pos_map = {}  # dict: key (int) = pos, value (int) = [row, col, sqare]
    unchangable = None  # set of indexes of unchangable cells
    board = None  # current board. List of int representation of every cell, 0 = empty cell
    show = []  # [[pos, value, cordA, cord1], ...]
    s = {11: "A", 12: "B", 13: "C", 14: "D", 15: "E", 16: "F", 17: "G", 18: "H", 19: "I"}
    c = 0

    def __init__(self, board="", standalone=False):
        """initialization
        """
        if standalone is True:
            return

        self.board = board

        # board_map creation
        self.board_map = {
            11: {board[i] for i in range(9)},
            12: {board[i] for i in range(9, 18)},
            13: {board[i] for i in range(18, 27)},
            14: {board[i] for i in range(27, 36)},
            15: {board[i] for i in range(36, 45)},
            16: {board[i] for i in range(45, 54)},
            17: {board[i] for i in range(54, 63)},
            18: {board[i] for i in range(63, 72)},
            19: {board[i] for i in range(72, 81)},

            21: {board[i] for i in range(0, 73, 9)},
            22: {board[i] for i in range(1, 74, 9)},
            23: {board[i] for i in range(2, 75, 9)},
            24: {board[i] for i in range(3, 76, 9)},
            25: {board[i] for i in range(4, 77, 9)},
            26: {board[i] for i in range(5, 78, 9)},
            27: {board[i] for i in range(6, 79, 9)},
            28: {board[i] for i in range(7, 80, 9)},
            29: {board[i] for i in range(8, 81, 9)},

            31: {board[i] for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)},
            32: {board[i] for i in (3, 4, 5, 12, 13, 14, 21, 22, 23)},
            33: {board[i] for i in (6, 7, 8, 15, 16, 17, 24, 25, 26)},
            34: {board[i] for i in (27, 28, 29, 36, 37, 38, 45, 46, 47)},
            35: {board[i] for i in (30, 31, 32, 39, 40, 41, 48, 49, 50)},
            36: {board[i] for i in (33, 34, 35, 42, 43, 44, 51, 52, 53)},
            37: {board[i] for i in (54, 55, 56, 63, 64, 65, 72, 73, 74)},
            38: {board[i] for i in (57, 58, 59, 66, 67, 68, 75, 76, 77)},
            39: {board[i] for i in (60, 61, 62, 69, 70, 71, 78, 79, 80)}
        }

        # preperation of squares map
        squares = {}
        start1, stop1 = 0, 3
        start2, stop2 = 9, 12
        start3, stop3 = 18, 21

        index = 1
        for _ in range(3):
            for _ in range(3):

                for i, j, k in zip(range(start1, stop1), range(start2, stop2), range(start3, stop3)):
                    squares[i], squares[j], squares[k] = 30 + index, 30 + index, 30 + index
                index += 1
                start1, stop1 = start1 + 3, stop1 + 3
                start2, stop2 = start2 + 3, stop2 + 3
                start3, stop3 = start3 + 3, stop3 + 3

            start1, stop1 = start1 + 18, stop1 + 18
            start2, stop2 = start2 + 18, stop2 + 18
            start3, stop3 = start3 + 18, stop3 + 18
        self.squares = sorted(squares.items(), key=lambda x: x[1])

        # mapping
        col_counter = 1
        row_counter = 1
        pos = 0
        for _ in range(9):
            for _ in range(9):
                self.pos_map[pos] = []
                self.pos_map[pos].append(10 + row_counter)
                self.pos_map[pos].append(20 + col_counter)
                self.pos_map[pos].append(squares[pos])
                col_counter += 1
                pos += 1
            row_counter += 1
            col_counter = 1

        # set of unchangable positions
        self.unchangable = {i for i in range(81) if board[i] != 0}

    def remove(self, value, pos):
        """remove value from hashtable"""

        self.board_map[self.pos_map[pos][0]].remove(value)
        self.board_map[self.pos_map[pos][1]].remove(value)
        self.board_map[self.pos_map[pos][2]].remove(value)

    def update(self, value, pos):
        """add value to hashtable"""

        self.board_map[self.pos_map[pos][0]].add(value)
        self.board_map[self.pos_map[pos][1]].add(value)
        self.board_map[self.pos_map[pos][2]].add(value)
        # self.show.append([pos, value, self.s[self.pos_map[pos][0]], self.pos_map[pos][1] - 20])

    def check_move(self, value, pos):
        """Return True if move is valid"""

        if (
                value not in self.board_map[self.pos_map[pos][0]]
                and value not in self.board_map[self.pos_map[pos][1]]
                and value not in self.board_map[self.pos_map[pos][2]]):

            return True
        else:
            return False


class BruteForce(Parent):
    """Bruteforce with backtracking. Check every state of board until find correct one.
    Each cell is tested for a valid number, moving "back" when there is a violation, and moving forward again until
    the puzzle is solved."""

    def start(self):
        pos = 0
        empty = False

        while True:
            while True:
                if pos in self.unchangable and empty is False:
                    pos += 1
                elif pos in self.unchangable and empty is True:
                    pos -= 1
                elif empty is True:
                    self.remove(self.board[pos], pos)
                    self.board[pos] += 1
                    break
                else:
                    if pos == 81:
                        break
                    empty = True
                    self.board[pos] = 1
                    break

            if pos == 81:
                break

            for _ in range(10 - self.board[pos]):
                if self.check_move(self.board[pos], pos):
                    self.update(self.board[pos], pos)
                    pos += 1
                    empty = False
                    break
                else:
                    self.board[pos] += 1
            else:
                # if not vaild number at pos
                self.board[pos] = 0
                pos -= 1
        print(self.board)
        return self.board


class SmartSolver(Parent):
    """Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using
        bruteforce (less_brutal method), or complete whole puzzle using mentioned algorithm (smart_solution method).
        markup: possible values of cell - dict:
            key = position of empty cell, value = set of possible digits in that cell
        again: True if state of the board change in current check
    """
    markup = {}
    again = False

    def __init__(self, board):
        super().__init__(board)
        self.create_markup()

    def less_brutal(self):
        """Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using
        bruteforce"""
        self.create_markup()
        if len(self.unchangable) == 81:
            return self.board

        while True:
            self.again = False
            self.check_row()
            self.check_col()
            self.check_square()

            if self.again is False:
               break

        if len(self.unchangable) != 81:
            solver = BruteForce(standalone=True)

            solver.board = self.board
            solver.unchangable = self.unchangable
            solver.board_map = self.board_map
            solver.pos_map = self.pos_map
            solver.squares = self.squares

            self.board = solver.start()

        return self.board

    def smart_solution(self, pos=-1):
        """complete whole puzzle using James Crook algorithm"""
        # if board is full return it
        if len(self.unchangable) == 81:
            return self.board

        # check for obvious cells until there arent any
        while True:
            self.again = False
            self.checks()

            if self.again is False:
                break

        while len(self.unchangable) < 81:
            # find first empty cell
            for i, value in enumerate(self.board[pos+1:], pos+1):
                if value == 0:
                    self.c += 1
                    pos = i
                    break

            # set of temporary variables for easy restoration of previous board state
            temp_board = copy(self.board)
            temp_unch = copy(self.unchangable)
            temp_boardmap = deepcopy(self.board_map)

            # get value from cells markup and set cell to it
            for markup in self.markup[pos]:
                self.board[pos] = markup
                self.unchangable.add(pos)
                self.create_markup()

                # if after previous operation there are cell with no possible value revert changes and get another
                # value from markup (next loop iteration)
                if not all(self.markup.values()):
                    self.board[pos] = 0
                    self.unchangable.remove(pos)
                    self.create_markup()
                    continue
                self.update(markup, pos)

                # check for obvious cells until there aren't any
                while True:
                    self.again = False
                    self.checks()

                    if self.again is False or not all(self.markup.values()):
                        break

                # if board is full break the loop
                if len(self.unchangable) == 81:
                    break
                # or revert changes and try another value from cells markup
                else:

                    self.board = copy(temp_board)
                    self.unchangable = copy(temp_unch)
                    self.board_map = deepcopy(temp_boardmap)
                    self.create_markup()

            # if there is no solution go to next cell


        return self.board

    def checks(self):
        """search for unique values in rows, columns and squares. If True, set found value in cell
        and update board state"""
        self.check_row()
        self.check_col()
        self.check_square()

    def check_row(self):
        """search for unique possible value in every rows markup"""
        pos = 0
        for row in range(9):
            unique = set()  # values uniqe for the row
            where = {}  # possible value: pos. If pos == -1 > value not uniqe in this row
            for cell in range(9):
                if pos not in self.unchangable:
                    for element in self.markup[pos]:
                        if element not in unique:
                            unique.add(element)
                            where[element] = pos
                        else:
                            where[element] = -1
                pos += 1

            for value, position in where.items():
                if position != -1:
                    self.board[position] = value
                    self.unchangable.add(position)
                    self.update(value, position)
                    self.again = True

            self.update_markup()

    def check_col(self):
        """search for unique possible value in every cols markup"""
        pos = 0
        for row in range(9):
            unique = set()  # values uniqe for the row
            where = {}  # possible value: pos. If pos == -1 > value not uniqe in this col
            for cell in range(9):
                if pos not in self.unchangable:
                    for element in self.markup[pos]:
                        if element not in unique:
                            unique.add(element)
                            where[element] = pos
                        else:
                            where[element] = -1

                pos += 9
            for value, position in where.items():
                if position != -1:
                    self.board[position] = value
                    self.unchangable.add(position)
                    self.update(value, position)
                    self.again = True
            pos -= 80
            self.update_markup()

    def check_square(self):
        """search for unique possible value in every squares markup"""
        square_counter = 0
        unique = set()  # values uniqe for the row
        where = {}  # possible value: pos. If pos == -1 > value not uniqe in this col
        for pos, square in self.squares:
            if pos not in self.unchangable:
                for element in self.markup[pos]:
                    if element not in unique:
                        unique.add(element)
                        where[element] = pos
                    else:
                        where[element] = -1
            if square_counter == 8:
                for value, position in where.items():
                    if position != -1:
                        self.board[position] = value
                        self.unchangable.add(position)
                        self.update(value, position)
                        self.again = True
                self.update_markup()
                square_counter = 0
                unique = set()
                where = {}
            else:
                square_counter += 1

    def create_markup(self):
        """fill self.markup dict: key = position of empty cell (0 - 80), value = set of possible values at this position
        based on filled cells. If only 1 value is valid set cell to this value, update unchangable cells set and set
        self.board to new state.
        """
        self.markup = {}
        while True:
            any_cell_changed = False
            for pos, cell in enumerate(self.board):

                if cell == 0:
                    vaild_values = []
                    for i in range(1, 10):
                        if self.check_move(i, pos) is True:
                            vaild_values.append(i)
                    if len(vaild_values) == 1:
                        self.board[pos] = vaild_values[0]
                        self.unchangable.add(pos)
                        any_cell_changed = True
                        self.update(self.board[pos], pos)

                    else:
                        self.markup[pos] = set(vaild_values)

            if any_cell_changed is False:
                break

    def update_markup(self):
        """update self.markup after inserting value to cell. Check only values for actual cell markup.
         If only 1 value is valid set cell to this value, update unchangable cells set and set
         self.board to new state"""
        temp_markup = self.markup
        self.markup = {}
        while True:
            any_cell_changed = False
            for pos, cell in enumerate(self.board):
                if pos not in self.unchangable:
                    vaild_values = []
                    for i in temp_markup[pos]:
                        if self.check_move(i, pos) is True:
                            vaild_values.append(i)

                    if len(vaild_values) == 1:
                        self.board[pos] = vaild_values[0]
                        self.unchangable.add(pos)
                        any_cell_changed = True
                        self.update(self.board[pos], pos)

                    else:
                        self.markup[pos] = set(vaild_values)

            if any_cell_changed is False:
                break
