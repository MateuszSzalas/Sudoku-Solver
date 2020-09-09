from copy import copy
import pickle


class Parent:
    """Parent class with methods and arguments common for all algorithms
    board_map:
        dict: key = (int) id of row (1x), column (2x) and square (3x) where x is number of this row, col or square
              value = (set of ints) set with all numbers in that row, col or square
    squares - match positions with squares:
        list of tuples: [(pos, square), ...] sorted by squares
    pos_map - match position with its row, column and square
        dict: key = (int) position
              value = (list of int) [row, column, square] id same as in board_map
    unchangeable:
        set: set which contain all positions with fixed board numbers (clues or values found by algorithm)
    board:
        list: list representation of current board state (list index = position of cell). 0 = empty cell
    """
    board_map = None
    squares = [
        (0, 31), (9, 31), (18, 31), (1, 31), (10, 31), (19, 31), (2, 31), (11, 31), (20, 31), (3, 32), (12, 32),
        (21, 32), (4, 32), (13, 32), (22, 32), (5, 32), (14, 32), (23, 32), (6, 33), (15, 33), (24, 33), (7, 33),
        (16, 33), (25, 33), (8, 33), (17, 33), (26, 33), (27, 34), (36, 34), (45, 34), (28, 34), (37, 34), (46, 34),
        (29, 34), (38, 34), (47, 34), (30, 35), (39, 35), (48, 35), (31, 35), (40, 35), (49, 35), (32, 35), (41, 35),
        (50, 35), (33, 36), (42, 36), (51, 36), (34, 36), (43, 36), (52, 36), (35, 36), (44, 36), (53, 36), (54, 37),
        (63, 37), (72, 37), (55, 37), (64, 37), (73, 37), (56, 37), (65, 37), (74, 37), (57, 38), (66, 38), (75, 38),
        (58, 38), (67, 38), (76, 38), (59, 38), (68, 38), (77, 38), (60, 39), (69, 39), (78, 39), (61, 39), (70, 39),
        (79, 39), (62, 39), (71, 39), (80, 39)
    ]
    pos_map = {
        0: [11, 21, 31], 1: [11, 22, 31], 2: [11, 23, 31], 3: [11, 24, 32], 4: [11, 25, 32], 5: [11, 26, 32],
        6: [11, 27, 33], 7: [11, 28, 33], 8: [11, 29, 33], 9: [12, 21, 31], 10: [12, 22, 31], 11: [12, 23, 31],
        12: [12, 24, 32], 13: [12, 25, 32], 14: [12, 26, 32], 15: [12, 27, 33], 16: [12, 28, 33], 17: [12, 29, 33],
        18: [13, 21, 31], 19: [13, 22, 31], 20: [13, 23, 31], 21: [13, 24, 32], 22: [13, 25, 32], 23: [13, 26, 32],
        24: [13, 27, 33], 25: [13, 28, 33], 26: [13, 29, 33], 27: [14, 21, 34], 28: [14, 22, 34], 29: [14, 23, 34],
        30: [14, 24, 35], 31: [14, 25, 35], 32: [14, 26, 35], 33: [14, 27, 36], 34: [14, 28, 36], 35: [14, 29, 36],
        36: [15, 21, 34], 37: [15, 22, 34], 38: [15, 23, 34], 39: [15, 24, 35], 40: [15, 25, 35], 41: [15, 26, 35],
        42: [15, 27, 36], 43: [15, 28, 36], 44: [15, 29, 36], 45: [16, 21, 34], 46: [16, 22, 34], 47: [16, 23, 34],
        48: [16, 24, 35], 49: [16, 25, 35], 50: [16, 26, 35], 51: [16, 27, 36], 52: [16, 28, 36], 53: [16, 29, 36],
        54: [17, 21, 37], 55: [17, 22, 37], 56: [17, 23, 37], 57: [17, 24, 38], 58: [17, 25, 38], 59: [17, 26, 38],
        60: [17, 27, 39], 61: [17, 28, 39], 62: [17, 29, 39], 63: [18, 21, 37], 64: [18, 22, 37], 65: [18, 23, 37],
        66: [18, 24, 38], 67: [18, 25, 38], 68: [18, 26, 38], 69: [18, 27, 39], 70: [18, 28, 39], 71: [18, 29, 39],
        72: [19, 21, 37], 73: [19, 22, 37], 74: [19, 23, 37], 75: [19, 24, 38], 76: [19, 25, 38], 77: [19, 26, 38],
        78: [19, 27, 39], 79: [19, 28, 39], 80: [19, 29, 39]
    }

    unchangeable = None  # set of indexes of unchangeable cells
    board = None  # current board. List of int representation of every cell, 0 = empty cell
    # show = []  # [[pos, value, cordA, cord1], ...]
    # s = {11: "A", 12: "B", 13: "C", 14: "D", 15: "E", 16: "F", 17: "G", 18: "H", 19: "I"}

    def __init__(self, board=None, standalone=True):
        """creation of class variables
        :param board: initial board state
        :param standalone: False if its not necessary to fill class variables
        """
        if board is None:
            board = []
        if standalone is False:
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

        # set of unchangeable positions
        self.unchangeable = {i for i in range(81) if board[i] != 0}

    def remove(self, value, pos):
        """remove value from board_map
        :param value: removed value
        :param pos: from position
        """
        self.board_map[self.pos_map[pos][0]].remove(value)
        self.board_map[self.pos_map[pos][1]].remove(value)
        self.board_map[self.pos_map[pos][2]].remove(value)

    def update(self, value, pos):
        """add value to board_map
        :param value: add value
        :param pos: to position
        """
        self.board_map[self.pos_map[pos][0]].add(value)
        self.board_map[self.pos_map[pos][1]].add(value)
        self.board_map[self.pos_map[pos][2]].add(value)
        # self.show.append([pos, value, self.s[self.pos_map[pos][0]], self.pos_map[pos][1] - 20])

    def check_move(self, value, pos):
        """Check if set number 'value' in position 'pos' is valid move
        :returns: True if move is valid, otherwise False"""
        if (
                value not in self.board_map[self.pos_map[pos][0]]
                and value not in self.board_map[self.pos_map[pos][1]]
                and value not in self.board_map[self.pos_map[pos][2]]):

            return True
        else:
            return False


class BruteForce(Parent):
    """Bruteforce with backtracking. Check every state of board until find correct one. Each cell is tested for a valid
     number, moving "back" when there is a violation, and moving forward if not, until the puzzle is solved."""

    def start(self):
        """run bruteforce algorithm
        :return: solved board"""
        pos = 0
        back = False

        while True:
            # find empty position
            while True:
                if pos in self.unchangeable and back is False:
                    pos += 1
                elif pos in self.unchangeable and back is True:
                    pos -= 1
                elif back is True:
                    self.remove(self.board[pos], pos)
                    self.board[pos] += 1
                    break
                else:
                    if pos == 81:
                        break
                    back = True
                    self.board[pos] = 1
                    break

            if pos == 81:
                break

            # check if any number fit at position
            for _ in range(10 - self.board[pos]):
                if self.check_move(self.board[pos], pos):
                    self.update(self.board[pos], pos)
                    pos += 1
                    back = False
                    break
                else:
                    self.board[pos] += 1
            else:
                # if not vaild number at pos go back
                self.board[pos] = 0
                pos -= 1

        return self.board


class SmartSolver(Parent):
    """Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using bruteforce
    (less_brutal method), or complete whole puzzle using mentioned algorithm (smart_solution method).
        markup: possible values of cell
            dict:
                key = position of empty cell
                value = set of possible digits in that cell
        again: True if state of the board change in current check
    """
    markup = {}
    again = False

    def __init__(self, board):
        super().__init__(board)
        self.create_markup()

    def less_brutal(self):
        """
        Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using bruteforce
        :return: solved board
        """
        # if board is full after
        if len(self.unchangeable) == 81:
            return self.board

        while True:
            self.again = False
            self.check_row()
            self.check_col()
            self.check_square()

            if self.again is False:
                break

        # if game is not finished solve it with bruteforce (much faster now because of extra clues)
        if len(self.unchangeable) != 81:
            solver = BruteForce(standalone=False)

            solver.board = self.board
            solver.unchangeable = self.unchangeable
            solver.board_map = self.board_map

            self.board = solver.start()

        return self.board

    def smart_solution(self):
        """complete whole puzzle using James Crook algorithm"""
        pos = 0
        # if board is full return it
        if len(self.unchangeable) == 81:
            return self.board

        # if there arent any possible move make copy of board state and check random number from markup
        temp_board = copy(self.board)
        temp_unch = copy(self.unchangeable)
        temp_boardmap = pickle.dumps(self.board_map)

        # select empty cell
        for i, value in enumerate(self.board):
            if value == 0:
                pos = i
                break

        # choose number from selected cells markup
        for markup in self.markup[pos]:
            self.board[pos] = markup
            self.unchangeable.add(pos)
            self.update(markup, pos)
            self.create_markup()

            # perform checks
            while True:
                self.again = False
                self.checks()
                if not all(self.markup.values()):  # if any cell markup is empty selected number is not correct
                    flag = False
                    break
                if self.again is False:
                    flag = True
                    break

            # if chosen number is correct and there are still empty cells
            if flag is True:
                solver = SmartSolver(self.board)
                self.board = solver.smart_solution()
                if len(solver.unchangeable) == 81:  # if puzzle finished
                    self.unchangeable = solver.unchangeable
                    return self.board
                else:  # if not finished restore board
                    self.board = copy(temp_board)
                    self.unchangeable = copy(temp_unch)
                    self.board_map = pickle.loads(temp_boardmap)
                    self.create_markup()

            else:  # if not finished restore board
                self.board = copy(temp_board)
                self.unchangeable = copy(temp_unch)
                self.board_map = pickle.loads(temp_boardmap)
                self.create_markup()

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
                if pos not in self.unchangeable:
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
                    self.unchangeable.add(position)
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
                if pos not in self.unchangeable:
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
                    self.unchangeable.add(position)
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
            if pos not in self.unchangeable:
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
                        self.unchangeable.add(position)
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
        based on filled cells. If only 1 value is valid set cell to this value, update unchangeable cells set and set
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
                        self.unchangeable.add(pos)
                        any_cell_changed = True
                        self.update(self.board[pos], pos)

                    else:
                        self.markup[pos] = set(vaild_values)

            if any_cell_changed is False:
                break

    def update_markup(self):
        """update self.markup after inserting value to cell. Check only values for actual cell markup."""
        self.markup = {}

        for pos, cell in enumerate(self.board):

            if cell == 0:
                vaild_values = []
                for i in range(1, 10):
                    if self.check_move(i, pos) is True:
                        vaild_values.append(i)

                    self.markup[pos] = set(vaild_values)
