from time import time
from utils import check_solution

def findNextCellToFill(grid:list[list[int]], i:int, j:int)->tuple[int, int]:
        """
        Find the next cell to fill in a Sudoku grid, given as a 2D list.

        Args:
                grid: 2D list representing a Sudoku grid
                i (int): row of the cell to start searching from
                j (int): column of the cell to start searching from

        Returns:
                tuple[int, int] containing the row and column of the next cell to fill
                or (-1, -1) if no cell is found
        """
        for x in range(i,9):
                for y in range(j,9):
                        if grid[x][y] == 0:
                                return x,y
        for x in range(0,9):
                for y in range(0,9):
                        if grid[x][y] == 0:
                                return x,y
        return -1,-1

def isValid(grid:list[list[int]], i:int, j:int, e:int)->bool:
        """
        Check if it will be legal to assign num e to the given i,j cell

        Args:
                grid: 2D list representing a Sudoku grid
                i (int): row of the cell to check
                j (int): column of the cell to check
                e (int): number to check

        Returns:
                bool: True if it is legal to assign e to the i,j cell, False otherwise
        """
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
                columnOk = all([e != grid[x][j] for x in range(9)])
                if columnOk:
                        # finding the top left x,y co-ordinates of the section containing the i,j cell
                        secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
                        for x in range(secTopX, secTopX+3):
                                for y in range(secTopY, secTopY+3):
                                        if grid[x][y] == e:
                                                return False
                        return True
        return False

def solveSudoku(grid:list, i:int=0, j:int=0)->list[list]|bool:
        """
        Solve a Sudoku grid.

        Args:
                grid (list[list]): 2D list representing a Sudoku grid
                i (int): row of the cell to start searching from. Defaults to 0.
                j (int): column of the cell to start searching from. Defaults to 0.

        Returns:
                list[list]: solved Sudoku grid as a 2D list if the grid is solvable, False otherwise
        """
        i,j = findNextCellToFill(grid, i, j)
        if i == -1:
                return grid
        for e in range(1,10):
                if isValid(grid,i,j,e):
                        grid[i][j] = e
                        if solveSudoku(grid, i, j):
                                return grid
                        # Undo the current cell for backtracking
                        grid[i][j] = 0
        return False




if __name__ == "__main__":
    
    field = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

    print("Standard version:")
    
    start_time = time()
    solution = solveSudoku(field)
    end_time = time()
    time_sudoku = end_time - start_time
    print(f"The time it took to solve the sudoku is: {time_sudoku*1000:,.2f} ms")
    if solution:
        valid_solution = check_solution(solution)
        if valid_solution:
            print("The solution is valid")
        else:
            print("The solution is invalid!")
    



