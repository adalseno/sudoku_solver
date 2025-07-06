from copy import deepcopy
from utils import   check_solution
from sudoku_enhanced import  sudoku_enhanced, print_field
from sudoku_normal import solveSudoku

import time

num_iterations = 1
field = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]


start_time = time.time()
# Code block to measure
for i in range(num_iterations):
    ret_sudoku = solveSudoku(deepcopy(field))
end_time = time.time()
time_sudoku = end_time - start_time


start_time = time.time()
# Code block to measure
for i in range(num_iterations):
    ret_sudoku4 = sudoku_enhanced(field, False)
end_time = time.time()

time_sudoku4 = end_time - start_time




N = len(field)
fill_factor = 0
for i in range(N):
    for j in range(N):
        cell = field[i][j]
        if cell != 0:
            fill_factor += 1
            

# time_sudoku = timeit.timeit('sudoku()', setup='from __main__ import sudoku', number=1)
# time_sudoku2 = timeit.timeit('sudoku2()', setup='from __main__ import sudoku2', number=1)
result = f"For {num_iterations} iterations, with a fill factor of {fill_factor/(N*N):.1%}:\n"
result += f" - the enhanced version took {time_sudoku4:.5f} seconds.\n"
result += f" - the tandard version took {time_sudoku:.5f} seconds.\n"

result += f"The enhanced version is {time_sudoku/time_sudoku4:.2f} times faster.\n"




if ret_sudoku == ret_sudoku4:
    result += "The output is the same for standard version and enhanced versions."
else:
    result += "The output is different for standard version and enhanced versions."
print(result)




if ret_sudoku != ret_sudoku4:
   
    print("Enhanced solution")
    print_field(ret_sudoku4)
    print(f"The solution is valid?:{check_solution(ret_sudoku4)}")
    print()
    print("Standard solution")
    print_field(ret_sudoku)
    print(f"The solution is valid?:{check_solution(ret_sudoku)}")
else:
    if check_solution(ret_sudoku):
        print("The solution is valid.")
        print_field(ret_sudoku4)
    else:
        print("The solution is invalid!")
    



