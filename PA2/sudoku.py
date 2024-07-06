import sys

# helps the sudoku while print the putput file
def print_sudoku(grid):
    out_str = ""
    for line1 in range(9):
        for line2 in range(8):
            out_str += str(grid[line1][line2]) + " "
        out_str += str(grid[line1][8])
        out_str += "\n"
    return out_str

# Check sudoku if cells are empty or not
def check_sudoku(grid, row, col, num):
    # Check every columns in the sudoku
    for k in range(9):
        if grid[k][col] == num:
            return False
    # Check every rows in the sudoku
    for l in range (9):
        if grid[row][l] == num:
            return False

    #Check every 3x3 cells in the sudoku
    row_start = row - row % 3
    column_start = col - col % 3

    for x in range(3):
        for y in range(3):
            if grid[x + row_start][y + column_start] == num:
                return False
    return True

# This function solves the sudoku
def sudoku_solver(grid, counter, out_str):
    # Calls check_sudoku function, checks every cols and rows zero or not and adds it is number to the list
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                liste = []
                for num in range(1, 10):
                    if check_sudoku(grid, row, col, num): liste.append(num)

                # Every list may not contain one value so adds "if" for this situation checks if one value writes the output next step
                # out_str it will work when creates the output file
                if len(liste) == 1:
                    grid[row][col] = liste[0]
                    out_str += 18 * "-" + "\n"
                    out_str += f"Step {counter} - {liste[0]} @ R{row + 1}C{col + 1}\n"
                    out_str += 18 * "-" + "\n"
                    out_str += print_sudoku(grid)
                    # every step increasing 1 step
                    counter += 1
                    # Uses Recursion function so that the function can return
                    sudoku_outcome = sudoku_solver(grid, counter, out_str)
                    # if sudoku_output[0] goes true sudoku is solved and goes the sudoku_solved[1] and writes 18 dash
                    if sudoku_outcome[0]:
                        return True, sudoku_outcome[1]
                else: continue
    # Last step add 18 dash
    return True, out_str + 18 * "-"

# main function calls input file and output_file and write in output_file the out_str we called before in sudoku_solver
def main():
    input_file = open(sys.argv[1], "r")
    # Defines a grid
    grid = []

    # Creates a grid by processing lines read from a input_file
    for line in input_file:
        row = [int(num) for num in line.split()]
        grid.append(row)

    # writes output_file in the solution of the sudoku step by step
    output_file = open(sys.argv[2], "w")
    output_file.write(sudoku_solver(grid, 1, "")[1])

    # Close the input and output file
    input_file.close()
    output_file.flush()
    output_file.close()

# Calls main function
if __name__ == "__main__":
    main()