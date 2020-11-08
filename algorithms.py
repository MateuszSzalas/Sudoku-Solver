from settings import Settings
from copy import copy
import pickle
from collections import defaultdict
from abc import ABC, abstractmethod
from typing import Any, DefaultDict, Dict, List, Set, Tuple


class Interface(ABC):
    """Base class with methods and arguments common for all algorithms
    square_map:
        dict: {(x, y): square_number, ... } - bind positions with square containing it
    rows:
        defaultdict: {row_number: {current_values_in_that_row}, ...} - current values in every row
    columns:
        defaultdict: {columns_number: {current_values_in_that_column}, ...} - current values in every column
    squares:
        defaultdict: {square_number: {current_values_in_that_square}, ...} - current values in every square
    unchangeable:
       set: {(x, y), ... } set which contain all positions with fixed board numbers (clues or values found by algorithm)
    board:
        nested list: [[value1, value2, ...], ...]representation of current board state (list index = position of cell).
        value = 0 -> empty cell
    """
    square_map: Dict[Tuple[int, int], int] = {}
    rows: DefaultDict[int, set] = defaultdict(set)
    columns: DefaultDict[int, set] = defaultdict(set)
    squares: DefaultDict[int, set] = defaultdict(set)
    unchangeable: Set[Tuple[int, int]] = set()
    board: List[List[int]] = None

    for y in range(Settings.row_number):
        for x in range(Settings.column_number):
            if x <= 2 and y <= 2:
                square_map[(x, y)] = 0
            elif 5 >= x > 2 >= y:
                square_map[(x, y)] = 1
            elif 5 < x <= 8 and y <= 2:
                square_map[(x, y)] = 2
            elif x <= 2 < y <= 5:
                square_map[(x, y)] = 3
            elif 2 < x <= 5 and 2 < y <= 5:
                square_map[(x, y)] = 4
            elif 8 >= x > 5 >= y > 2:
                square_map[(x, y)] = 5
            elif x <= 2 and 5 < y <= 8:
                square_map[(x, y)] = 6
            elif 2 < x <= 5 < y <= 8:
                square_map[(x, y)] = 7
            elif 5 < x <= 8 and 5 < y <= 8:
                square_map[(x, y)] = 8

    @abstractmethod
    def __init__(self, board: List[List[int]] = None, solver: 'SolverWithMarkup' = None):
        """creation of class attributes
        :param board: initial board state
        :param solver: if None attributes are initialized. If not None attributes of passed solver are used
        """
        if board is None:
            board = []
        if solver is not None:
            self.square_map = solver.square_map
            self.squares = solver.squares
            self.rows = solver.rows
            self.columns = solver.columns
            self.unchangeable = solver.unchangeable
            self.board = solver.board
            return

        self.board = board
        self.squares = defaultdict(set)
        self.rows = defaultdict(set)
        self.columns = defaultdict(set)
        self.unchangeable = set()

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell != 0:
                    self.unchangeable.add((x, y))
                self.squares[self.square_map[(x, y)]].add(cell)
                self.rows[y].add(cell)
                self.columns[x].add(cell)
        self.square_map = dict(sorted(self.square_map.items(), key=lambda sq_number: sq_number[1]))

    def remove(self, value: int, x: int, y: int):
        """remove value from rows, columns and squares sets
        :param value: removed value
        :param x: column number
        :param y: row number"""
        self.squares[self.square_map[(x, y)]].remove(value)
        self.columns[x].remove(value)
        self.rows[y].remove(value)

    def update(self, value: int, x: int, y: int):
        """add value to rows, columns and squares sets
        :param value: removed value
        :param x: column number
        :param y: row number"""
        self.squares[self.square_map[(x, y)]].add(value)
        self.columns[x].add(value)
        self.rows[y].add(value)

    def check_move(self, value: int, x: int, y: int):
        """Check if assignment number to position is valid move
        :param value: evaluated value
        :param x: evaluated coordinate x
        :param y: evaluated coordinate y
        :return: True if move is valid, otherwise False"""
        if (
            value not in self.rows[y]
            and value not in self.columns[x]
            and value not in self.squares[self.square_map[(x, y)]]
        ):
            return True
        else:
            return False

    def find_empty_cell(self, x: int, y: int, back: bool) -> Tuple[int, int, bool]:
        """find next empty cell
        :param x: starting coordinate x
        :param y: starting coordinate y
        :param back: True if going backward, False if going forward
        :return: coordinates of next empty cell"""
        while True:
            if (x, y) in self.unchangeable and back is False:
                x, y = self.move_forward(x, y)
            elif (x, y) in self.unchangeable and back is True:
                x, y = self.move_backward(x, y)
            elif back is True:
                self.remove(self.board[y][x], x, y)
                self.board[y][x] += 1
                break
            else:
                if x == 0 and y == 9:
                    break
                back = True
                self.board[y][x] = 1
                break
        return x, y, back

    def move_forward(self, x: int, y: int) -> Tuple[int, int]:
        """change current position to next one
        :param x: current coordinate x
        :param y: current coordinate y
        :return: coordinates of new position"""
        if x < 8:
            x += 1
        else:
            x = 0
            y += 1
        return x, y

    def move_backward(self, x: int, y: int) -> Tuple[int, int]:
        """change current position to previous one
        :param x: current coordinate x
        :param y: current coordinate y
        :return: coordinates of new position"""
        if x != 0:
            x -= 1
        else:
            x = 8
            y -= 1
        return x, y


class BruteForce(Interface):
    """Bruteforce with backtracking. Check every state of board until find correct one. Each cell is tested for a valid
     number, moving "back" when there is a violation, and moving forward if not, until the puzzle is solved."""

    def __init__(self, board: List[List[int]] = None, solver: 'SolverWithMarkup' = None):
        """
        :param board: initial board state
        :param solver: if None attributes are initialized. If not None attributes of passed solver are used"""
        super().__init__(board=board, solver=solver)

    def solve(self) -> List[List[int]]:
        """run bruteforce algorithm
        :return: solved board"""
        end_point = Settings.row_number
        x, y = 0, 0
        back = False  # False - move forward, True - move backward

        while True:
            x, y, back = self.find_empty_cell(x, y, back)

            if x == 0 and y == end_point:
                break

            # check if any number fit at position
            for _ in range(10 - self.board[y][x]):
                if self.check_move(self.board[y][x], x, y):
                    self.update(self.board[y][x], x, y)
                    x, y = self.move_forward(x, y)
                    back = False
                    break
                else:
                    self.board[y][x] += 1
            else:
                # if no valid number at pos go back
                self.board[y][x] = 0
                x, y = self.move_backward(x, y)

        return self.board


class SolverWithMarkup(Interface):
    """Base class for algorithms using markup
    markup:
        dict: {(x, y): {values_possible_in_that_cell}, ...} set of values possible at position (x, y)
    again:
        bool: If state of the board change during check repeat checks"""
    markup: Dict[Tuple[int, int], Set[int]] = {}
    again: bool = False

    def __init__(self, board: List[List[int]]):
        """:param board: initial board state"""
        super().__init__(board)
        self.create_markup()

    def checks(self):
        """search for unique values in rows, columns and squares. If True, set found value in cell
        and update board state"""
        self.check_row()
        self.check_column()
        self.check_square()

    def check_row(self):
        """search for unique possible value in every rows markup"""
        for y, row in enumerate(self.board):
            unique_row_values = set()
            unique_positions = {}
            for x, cell in enumerate(row):

                if (x, y) not in self.unchangeable:
                    for element in self.markup[(x, y)]:
                        if element not in unique_row_values:
                            unique_row_values.add(element)
                            unique_positions[element] = (x, y)
                        else:
                            unique_positions[element] = -1
            self.unique_positions_check(unique_positions)

    def check_column(self):
        """search for unique possible value in every columns markup"""
        for x in range(Settings.column_number):
            unique_col_values = set()
            unique_positions = {}
            for y in range(Settings.row_number):

                if (x, y) not in self.unchangeable:
                    for element in self.markup[(x, y)]:
                        if element not in unique_col_values:
                            unique_col_values.add(element)
                            unique_positions[element] = (x, y)
                        else:
                            unique_positions[element] = -1
            self.unique_positions_check(unique_positions)

    def check_square(self):
        """search for unique possible value in every squares markup"""
        for position, square in self.square_map.items():
            square_counter = 0
            unique_square_values = set()
            unique_positions = {}
            if position not in self.unchangeable:
                for element in self.markup[position]:
                    if element not in unique_square_values:
                        unique_square_values.add(element)
                        unique_positions[element] = position
                    else:
                        unique_positions[element] = -1

            if square_counter == 8:
                self.unique_positions_check(unique_positions)

            else:
                square_counter += 1

    def unique_positions_check(self, position_list: Dict):
        """Check if position_list contain unique positions (positions with only 1 possible value). If so, set unique
        position to this value.
        :param position_list: dict: {value: (x, y)} - if position is unique, {value: -1} if possition is not unique"""
        for value, position in position_list.items():
            if position != -1:
                self.board[position[1]][position[0]] = value
                self.unchangeable.add(position)
                self.update(value, position[0], position[1])
                self.again = True
        self.update_markup()

    def create_markup(self):
        """create markup - set of values that are possible in cell with coordinates (x, y) - and save it in class
        atribute. If only 1 value is valid set cell to this value, update unchangeable cells set and set
        self.board to new state.
        """
        self.markup = {}
        while True:
            any_cell_changed = False
            for y, row in enumerate(self.board):
                for x, cell in enumerate(row):
                    if cell == 0:
                        valid_values = []
                        for i in range(1, 10):
                            if self.check_move(i, x, y) is True:
                                valid_values.append(i)
                        if len(valid_values) == 1:
                            self.board[y][x] = valid_values[0]
                            self.unchangeable.add((x, y))
                            any_cell_changed = True
                            self.update(self.board[y][x], x, y)
                        else:
                            self.markup[(x, y)] = set(valid_values)

            if any_cell_changed is False:
                break

    def update_markup(self):
        """update self.markup after inserting value to cell. Check only values from actual cell markup."""
        self.markup = {}

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):

                if cell == 0:
                    valid_values = []
                    for i in range(1, 10):
                        if self.check_move(i, x, y) is True:
                            valid_values.append(i)

                        self.markup[(x, y)] = set(valid_values)


class CombinedSolver(SolverWithMarkup):
    """Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using bruteforce.
    """
    def solve(self) -> List[List[int]]:
        """
        Fill part of the board (or whole in easier puzzles) using James Crook algorithm and fill rest using bruteforce
        :return: solved board
        """
        if len(self.unchangeable) == Settings.column_number:
            return self.board

        while True:
            self.again = False
            self.checks()

            if self.again is False:
                break

        # if game is not finished finish it with bruteforce (much faster now because of extra clues)
        if len(self.unchangeable) != Settings.column_number:
            solver = BruteForce(solver=self)
            self.board = solver.solve()

        return self.board


class SmartSolver(SolverWithMarkup):
    """complete whole puzzle using James Crook algorithm"""
    def solve(self) -> List[List[int]]:
        """complete whole puzzle using James Crook algorithm"""
        if len(self.unchangeable) == Settings.cell_number:
            return self.board

        board_copy = self.save_board_state()

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == 0:
                    pos = (x, y)
                    break
            else:
                continue
            break

        for markup in self.markup[pos]:
            self.board[pos[1]][pos[0]] = markup
            self.unchangeable.add(pos)
            self.update(markup, pos[0], pos[1])
            self.create_markup()

            # perform checks
            while True:
                self.again = False
                self.checks()
                if not all(self.markup.values()):  # if any cell markup is empty selected number is not correct
                    correct = False
                    break
                if self.again is False:
                    correct = True
                    break

            # if chosen number is correct and there are still empty cells
            if correct is True:
                solver = SmartSolver(self.board)
                self.board = solver.solve()
                if len(solver.unchangeable) == Settings.cell_number:  # if puzzle finished
                    self.unchangeable = solver.unchangeable
                    return self.board
                else:  # if not finished restore board
                    self.load_board_state(board_copy)

            else:  # if not finished restore board
                self.load_board_state(board_copy)

        return self.board

    def save_board_state(self) -> List[Any]:
        """Save current board state
        :return: list with saved attributes: [board, unchangable, rows, columns, squares, markup]"""
        temp_board = pickle.dumps(self.board)
        temp_unch = copy(self.unchangeable)
        temp_rows = pickle.dumps(self.rows)
        temp_columns = pickle.dumps(self.columns)
        temp_squares = pickle.dumps(self.squares)
        temp_markup = pickle.dumps(self.markup)

        return [temp_board, temp_unch, temp_rows, temp_columns, temp_squares, temp_markup]

    def load_board_state(self, saved_copy: List[Any]):
        """Restore board state from save
        :param saved_copy: list of saved attributes: [board, unchangable, rows, columns, squares, markup]"""

        self.board = pickle.loads(saved_copy[0])
        self.unchangeable = copy(saved_copy[1])
        self.rows = pickle.loads(saved_copy[2])
        self.columns = pickle.loads(saved_copy[3])
        self.squares = pickle.loads(saved_copy[4])
        self.markup = pickle.loads(saved_copy[5])
