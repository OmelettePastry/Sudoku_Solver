# Sudoku solver, creator
#
# This class has static methods to create and solve sudoku puzzles of size n^2, where n is a integer and n > 1
#   (The actual dimensions will be (n^2) by (n^2))
#
# Comments:
# 1. Rename variables more appropriately

import copy     # deepcopy used for 3d list
import random
import math

class Solver:

    # dictionaries used for determining box number of cell
    # will be populated with init_dict()
    box_dict = {}
    box_dict_id = {}
    sudoku_puzzle_size = 9

    @classmethod
    def set_size(cls, size):
        Solver.sudoku_puzzle_size = size
        Solver.init_dict(Solver.sudoku_puzzle_size)

    # initializes the box dictionaries for specified puzzle grid size
    # Note: Please use the square root of the actual size
    @classmethod
    def init_dict(cls, puzzle_size):

        box_size = int(math.sqrt(puzzle_size))

        # clear dictionaries
        Solver.box_dict.clear()
        Solver.box_dict_id.clear()
        
        box_list = [[] for j in range(puzzle_size)]

        # default values to -1
        box_row = -1
        box_column = -1

        # loop to append cell coordinates to appropriate box number
        for y in range(puzzle_size):
            for x in range(puzzle_size):
                for i in range(box_size):
                    max = box_size * (i + 1) - 1
                    min = box_size * i
                    
                    if (x >= min and x <= max):
                        box_column = i
                    if (y >= min and y <= max):
                        box_row = i
                        
                box_number = box_size * box_row + box_column
                box_list[box_number].append((y,x))

        # assign key i to value (value is a list of 2-element tuples (y,x coodrinate))
        for i in range(puzzle_size):
            Solver.box_dict[i] = box_list[i]

        # box_dict_id: key = y,x coordinates and value = box number
        for j in range(puzzle_size):
            for k in range(puzzle_size):
                coord = box_list[j][k]
                Solver.box_dict_id[coord] = j

    # create a puzzle
    # parameters --
    # puzzle_grid: 2d list of the grid
    # num_numbers: number of initial values to populate the grid

    # ? should we create the puzzle_grid here?
    @classmethod    
    def create_puzzle(cls, num_numbers):
        
        puzzle_grid = [[0 for y in range(Solver.sudoku_puzzle_size)] for x in range(Solver.sudoku_puzzle_size)]
        
        # new cell possibles (1 to size, in each cell)
        cell_possibles = [[list(range(1, Solver.sudoku_puzzle_size + 1)) for b in range(Solver.sudoku_puzzle_size)] for c in range(Solver.sudoku_puzzle_size)]
        
        # generate initial puzzle grid coordinates
        x = random.randint(0, Solver.sudoku_puzzle_size - 1)
        y = random.randint(0, Solver.sudoku_puzzle_size - 1)
        
        solveable = True
        counter = 0

        # loop while initial numbers are less than max numbers
        while(counter != num_numbers):
            counter = 0
            
            # loop while you have fewer numbers than needed and it's solveable
            while(counter < num_numbers) and (solveable == True):
            
                # get coordinates of grid that has not been initialized with a value yet
                while(puzzle_grid[y][x] != 0):
                    x = random.randint(0, Solver.sudoku_puzzle_size - 1)
                    y = random.randint(0, Solver.sudoku_puzzle_size - 1)
                    
                # get random value from cell_possibles at current location
                num_choice = random.choice(cell_possibles[y][x])
                puzzle_grid[y][x] = num_choice
                cell_possibles[y][x].clear()
                cell_possibles[y][x] = [puzzle_grid[y][x]]
                
                # if this value causes issues with other cells, then it is unsolveable
                if not Solver.remove_num_cell(cell_possibles, num_choice, y, x):
                    solveable = False
                if not Solver.remove_num_box(cell_possibles, num_choice, y, x):
                    solveable = False
                
                # increment counter only when it is still solveable
                # ensures the outermost loop ends only when we have all valid values in the cells
                if solveable != False:
                    counter = counter + 1

        return puzzle_grid
        

    # solver method
    @classmethod    
    def solve(cls, grid):
        
        grid_size = len(grid)
        
        # create 3-dimensional list, where row = row of number, column = column of number, depth = list of possilbe values for the cell
        #   size: row, column and depth size of 9
        #   contents: sequence from 1 to 9
        cell_possibles = [[list(range(1, grid_size + 1)) for b in range(grid_size)] for c in range(grid_size)]

        # initally remove all possible values for cell according to the initial sudoku puzzle values
        Solver.remove_initial_possibles(grid, cell_possibles)
        
        return Solver.solve_helper(grid, cell_possibles, 0, 0)

    # helper function (used by solve() function)
    @classmethod    
    def solve_helper(cls, grid, cell_possibles, row, column):

        # go to next row is column index is over the maximum grid column index size
        if (row < len(grid)) and (column == len(grid)):
            row = row + 1
            column = 0
            
        # if row index is more than the maximum row index size, we have traversed
        #  through the entire grid successfully, return True
        if (row == len(grid)):
            return True
        
        # iterate through all the possible cell values in specified cell
        for x in cell_possibles[row][column]:
            
            grid[row][column] = x
            
            cell_possibles_copy = copy.deepcopy(cell_possibles)
            
            # remove value from all cell possibles in the same row, column and box
            is_cell_success = Solver.remove_num_cell(cell_possibles_copy, x, row, column)
            is_box_success = Solver.remove_num_box(cell_possibles_copy, x, row, column)
            
            # recursive call
            if (is_cell_success and is_box_success):
                if Solver.solve_helper(grid, cell_possibles_copy, row, column + 1):
                    return True
                    
        # DEBUG OUTPUT
        # print("False")
        return False

    # removes values from cells in accordance with the initial values of the grid
    @classmethod    
    def remove_initial_possibles(cls, grid, cell_possibles):

        grid_size = len(grid)
        
        # iterate through grid to find inital values
        for y in range(grid_size):
            for x in range(grid_size):
                
                # grid has initial value
                if grid[y][x] > 0:
                
                    # clear cell and insert initial value into possibles
                    cell_possibles[y][x].clear()
                    cell_possibles[y][x] = [grid[y][x]]
                    
                    # remove all possibles from cells with the same row and column
                    Solver.remove_num_cell(cell_possibles, grid[y][x], y, x)
                    
                    # remove all possibles from all cells contained in the box
                    Solver.remove_num_box(cell_possibles, grid[y][x], y, x)

    # remove value from possibles in the cells with the same row and column as the specified cell
    @classmethod    
    def remove_num_cell(cls, cell_possibles, num, row, column):
        
        grid_size = len(cell_possibles)
        
        # remove values from possibles in the same row
        for x in range(grid_size):
            
            # if value exists in possibles in cell (of the same row), remove it,
            #   except in the specified cell itself
            if (x != column):
                if num in cell_possibles[row][x]:
                    cell_possibles[row][x].remove(num)
                    
                    # if the cell in which the value is removed has no values,
                    #   return False -- this is not a solution
                    if len(cell_possibles[row][x]) == 0:
                        return False
        
        # remove values from possibles in the same column  
        for y in range(grid_size):
        
            # if value exists in possibles in cell (of the same column), remove it,
            #   except in the specified cell itself
            if (y != row):
                if num in cell_possibles[y][column]:
                    cell_possibles[y][column].remove(num)
                    
                    # if the cell in which the value is removed has no values,
                    #   return False -- this is not a solution                
                    if len(cell_possibles[y][column]) == 0:
                        return False
                        
        return True

    # removes all values from possibles for cells in the same box as the specified cell
    @classmethod    
    def remove_num_box(cls, cell_possibles, num, row, column):
        
        # determine which set to choose from, from the box dictionary
        id = Solver.box_dict_id[(row, column)]
        box_set = Solver.box_dict[id]

        # iterate through all cells in the same box and remove value from possibles
        #  except the specified cell itself
        for x in box_set:
            if (x[0] != row and x[1] != column):
                if num in cell_possibles[x[0]][x[1]]:
                    cell_possibles[x[0]][x[1]].remove(num)
                    
                    # if there is a cell in the same box with no values,
                    #   return False -- this is not a solution
                    if len(cell_possibles[x[0]][x[1]]) == 0:
                        return False
                        
        return True
