from queue import PriorityQueue

class BoardAnalyser():

    def __init__(self):
        self.board = None;
        self.goal = None;
        self.chars = ['-', 'X', 'O', '@'];

    def formatInput(self):

        self.board = [];
        # Read board
        for i in range(0, 8):
            content = input();
            self.board.append(content.split());

        self.goal = input();

        return True;

    def getChar(self, pos):

        if (pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0):
            return '';

        pos_y = pos[0];
        pos_x = pos[1];
        o = self.board[pos_x][pos_y];

        object_dict = {
        	"X" : "conner",
        	"O" : "white",
        	"@" : "black",
        	"-" : "space",
        }

        return o;

    # Returns all coordinates of CHAR
    def getPosOfChar(self, char, boardSize = 8):

        resultPos = [];
        # 4 types of char: - X O @
        if char not in self.chars:
            return None;

        for x in range(0, boardSize):

            for y in range(0, boardSize):

                if char == self.board[x][y]:
                    # (col, row)
                    resultPos.append((y,x));

        return resultPos;

    def countMoves(self, dots):

        total_moves = 0;

        if (len(dots) == 0):
            return 0;

        # Counts direct moves
        for dot in dots:

            col = dot[0];
            row = dot[1];
            # col + 1
            # col - 1
            # row + 1
            # row - 1
            directDots = [(col+1, row), (col-1, row), (col, row+1), (col, row-1)];

            for i in range(0, 4):

                if (self.getChar(directDots[i]) == '-'):
                    total_moves += 1;

                if (self.getChar(directDots[i]) == 'O' or self.getChar(directDots[i]) == '@'):

                    ccol = directDots[i][0];
                    rrow = directDots[i][1];

                    # Up
                    if (i == 0 and self.getChar((ccol + 1, rrow)) == '-'):
                        total_moves += 1;
                        continue;

                    # Down
                    if (i == 1 and self.getChar((ccol - 1, rrow)) == '-'):
                        total_moves += 1;
                        continue;

                    # Right
                    if (i == 2 and self.getChar((ccol, rrow + 1)) == '-'):
                        total_moves += 1;
                        continue;

                    # Left
                    if (i == 3 and self.getChar((ccol, rrow - 1)) == '-'):
                        total_moves += 1;
                        continue;

        return total_moves;

    def printWBMoves(self):

        whiteDots = self.getPosOfChar('O');
        blackDots = self.getPosOfChar('@');
        print(self.countMoves(whiteDots));
        print(self.countMoves(blackDots));


    def sortBlackDotsList(self, blackDots, whiteDots):
        pq = PriorityQueue();
        for blackDot in blackDots:
            priority = self.whiteDotsToABlackDot(blackDot, whiteDots);
            pq.put([priority, blackDot]);
        return pq; #黑棋被eliminate的顺序

    def whiteDotsToABlackDot(self, blackDot, whiteDots):
        if (len(whiteDots) == 0):
            return -1;

        sumdist = 0
        for whiteDot in whiteDots:
            colW = whiteDot[0];
            rowW = whiteDot[1];

            sumdist += abs(colW - blackDot[0]) + abs(rowW - blackDot[1]);
        return sumdist;


if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();
    ba.printWBMoves();
