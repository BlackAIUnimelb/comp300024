import random


def generateRandomBoard(command):

    seeds = ["O", "@", "-", "-"];

    board = [];

    boardSize = 8

    for i in range(0, boardSize):

        row = []

        for j in range(0, boardSize):

            # print(random.choice(seeds), end=" ")

            row.append(random.choice(seeds))

        board.append(row)


    board[0][0] = 'X';
    board[boardSize-1][0] = 'X';
    board[0][boardSize-1] = 'X';
    board[boardSize-1][boardSize-1] = 'X';


    for row in board:

        for col in row:

            print("{} ".format(col), end="")

        print()

    print(command)

if __name__ == '__main__':

    commands = ["Moves", "Massacre"];

    generateRandomBoard(random.choice(commands));
