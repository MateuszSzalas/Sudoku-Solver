from random import randint

class Parent:
    """brute force alghoritm for solving sudoku
    hash_board: dict which assign TBD
    """
    hash_board = None
    squares = {}  # dict: key = position index, value = square number
    unchangable = None  # set of indexes of unchangable cells

    @classmethod
    def init(cls, board):
        """initialization"""
        cls.hash_board = {
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

        # preperation of squares hash map
        start1, stop1 = 0, 3
        start2, stop2 = 9, 12
        start3, stop3 = 18, 21

        index = 1
        for _ in range(3):
            for _ in range(3):

                for i, j, k in zip(range(start1, stop1), range(start2, stop2), range(start3, stop3)):
                    cls.squares[i], cls.squares[j], cls.squares[k] = 30 + index, 30 + index, 30 + index
                index += 1
                start1, stop1 = start1 + 3, stop1 + 3
                start2, stop2 = start2 + 3, stop2 + 3
                start3, stop3 = start3 + 3, stop3 + 3

            start1, stop1 = start1 + 18, stop1 + 18
            start2, stop2 = start2 + 18, stop2 + 18
            start3, stop3 = start3 + 18, stop3 + 18

        # set of unchangable positions
        cls.unchangable = {i for i in range(81) if board[i] != 0}

    @classmethod
    def coordinates_detect(cls, pos):
        """calculate position of cell. Return row, column and square"""
        row = pos // 9 + 1
        col = 1 + int(pos / 0.9 % 10)
        square = cls.squares[pos]

        return row, col, square

    @classmethod
    def remove(cls, value, row, col, square):
        """remove value from hashtable"""

        cls.hash_board[10 + row].remove(value)
        cls.hash_board[20 + col].remove(value)
        cls.hash_board[square].remove(value)

    @classmethod
    def update(cls, value, row, col, square):
        """add value to hashtable"""

        cls.hash_board[10 + row].add(value)
        cls.hash_board[20 + col].add(value)
        cls.hash_board[square].add(value)

    @classmethod
    def check_move(cls, value, row, col, square):
        """Return True if move is valid"""

        if (
                value not in cls.hash_board[10 + row]
                and value not in cls.hash_board[20 + col]
                and value not in cls.hash_board[square]
        ):

            return True
        else:
            return False

print("tets")
class BruteForce(Parent):
    @classmethod
    def start(cls, board):
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
                    row, col, square = cls.coordinates_detect(pos)

                    cls.remove(board[pos], row, col, square)
                    board[pos] += 1
                    break
                else:
                    if pos == 81:
                        break
                    row, col, square = cls.coordinates_detect(pos)

                    empty = True
                    board[pos] = 1
                    break

            if pos == 81:
                break

            for _ in range(10 - board[pos]):
                if cls.check_move(board[pos], row, col, square):
                    cls.update(board[pos], row, col, square)
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

    @classmethod
    def placeholder(cls, board, pos=0):
        """recursive solution TBD"""
        current_board = board

        while True:
            if current_board[pos] != 0 and pos < 80:
                pos += 1
            else:
                break

        current_board[pos] = 1

        for _ in range(1, 9):
            if cls.check_move(pos, current_board[pos]):
                cls.update(pos, current_board[pos])
                cls.solution(current_board, pos=pos + 1)
            else:
                current_board[pos] += 1

        current_board[pos] = 0
        if pos == 80:
            return current_board

class BruteForceWithMarkup(BruteForce):
    markup = {}

    @classmethod
    def start(cls, board):
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
                    row, col, square = cls.coordinates_detect(pos)

                    cls.remove(board[pos], row, col, square)

                    while True:
                        board[pos] += 1
                        if board[pos] in cls.markup[pos] or board[pos] >= 9:
                            break

                    break
                else:
                    if pos == 81:
                        break
                    row, col, square = cls.coordinates_detect(pos)

                    empty = True
                    board[pos] = 1
                    break

            if pos == 81:
                break

            for _ in range(10 - board[pos]):
                if cls.check_move(board[pos], row, col, square):
                    cls.update(board[pos], row, col, square)
                    pos += 1
                    empty = False
                    break
                else:
                    while True:
                        board[pos] += 1
                        if board[pos] in cls.markup[pos] or board[pos] >= 9:
                            break
            else:
                # if not vaild number at pos
                board[pos] = 0
                pos -= 1
        return board

    @classmethod
    def fill_obvious(cls, board):
        """ If only 1 value is valid set cell to this value, update unchangable cells set and return
        new board"""
        added = True
        cls.init(board)
        while added is True:
            for pos, cell in enumerate(board):
                if cell == 0:
                    row, col, square = cls.coordinates_detect(pos)
                    vaild_values = []
                    for i in range(1, 10):
                        if cls.check_move(i, row, col, square) is True:
                            vaild_values.append(i)

                    if len(vaild_values) == 1:
                        board[pos] = vaild_values[0]
                        cls.unchangable.add(pos)
                        print(cls.unchangable)
                    else:
                        added = False

        return board

    @classmethod
    def create_markup(cls, board):
        """fill cls.markup dict: key = position of empty cell (0 - 80), value = set of possible values at this position
        based on filled cells. If only 1 value is valid set cell to this value, update unchangable cells set and return
        new board
        """
        for pos, cell in enumerate(board):
            if cell == 0:
                row, col, square = cls.coordinates_detect(pos)
                vaild_values = []
                for i in range(1, 10):
                    if cls.check_move(i, row, col, square) is True:
                        vaild_values.append(i)

                if len(vaild_values) == 1:
                    board[pos] = vaild_values[0]
                    cls.unchangable.add(pos)
                else:
                    cls.markup[pos] = set(vaild_values)
        return board


class RandomSolver(Parent):
    """randomly assign values to empty cells until puzzle is solved"""
    @classmethod
    def randemonium(cls, board):
        cls.init(board)
        # repeat until solved
        while True:
            for pos, cell in enumerate(board):
                if pos in cls.unchangable:
                    continue
                board[pos] = randint(1, 9)
            pos = 0
            stop = False

            while True:
                row, col, square = cls.coordinates_detect(pos)
                if cls.check_move(board[pos], row, col, square) is False:
                    break
                pos += 1
            else:
                break
        return board


class SmartSolver(Parent):
    markup = {}

    @classmethod
    def start(cls, board):
        cls.init(board)
        board = cls.create_markup(board)

        for i in range(9):
            
            for j in range(9):


    @classmethod
    def create_markup(cls, board):
        """fill cls.markup dict: key = position of empty cell (0 - 80), value = set of possible values at this position
        based on filled cells. If only 1 value is valid set cell to this value, update unchangable cells set and return
        new board
        """

        while True:
            any_cell_changed = False
            for pos, cell in enumerate(board):

                if cell == 0:
                    row, col, square = cls.coordinates_detect(pos)
                    vaild_values = []
                    for i in range(1, 10):
                        if cls.check_move(i, row, col, square) is True:
                            vaild_values.append(i)

                    if len(vaild_values) == 1:
                        board[pos] = vaild_values[0]
                        cls.unchangable.add(pos)
                        any_cell_changed = True
                        cls.update(board[pos], row, col, square)

                    else:
                        cls.markup[pos] = set(vaild_values)

            if any_cell_changed is False:
                break

        return board

