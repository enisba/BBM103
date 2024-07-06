import sys

# Here it opens the file and the L R's and U D's are listed separately in order
def txt_reader(direction, cells, coord_list, sorted_list):
    with open(sys.argv[1], "r") as txt:
        lines = txt.readlines()

    for line in lines[:4]:
        numbers = [int(i) for i in line.split()]
        direction.append(numbers)

    for cell_line in lines[4:]:
        cell = [str(j) for j in cell_line.split()]
        cells.append(cell)

    for i in range(len(cells)):
        for j in range(len(cells[i])):

            if cells[i][j] == "L" and j + 1 < len(cells[i]) and cells[i][j + 1] == "R":
                sorted_list.append(["L", "R"])
                coord_list.append([[i, j], [i, j + 1]])

            if cells[i][j] == "U" and i + 1 < len(cells) and cells[i + 1][j] == "D":
                sorted_list.append(["U", "D"])
                coord_list.append([[i, j], [i + 1, j]])

# Here is a backtracking with recursion logic
def solver_valley(sorted_list, direction, dot, coord_list, cells):

    if dot >= len(sorted_list):
        return constraints_row_col(direction, cells)
    # H B control
    sorted_list[dot][0] = "H"
    sorted_list[dot][1] = "B"

    # backtracking
    if not check_around(sorted_list, coord_list, dot, cells) or not solver_valley(sorted_list, direction, dot + 1, coord_list, cells):
        # B H control
        sorted_list[dot][0] = "B"
        sorted_list[dot][1] = "H"

        # backtracking
        if (not check_around(sorted_list, coord_list, dot, cells) or
                not solver_valley(sorted_list, direction, dot + 1, coord_list, cells)):
            # N N control
            sorted_list[dot][0] = "N"
            sorted_list[dot][1] = "N"
            # Returns False if the above conditions are not met
            if not solver_valley(sorted_list, direction, dot + 1, coord_list, cells):
                return False

    return True

# Controls neighboring cells
def check_around(sorted_list, coord_list, dot, cells):

    for i in range(len(coord_list)):
        cells[coord_list[i][0][0]][coord_list[i][0][1]] = sorted_list[i][0]
        cells[coord_list[i][1][0]][coord_list[i][1][1]] = sorted_list[i][1]

    for i in range(2):
        row, col = coord_list[dot][i][0], coord_list[dot][i][1]

        # left cell control
        if 0 <= row - 1 and cells[row][col] == cells[row - 1][col] :
            return False

        # down cell control
        elif col + 1 < len(cells[row]) and cells[row][col] == cells[row][col + 1] :
            return False

        # up cell control
        elif 0 <= col - 1 and cells[row][col] == cells[row][col - 1] :
            return False

    return True

# function that checks how many B H in row and column
def constraints_row_col(direction, cells):

    # row of H
    for l in range(len(direction[0])):
        h_row = cells[l].count("H")
        if direction[0][l] != -1 and direction[0][l] != h_row:
            return False
        # row of B
        b_row = cells[l].count("B")
        if direction[1][l] != -1 and direction[1][l] != b_row:
            return False
    # column of H
    for l in range(len(direction[2])):
        h_col = [cells[r][l] for r in range(len(cells))].count("H")
        if direction[2][l] != -1 and direction[2][l] != h_col:
            return False
        # column of B
        b_col = [cells[r][l] for r in range(len(cells))].count("B")
        if direction[3][l] != -1 and direction[3][l] != b_col:
            return False

    return True

# Where Everything is called and the Code works
def main():
    direction = []
    cells = []
    sorted_list = []
    coord_list = []
    dot = 0

    txt_reader(direction, cells, coord_list, sorted_list)

    # code acceleration process
    solved = solver_valley(sorted_list, direction, dot, coord_list, cells)

    # file printing
    with open(sys.argv[2], "w") as txt_writer:
        if solved:
            for i,row in enumerate(cells):
                if i < len(cells) - 1:
                    txt_writer.write(' '.join(row) + '\n')
                else:
                    txt_writer.write(' '.join(row))
        else: txt_writer.write('No solution!')

if __name__ == "__main__":
    main()












