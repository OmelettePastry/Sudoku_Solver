from solver import Solver
import time

def main():
    
    # possibly for later use with variable sudoku grid sizes
    puzzle_size = 9
    
    Solver.set_size(puzzle_size)
    
    test_grid = Solver.create_puzzle(10)
    
    print("---- Puzzle -----")
    for y in range(len(test_grid)):
        for x in range(len(test_grid)):
            print("%1d" % (test_grid[y][x]), end = " ")
        print()
    
    print()
    print("- Solved Puzzle -")
    
    Solver.solve(test_grid)
    for y in range(len(test_grid)):
        for x in range(len(test_grid)):
            print("%1d" % (test_grid[y][x]), end = " ")
        print()
     
main()