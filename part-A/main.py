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

    def countDirectMoves(self, dots):

        moves = 0;

        if (len(dots) == 0):
            return 0;

        for dot in dots:

            col = dot[0];
            row = dot[1];

            # col + 1
            if (self.getChar((col+1, row)) == '-'):
                moves += 1;
            # col - 1
            if (self.getChar((col-1, row)) == '-'):
                moves += 1;
            # row + 1
            if (self.getChar((col, row+1)) == '-'):
                moves += 1;
            # row - 1
            if (self.getChar((col, row-1)) == '-'):
                moves += 1;

        return moves;

    def count

if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();
    # blackDots = ba.getPosOfChar('@');
    whiteDots = ba.getPosOfChar('O')
    moves = 0
    if whiteDots != None:
        moves += ba.countDirectMoves(whiteDots);

    print(moves)
