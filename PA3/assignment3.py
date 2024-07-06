import sys

# global variables
board_reader = []
input_cell = []
score = 0

def create_list():
    global board_reader
    # create a list in the list
    input_file = open(sys.argv[1], "r")
    list_board = input_file.read().split("\n")
    for listing in list_board:
        board_reader.append([int(i) for i in listing.split()])
    for rows in board_reader:
        for board in rows:
            print(board, end=" ")
        print()
    # prints the starting score on the screen
    print()
    print(f"Your score is: {score}")
    print()

def col_and_row():
    global input_cell, board_reader

    # determines the number of columns and rows
    number_of_rows = len(board_reader)
    number_of_columns = len(board_reader[0])

    # create a list for given row and column
    input_cell = input("Please enter a row and column number: ")
    print()
    input_cell = [int(num) for num in input_cell.split()]

    if 0 < input_cell[0] <= number_of_rows and 0 < input_cell[1] <= number_of_columns:
        if (
            # checks to the left for mistakes
            input_cell[1]  < number_of_columns and
            board_reader[input_cell[0] - 1][input_cell[1] - 1] == board_reader[input_cell[0] - 1][input_cell[1]] or

            # checks to the right for mistakes
            input_cell[1] - 2 >= 0 and
            board_reader[input_cell[0] - 1][input_cell[1] - 1] == board_reader[input_cell[0] - 1][input_cell[1] - 2] or

            # checks to the down for mistakes
            input_cell[0] < number_of_rows and
            board_reader[input_cell[0] - 1][input_cell[1] - 1] == board_reader[input_cell[0]][input_cell[1] - 1] or

            # checks to the up for mistakes
            input_cell[0] - 2 >= 0 and
            board_reader[input_cell[0] - 1][input_cell[1] - 1] == board_reader[input_cell[0] - 2][input_cell[1] - 1]
        ):
            game_basis()
            return True

        # error if the movement does not occur
        else:
            print("No movement happened, try again!")
            print()
            for rows in board_reader:
                for board in rows:
                    print(board, end=" ")
                print()
            print()
            print(f"Your score is: {score}")
            print()

            col_and_row()
    # error if correct numbers are not given
    else:
        print("Please enter a correct size! ")
        print()
        col_and_row()

# function that makes numbers fall down
def lean_down():
    global board_reader

    # shifting places by checking the numbers above and below
    for i in range(len(board_reader) - 1):
        for j in range(len(board_reader[i])):
            if board_reader[i + 1][j] == " " and board_reader[i][j] != " ":
                board_reader[i][j], board_reader[i + 1][j] = board_reader[i + 1][j], board_reader[i][j]
                lean_down()
                return None

# check_cell and game_basis check the neighborhood of the selected number and continue to do so if the same number exists
def check_cell(row, col, num):
    global input_cell, board_reader, score

    number_of_rows = len(board_reader)
    number_of_columns = len(board_reader[0])


    check_near = [[0, 1], [0, -1], [1, 0], [-1, 0]]


    for dir in check_near:
        if (0 <= col + dir[1] < number_of_columns and 0 <= row + dir[0] < number_of_rows and
                board_reader[row + dir[0]][col + dir[1]] == num):
            score += int(num)
            board_reader[row + dir[0]][col + dir[1]] = " "
            check_cell(row + dir[0], col + dir[1], num)

def game_basis():
    global input_cell, board_reader, score

    row = input_cell[0] - 1
    col = input_cell[1] - 1

    check_all()

    # calls recursive for check_cell()
    if board_reader[row][col] != " ":
        score += int(board_reader[row][col])
        num = board_reader[row][col]
        board_reader[row][col] = " "

        check_cell(row, col, num)
    else:
        print("No movement happened, try again!")
        print()

    # swipe left
    lean_left()
    # swipe down
    lean_down()
    # swipe up
    lean_row()
    # if necessary, if the line has shifted upwards, lower the numbers down again one by one
    lean_down()

    # prints board and score on the screen
    for rows in board_reader:
        for board in range(len(rows) - 1):
            print(rows[board], end=" ")
        print(str(rows[len(rows) - 1]))
    print()
    print(f"Your score is: {score}")
    print()

    # call game_over if the game is over
    game_over()
    col_and_row()

# makes the numbers shift to the left if any column is empty
def lean_left():
    global board_reader

    for col in range(len(board_reader[0])):
        empty_columns = all(board_reader[row][col] == " " for row in range(len(board_reader)))
        if empty_columns:
            for row in range(len(board_reader)):
                board_reader[row].pop(col)

            lean_left()
            return None

# makes the numbers scroll up if any line is empty
def lean_row():
    global board_reader

    for row in range(len(board_reader)):
        empty_rows = all(board_reader[row][col] == " " for col in range(len(board_reader[row])))
        if empty_rows:
            if row != len(board_reader) - 1:
                board_reader.pop(row)

                lean_row()
            return None

# if there is no number to the right or left of any number, or the same number above or below it, the game is over.
def game_over():
    global board_reader, input_cell

    number_of_rows = len(board_reader)
    number_of_columns = len(board_reader[0])

    canplay = False

    for i in range(number_of_rows):
        for j in range(number_of_columns):
            # checks every neighbor cell is it same or not if not, print "game_over" on the screen
            if board_reader[i][j] != " ":
                if j != number_of_columns - 1 and board_reader[i][j] == board_reader[i][j + 1]: canplay = True
                if j != 0 and board_reader[i][j] == board_reader[i][j - 1]: canplay = True
                if i != number_of_rows - 1 and board_reader[i][j] == board_reader[i + 1][j]: canplay = True
                if i != 0 and board_reader[i][j] == board_reader[i - 1][j]: canplay = True

    if not canplay:
        print("Game Over")
        exit()

# function to be used if there are no numbers left in the list when we explode the number
def check_all():
    global board_reader

    num = board_reader[0][0]

    for i in board_reader:
        for j in i:
            if j != num: return None

    print("Game Over")
    exit()

# executes the main function and the game is playable
def main():
    create_list()
    col_and_row()
    game_basis()
    game_over()

if __name__ == "__main__": main()