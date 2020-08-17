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
    pos_map = {}  # dict: key = pos, vale = [row, col, sqare]
    unchangable = None  # set of indexes of unchangable cells
    board = None  # current board. List of int representation of every cell, 0 = empty cell

    @classmethod
    def init(cls, board):
        """initialization"""
        cls.board = board

        # board_map creation
        cls.board_map = {
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
        cls.squares = sorted(squares.items(), key=lambda x: x[1])

        # mapping
        col_counter = 1
        row_counter = 1
        pos = 0
        for _ in range(9):
            for _ in range(9):
                cls.pos_map[pos] = []
                cls.pos_map[pos].append(10 + row_counter)
                cls.pos_map[pos].append(20 + col_counter)
                cls.pos_map[pos].append(squares[pos])
                col_counter += 1
                pos += 1
            row_counter += 1
            col_counter = 1

        # set of unchangable positions
        cls.unchangable = {i for i in range(81) if board[i] != 0}

    @classmethod
    def remove(cls, value, pos):
        """remove value from hashtable"""

        cls.board_map[cls.pos_map[pos][0]].remove(value)
        cls.board_map[cls.pos_map[pos][1]].remove(value)
        cls.board_map[cls.pos_map[pos][2]].remove(value)

    @classmethod
    def update(cls, value, pos):
        """add value to hashtable"""

        cls.board_map[cls.pos_map[pos][0]].add(value)
        cls.board_map[cls.pos_map[pos][1]].add(value)
        cls.board_map[cls.pos_map[pos][2]].add(value)

    @classmethod
    def check_move(cls, value, pos):
        """Return True if move is valid"""

        if (
                value not in cls.board_map[cls.pos_map[pos][0]]
                and value not in cls.board_map[cls.pos_map[pos][1]]
                and value not in cls.board_map[cls.pos_map[pos][2]]):

            return True
        else:
            return False


class BruteForce(Parent):
    """Bruteforce with backtracking. Check every state of board until find correct one.
    Each cell is tested for a valid number, moving "back" when there is a violation, and moving forward again until
    the puzzle is solved."""
    @classmethod
    def start(cls, board):
        if cls.board is None:
            cls.init(board)
        pos = 0
        empty = False

        while True:
            while True:
                if pos in cls.unchangable and empty is False:
                    pos += 1
                elif pos in cls.unchangable and empty is True:
                    pos -= 1
                elif empty is True:
                    cls.remove(board[pos], pos)
                    board[pos] += 1
                    break
                else:
                    if pos == 81:
                        break
                    empty = True
                    board[pos] = 1
                    break

            if pos == 81:
                break

            for _ in range(10 - board[pos]):
                if cls.check_move(board[pos], pos):
                    cls.update(board[pos], pos)
                    pos += 1
                    empty = False
                    break
                else:
                    board[pos] += 1
            else:
                # if not vaild number at pos
                board[pos] = 0
                pos -= 1
        return board


class SmartSolver(Parent):
    """Fill part of the board (or whole in easier puzzles) using James Crook Occupancy theorem and fill rest using
        bruteforce.
        markup: possible values of cell - dict:
            key = position of empty cell, value = set of possible digits in that cell
    """
    markup = {}
    again = False

    @classmethod
    def start(cls, board):
        cls.init(board)
        cls.create_markup()
        if len(cls.unchangable) == 81:
            return cls.board

        while True:
            cls.again = False
            cls.check_row()
            cls.check_col()
            cls.check_square()

            if cls.again is False:
               break

        if len(cls.unchangable) != 81:
            cls.board = BruteForce.start(cls.board)

        return cls.board

    @classmethod
    def check_row(cls):
        """search for unique possible value in every rows markup"""
        pos = 0
        for row in range(9):
            unique = set()  # values uniqe for the row
            where = {}  # possible value: pos. If pos == -1 > value not uniqe in this row
            for cell in range(9):
                if pos not in cls.unchangable:
                    for element in cls.markup[pos]:
                        if element not in unique:
                            unique.add(element)
                            where[element] = pos
                        else:
                            where[element] = -1
                pos += 1

            for value, position in where.items():
                if position != -1:
                    cls.board[position] = value
                    cls.unchangable.add(position)
                    cls.update(value, position)
                    cls.again = True
            cls.update_markup()

    @classmethod
    def check_col(cls):
        """search for unique possible value in every cols markup"""
        pos = 0
        for row in range(9):
            unique = set()  # values uniqe for the row
            where = {}  # possible value: pos. If pos == -1 > value not uniqe in this col
            for cell in range(9):
                if pos not in cls.unchangable:
                    for element in cls.markup[pos]:
                        if element not in unique:
                            unique.add(element)
                            where[element] = pos
                        else:
                            where[element] = -1

                pos += 9
            for value, position in where.items():
                if position != -1:
                    cls.board[position] = value
                    cls.unchangable.add(position)
                    cls.update(value, position)
                    cls.again = True
            pos -= 80
            cls.update_markup()

    @classmethod
    def check_square(cls):
        """search for unique possible value in every squares markup"""
        square_counter = 0
        unique = set()  # values uniqe for the row
        where = {}  # possible value: pos. If pos == -1 > value not uniqe in this col
        for pos, square in cls.squares:
            if pos not in cls.unchangable:
                for element in cls.markup[pos]:
                    if element not in unique:
                        unique.add(element)
                        where[element] = pos
                    else:
                        where[element] = -1
            if square_counter == 8:
                for value, position in where.items():
                    if position != -1:
                        cls.board[position] = value
                        cls.unchangable.add(position)
                        cls.update(value, position)
                        cls.again = True
                cls.update_markup()
                square_counter = 0
                unique = set()
                where = {}
            else:
                square_counter += 1

    @classmethod
    def create_markup(cls):
        """fill cls.markup dict: key = position of empty cell (0 - 80), value = set of possible values at this position
        based on filled cells. If only 1 value is valid set cell to this value, update unchangable cells set and set
        cls.board to new state.
        """

        while True:
            any_cell_changed = False
            for pos, cell in enumerate(cls.board):

                if cell == 0:
                    vaild_values = []
                    for i in range(1, 10):
                        if cls.check_move(i, pos) is True:
                            vaild_values.append(i)
                    if len(vaild_values) == 1:
                        cls.board[pos] = vaild_values[0]
                        cls.unchangable.add(pos)
                        any_cell_changed = True
                        cls.update(cls.board[pos], pos)

                    else:
                        cls.markup[pos] = set(vaild_values)

            if any_cell_changed is False:
                break

    @classmethod
    def update_markup(cls):
        """update cls.markup after inserting value to cell. Check only values for actual cell markup.
         If only 1 value is valid set cell to this value, update unchangable cells set and set
         cls.board to new state"""
        temp_markup = cls.markup
        while True:
            any_cell_changed = False
            for pos, cell in enumerate(cls.board):
                if pos not in cls.unchangable:
                    vaild_values = []
                    for i in temp_markup[pos]:
                        if cls.check_move(i, pos) is True:
                            vaild_values.append(i)

                    if len(vaild_values) == 1:
                        cls.board[pos] = vaild_values[0]
                        cls.unchangable.add(pos)
                        any_cell_changed = True
                        cls.update(cls.board[pos], pos)

                    else:
                        cls.markup[pos] = set(vaild_values)

            if any_cell_changed is False:
                break
