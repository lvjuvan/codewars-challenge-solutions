#https://www.codewars.com/kata/55171d87236c880cea0004c6


SUDOKU_L = 9

'''
Solves the problem by first deducing which values are possible in each cell, then
starting from the one which has the fewest. Each attempt updates the rows, columns and squares
which are related to it by removing the assigned value to the possible values. If this results
no remaining possible values in an affected cell, this immediately counts as a failure. These mutations
are then undone if the attempted value failed later on. By starting with the cells with the
fewest amount of possible values, we reduce the chance that the algorithm will have to
backtrack as far back. This code runs the full set of tests in less than a second while the vanilla
version described in the instructions would time out after 12 seconds, managing about 200 random tests
'''

def solve(board):
    cells_blank = []
    cells_attempted = []

    rows = {i: [] for i in range(SUDOKU_L)}
    cols = {i: [] for i in range(SUDOKU_L)}
    squares = {i: [] for i in range(SUDOKU_L)}

    for r in range(SUDOKU_L):
        for c in range(SUDOKU_L):
            if board[r][c] == 0:
                not_allowed = get_not_allowed(r, c, board)
                curr_cell = CellPossibilities(not_allowed, r, c)
                cells_blank.append(curr_cell)
                rows[r].append(curr_cell)
                cols[c].append(curr_cell)
                squares[get_square(r, c)].append(curr_cell)

    for i in range(len(cells_blank)):
        cells_blank[i].row = rows[cells_blank[i].row_n]
        cells_blank[i].col = cols[cells_blank[i].col_n]
        cells_blank[i].square = squares[get_square(cells_blank[i].row_n, cells_blank[i].col_n)]
    while len(cells_blank) > 0:
        cells_blank.sort(key=lambda x: len(x.possible_values), reverse=True)
        current_cell = cells_blank.pop()
        while current_cell.try_next() is None:
            cells_blank.append(current_cell)
            current_cell = cells_attempted.pop()
        cells_attempted.append(current_cell)
    for cell in cells_attempted:
        board[cell.row_n][cell.col_n] = cell.value
    return board


def get_square(row, col):
    return (row // 3) * 3 + col // 3


class CellPossibilities:
    def __init__(self, not_allowed, row_n, col_n):
        self.possible_values = []
        self.mutations = {}
        for i in range(1, SUDOKU_L + 1):
            if i not in not_allowed:
                self.possible_values.append(i)
        self.row_n = row_n
        self.col_n = col_n
        self.row = None
        self.col = None
        self.square = None
        self.index = row_n * SUDOKU_L + col_n
        self.last_attempted_index = -1
        self.value = 0

    def on_value_added(self, value, index):
        if value in self.possible_values and index != self.index:
            self.mutations[index] = value
            self.possible_values.remove(value)
        return len(self.possible_values) > 0

    def on_value_removed(self, index):
        if index in self.mutations.keys() and index != self.index:
            self.possible_values.append(self.mutations[index])
            self.possible_values.sort()
            self.mutations.pop(index)

    def try_next(self):
        otw_back = self.last_attempted_index != -1
        self.last_attempted_index += 1
        if self.last_attempted_index >= len(self.possible_values):
            for i in range(len(self.row)):
                self.row[i].on_value_removed(self.index)
            for i in range(len(self.col)):
                self.col[i].on_value_removed(self.index)
            for i in range(len(self.square)):
                self.square[i].on_value_removed(self.index)
            self.last_attempted_index = -1
            self.value = 0
            return None
        value = self.possible_values[self.last_attempted_index]

        if otw_back:
            for i in range(len(self.row)):
                self.row[i].on_value_removed(self.index)
            for i in range(len(self.col)):
                self.col[i].on_value_removed(self.index)
            for i in range(len(self.square)):
                self.square[i].on_value_removed(self.index)

        for i in range(len(self.row)):
            if not self.row[i].on_value_added(value, self.index):
                return self.try_next()
        for i in range(len(self.col)):
            if not self.col[i].on_value_added(value, self.index):
                return self.try_next()
        for i in range(len(self.square)):
            if not self.square[i].on_value_added(value, self.index):
                return self.try_next()
        self.value = value
        return value


def get_not_allowed(row, col, board):
    not_allowed = set()
    for v in board[row]:
        not_allowed.add(v)
    for i in range(SUDOKU_L):
        not_allowed.add(board[i][col])
    r_start = 3 * (row // 3)
    c_start = 3 * (col // 3)
    for r_i in range(r_start, r_start + 3):
        for c_i in range(c_start, c_start + 3):
            not_allowed.add(board[r_i][c_i])
    return not_allowed



def print_board(board):
    print("----------------------------------")
    print("\n".join([" | ".join([str(v) for v in row]) for row in board]))
    print("----------------------------------")


def get_coords(index):
    return index % SUDOKU_L, index // SUDOKU_L
