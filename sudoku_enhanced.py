from copy import deepcopy
from time import time
from typing import Any
from utils import check_solution, extract_squares

import numpy as np


def get_square_index(row: int, col: int) -> int:
    """
    Returns the 3x3 square index (0–8) for a given row and col index.
    Args:
        row: int
        col: int
    Returns: int
    """
    return (row // 3) * 3 + (col // 3)

def get_row_set(row: int, field: np.ndarray) -> set[int]:
    """
    Returns the set of non-zero values in the given row of the given 2D array.
    Args:
        row: int
        field: np.ndarray
    Returns: set
    """
    return set( int(x) for x in field[row] if x != 0)

def get_col_set(col: int, field: np.ndarray) -> set[int]:
    """
    Returns the set of non-zero values in the given column of the given 2D array.
    Args: 
        col: int
        field: np.ndarray
    Returns: set
    """
    return set(int(x) for x in field[:, col] if x != 0)

def print_field(field:list[list[int]], display=True)->str|list[list[int]]:
    """
    Prints a sudoku field to the standard output.

    Args:
        field: A 2-dimensional list of integers. A value of 0 or a set of values
               indicates an empty cell. Otherwise the value is the number that
               should be placed in the cell.
    Returns: The solved puzzle or None if no solution is found.
    """
    if field is None:
        print("No solution")
        return None
        
    N = len(field)

        
    if display:
        for i in range(N):
            for j in range(N):
                cell = field[i][j]
                if cell == 0 or isinstance(cell, set):
                    print('.', end='')
                else:
                    print(cell, end='')
                if (j + 1) % 3 == 0 and j < 8:
                    print(' |', end='')

                if j != 8:
                    print(' ', end='')
            print()
            if (i + 1) % 3 == 0 and i < 8:
                print("- - - + - - - + - - -")

    return field

def read(field:list[list[int]])->list[list[Any]]:
    """ Read field into state (replace 0 with set of possible values) 
        Args: list
        Returns: list
    """
    N = len(field)
    state = field.tolist()
    squares = extract_squares(field)
    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if cell == 0:
                square_ind = get_square_index(i, j)
                row_set = get_row_set(i, field)
                col_set = get_col_set(j, field)
                starting_set = squares[square_ind] | row_set | col_set
                state[i][j] = set(range(1,10))-starting_set

    return state

def done(state:list[list[Any]])->bool:
    """ Are we done? 
        Args: list
        Returns: bool
    """
    for row in state:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True

def get_current_constraints(state: list[list[Any]], row: int, col: int) -> set[int]:
    """Get all values that are currently constrained for position (row, col)
        Args: list
        Returns: set
    """
    constraints = set()
    
    # Row constraints
    for j in range(9):
        if j != col and not isinstance(state[row][j], set):
            constraints.add(state[row][j])
    
    # Column constraints
    for i in range(9):
        if i != row and not isinstance(state[i][col], set):
            constraints.add(state[i][col])
    
    # Box constraints
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(box_row_start, box_row_start + 3):
        for j in range(box_col_start, box_col_start + 3):
            if (i != row or j != col) and not isinstance(state[i][j], set):
                constraints.add(state[i][j])
    
    return constraints

def naked_singles(state: list[list[Any]]) -> tuple[bool, bool]:
    """Find cells with only one possible value (naked singles)
        Args: list
        Returns: tuple[bool, bool]
    """
    changed = False
    N = len(state)
    
    for i in range(N):
        for j in range(N):
            if isinstance(state[i][j], set):
                # Remove all current constraints
                constraints = get_current_constraints(state, i, j)
                state[i][j] -= constraints
                
                if len(state[i][j]) == 0:
                    return False, False  # Invalid state
                elif len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    changed = True
    
    return True, changed

def hidden_singles(state: list[list[Any]]) -> tuple[bool, bool]:
    """Find values that can only go in one cell within a unit (hidden singles)
        Args: lisy
        Returns: tuple[bool, bool]
    """
    changed = False
    N = len(state)
    
    # Check rows
    for i in range(N):
        for digit in range(1, 10):
            # Skip if digit is already placed in this row
            if digit in [state[i][j] for j in range(N) if not isinstance(state[i][j], set)]:
                continue
                
            possible_positions = []
            for j in range(N):
                if isinstance(state[i][j], set) and digit in state[i][j]:
                    possible_positions.append(j)
            
            if len(possible_positions) == 1:
                j = possible_positions[0]
                if isinstance(state[i][j], set) and len(state[i][j]) > 1:
                    state[i][j] = digit
                    changed = True
            elif len(possible_positions) == 0:
                return False, False  # Invalid state - digit cannot be placed
    
    # Check columns
    for j in range(N):
        for digit in range(1, 10):
            # Skip if digit is already placed in this column
            if digit in [state[i][j] for i in range(N) if not isinstance(state[i][j], set)]:
                continue
                
            possible_positions = []
            for i in range(N):
                if isinstance(state[i][j], set) and digit in state[i][j]:
                    possible_positions.append(i)
            
            if len(possible_positions) == 1:
                i = possible_positions[0]
                if isinstance(state[i][j], set) and len(state[i][j]) > 1:
                    state[i][j] = digit
                    changed = True
            elif len(possible_positions) == 0:
                return False, False  # Invalid state - digit cannot be placed
    
    # Check 3x3 boxes
    for box_idx in range(9):
        box_row_start = (box_idx // 3) * 3
        box_col_start = (box_idx % 3) * 3
        
        for digit in range(1, 10):
            # Skip if digit is already placed in this box
            placed_values = set()
            for i in range(box_row_start, box_row_start + 3):
                for j in range(box_col_start, box_col_start + 3):
                    if not isinstance(state[i][j], set):
                        placed_values.add(state[i][j])
            
            if digit in placed_values:
                continue
                
            possible_positions = []
            for i in range(box_row_start, box_row_start + 3):
                for j in range(box_col_start, box_col_start + 3):
                    if isinstance(state[i][j], set) and digit in state[i][j]:
                        possible_positions.append((i, j))
            
            if len(possible_positions) == 1:
                i, j = possible_positions[0]
                if isinstance(state[i][j], set) and len(state[i][j]) > 1:
                    state[i][j] = digit
                    changed = True
            elif len(possible_positions) == 0:
                return False, False  # Invalid state - digit cannot be placed
    
    return True, changed

def propagate_step(state: list[list[Any]]) -> tuple[bool|None, bool|None]:
    """
    Enhanced propagation step that applies multiple constraint techniques.
    Args: list
    
    Returns: A two-tuple that says whether the configuration
            is solvable and whether the propagation changed the state.
    """
    overall_changed = False
    
    # Apply naked singles (cells with only one possible value)
    valid, changed = naked_singles(state)
    if not valid:
        return False, None
    if changed:
        overall_changed = True
    
    # Apply hidden singles (values that can only go in one cell)
    valid, changed = hidden_singles(state)
    if not valid:
        return False, None
    if changed:
        overall_changed = True
    
    return True, overall_changed





def propagate(state:list[list[Any]], use_enhanced=True)->bool:
    """ Propagate until we reach a fixpoint 
        Args:
           state: list
        return: bool  
    """
    while True:
        solvable, new_unit = propagate_step(state)
        
        if not solvable:
            return False
        if not new_unit:
            return True

def solve(state:list[list[Any]])->list[list[Any]]:
    """ Solve sudoku """
    N = len(state)
    solvable = propagate(state)

    if not solvable:
        return None

    if done(state):
        return state

    # Find the cell with minimum remaining values (MRV heuristic)
    min_possibilities = 10
    best_cell = None
    
    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if isinstance(cell, set) and len(cell) < min_possibilities:
                min_possibilities = len(cell)
                best_cell = (i, j)
    
    if best_cell:
        i, j = best_cell
        cell = state[i][j]
        for value in cell:
            new_state = deepcopy(state)
            new_state[i][j] = value
            solved = solve(new_state)
            if solved is not None:
                return solved
    
    return None

def sudoku_enhanced(field:list[list[int]]|None=None, display:bool=True, use_enhanced=True)->list[list[int]]|None:
    """
    Enhanced sudoku solver with improved propagation techniques.
    
    Args:
        field: The sudoku puzzle as a 2D list. 0 represents empty cells.
        display: Whether to display the solution.
        
    return: The solved sudoku puzzle as a 2D list or None if no solution is found.
    """
    if field is None:
        field = [[5,1,7,6,0,0,0,3,4],
                [2,8,9,0,0,4,0,0,0],
                [3,4,6,2,0,5,0,9,0],
                [6,0,2,0,0,0,0,1,0],
                [0,3,8,0,0,6,0,4,7],
                [0,0,0,0,0,0,0,0,0],
                [0,9,0,0,0,0,0,7,8],
                [7,0,3,4,0,0,5,6,0],
                [0,0,0,0,0,0,0,0,0]]

    field = np.array(field)
    state = read(field)
    return print_field(solve(state), display)


if __name__ == "__main__":
    print("Enhanced version:")
    
    start_time = time()
    solution = sudoku_enhanced()
    end_time = time()
    time_sudoku = end_time - start_time
    print(f"The time it took to solve the sudoku is: {time_sudoku*1000:,.2f} ms")
    if solution:
        valid_solution = check_solution(solution)
        if valid_solution:
            print("The solution is valid")
        else:
            print("The solution is invalid!")
    
    