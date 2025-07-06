"""Utility functions for both sudoku.py and sudoku3.py"""
import numpy as np

def get_square_indices(square_index: int) -> tuple[list[int], list[int]]:
    """Return row and col indices for a given 3x3 square index (0–8)."""
    row_start = (square_index // 3) * 3
    col_start = (square_index % 3) * 3
    rows = [row_start + i for i in range(3)]
    cols = [col_start + j for j in range(3)]
    return rows, cols

def extract_squares(field: np.ndarray) -> dict[int, set[int]]:
    """Returns dict mapping square index (0–8) to a set of non-zero values."""
    squares = {}
    for idx in range(9):
        rows, cols = get_square_indices(idx)
        square = field[np.ix_(rows, cols)]
        squares[idx] = set(int(x) for x in square.ravel() if x != 0) 
    return squares



def check_solution(field:list[list[int]])->bool:
    """
    Validates a completed Sudoku grid.

    Args:
        field: A 2D list representing a Sudoku grid, where each element is an integer from 1 to 9.

    Returns:
        bool: True if the grid is a valid Sudoku solution, meaning each row, column, and 3x3 square
              contains all digits from 1 to 9 exactly once. False otherwise.
    """

    valid_set = set(range(1, 10))
    field_array = np.array(field)
    N = len(field)
    squares = extract_squares(field_array)
    for i in range(N):
        # Check row contraint
        row_set = set([x for x in field_array[i]])
        if row_set != valid_set:  
            print(f"Error in row {i}")
            return False

        # Check column contraint
        col_set = set([x for x in field_array[:, i]])
        if col_set != valid_set:  
            print(f"Error in col {i}")
            return False

        # Check square contraint
        square_set = set([x for x in squares[i]])
        if square_set != valid_set:  
            print(f"Error in square {i}")
            return False 
    return True