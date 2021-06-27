# A test of our sudoku solver program
# Creates a sudoku puzzle of user-defined size and attempts to solve it
# Outputs to console

from solver import Solver
import time
import math

def main():
    
    # the puzzle size and number of initial values for creating the puzzle
    puzzle_size = 9
    num_initial_values = 20
    
    # puzzle size must be set before creating or solving puzzle
    Solver.set_size(puzzle_size)
    
    # create a puzzle (puzzle can also be generated manually using a 2d list of size n^2 (where n is an integer and n > 1)
    # the argument passed to Solver.create_puzzle() is the number of initial values in the puzzle
    test_grid = Solver.create_puzzle(num_initial_values)
    box_size = int(math.sqrt(puzzle_size))
    
    # Our unsolved puzzle
    print("Puzzle")
    horizontal_line = ""
    output = "%1d"
    digit_num = 2

    # puzzle size of > 16 require double digits (used for output formatting)
    if puzzle_size > 9:
        digit_num = 3
        output = "%02d"

    line_len = puzzle_size * digit_num + box_size * 2 + 1  
    
    for a in range(line_len):
        horizontal_line = horizontal_line + "-"
        
    for y in range(len(test_grid)):
        if (y % box_size == 0):
            print(horizontal_line)    
        for x in range(len(test_grid)):
            if (x % box_size == 0):
                print("|", end = " ")
            print(output % (test_grid[y][x]), end = " ")
        print("|", end = "\n")
    print(horizontal_line) 
    
    print()
    
    # Output results of solver
    if(Solver.solve(test_grid)):
        print("Solved Puzzle")
        for y in range(len(test_grid)):
            if (y % box_size == 0):
                print(horizontal_line)   
            for x in range(len(test_grid)):
                if (x % box_size == 0):
                    print("|", end = " ")
                print(output % (test_grid[y][x]), end = " ")
            print("|", end = "\n")
        print(horizontal_line)             
    else:
        print("Unsolveable Puzzle")

main()