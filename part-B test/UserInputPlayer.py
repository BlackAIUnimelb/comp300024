from random import randint
import copy

class Player():
	def __init__(self, colour):
		self.cnt = 0;
		self.placingPhase = True;
		self.colour = colour;

		self.ba = BoardAnalyser();
		self.ba.createEmptyBoard();
		return;


	def action(self, turns):
		# print("Board view " + self.colour)
		# outputBoard(self.ba.board);

		self.cnt = self.cnt + 1;
		if (self.cnt > 12):
			self.placingPhase = False;

		paction = None;
		if self.placingPhase:
			pos = input("Placing Phase Black Player:");
			# tmplist = ();
			pos = pos.split();
			a = int(float(pos[0]));
			b = int(float(pos[1]));
			paction = (a ,b);
		else:
			pos = input("Moving Phase Black Player:");
			# tmplist = ();
			pos = pos.split();
			a = int(float(pos[0]));
			b = int(float(pos[1]));
			c = int(float(pos[2]));
			d = int(float(pos[3]));
			paction = ((a ,b), (c, d));

		self.ba.placePiece(paction, self.colour);
		self.ba.updateBoard(self.colour);
		return paction;


	def update(self, actions):
		if self.colour == 'white':
			opponentColour = 'black';
		elif self.colour == 'black':
			opponentColour = 'white';

		self.ba.placePiece(actions, opponentColour);
		self.ba.updateBoard(opponentColour);
		return;

	def notAllowedPosition(self):
		isWhite = True;
		if self.colour == 'white':
			isWhite = True;
			opponentSymbol = '@';
			selfSymbol = 'O';
		elif self.colour == 'black':
			isWhite = False;
			opponentSymbol = 'O';
			selfSymbol = '@';

		notAllowedPositionList = [];
		#对白棋来说，最下面两行不可以place
		if isWhite:
			for i in range(6, 8):
				for j in range(0, 8):
					notAllowedPositionList.append((j,i));
			notAllowedPositionList.append((0, 0));
			notAllowedPositionList.append((7 ,0));
		else:
			for i in range(0, 2):
				for j in range(0, 8):
					notAllowedPositionList.append((j,i));
			notAllowedPositionList.append((0, 7));
			notAllowedPositionList.append((7 ,7));

		opponentPieces = self.ba.getPosOfChar(opponentSymbol);
		if len(opponentPieces) > 0:
			for op in opponentPieces:
				notAllowedPositionList.append(op);


		selfPieces = self.ba.getPosOfChar(selfSymbol);
		if len(selfPieces) > 0:
			for sp in selfPieces:
				notAllowedPositionList.append(sp);

		return notAllowedPositionList;

	#in placing phase, return the allowed positions for white pieces to place 
	def allowedPositions(self):
		notAllowedPositionList = self.notAllowedPosition();
		allowedPositionsList = [];

		for i in range(0, 8):
			for j in range(0, 8):
				if (i ,j) in notAllowedPositionList:
					continue;
				else:
					allowedPositionsList.append((i, j));

		return allowedPositionsList;




#Board analyser
class BoardAnalyser():

    def __init__(self):
        self.board = None;
        self.command = None;
        self.chars = ['-', 'X', 'O', '@'];

    def createEmptyBoard(self):
    	self.board = [
    		['X','-','-','-','-','-','-','X'],
    		['-','-','-','-','-','-','-','-'],
    		['-','-','-','-','-','-','-','-'],
    		['-','-','-','-','-','-','-','-'],
    		['-','-','-','-','-','-','-','-'],
    		['-','-','-','-','-','-','-','-'],
    		['-','-','-','-','-','-','-','-'],
    		['X','-','-','-','-','-','-','X']
    	];

    def getChar(self, pos):
        if (pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0):
            return '';

        pos_x = pos[0];
        pos_y = pos[1];
        o = self.board[pos_x][pos_y];
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
                    resultPos.append((x, y));

        return resultPos;


    #move a piece to a given position
    def makeMove(self, piece, destination):
        tmp_col = piece[0];
        tmp_row = piece[1];
        tmp_piece_type = self.board[tmp_col][tmp_row];

        self.board[tmp_col][tmp_row] = '-';
        self.board[destination[0]][destination[1]] = tmp_piece_type;

        # self.updateBoard();

    #check if black pieces being eliminated
    def updateBoard(self, colour):
    	isWhite = True;
    	if colour == 'white':
    		isWhite = True;
    	elif colour == 'black':
    		isWhite = False;

    	# board = copy.deepcopy(self.board);
    	blackPieces = self.getPosOfChar('@');
    	whitePieces = self.getPosOfChar('O');
    	if isWhite:
    		#eliminate black pieces
    		for bp in blackPieces:
    			col = bp[0];
    			row = bp[1];

    			left_right = [(col, row-1), (col, row+1)];
    			up_down = [(col-1, row), (col+1, row)];

    			if left_right[0][1] >=0 and left_right[1][1] <= 7:
    				if (self.getChar(left_right[0]) == 'O' and self.getChar(left_right[1]) == 'O') or (self.getChar(left_right[0]) == 'O' and self.getChar(left_right[1]) == 'X') or (self.getChar(left_right[0]) == 'X' and self.getChar(left_right[1]) == 'O'):
    					self.board[col][row] = '-';
    			if up_down[0][0] >= 0 and up_down[1][0] <= 7:
    				if (self.getChar(up_down[0]) == 'O' and self.getChar(up_down[1]) == 'O') or (self.getChar(up_down[0]) == 'O' and self.getChar(up_down[1]) == 'X') or ((self.getChar(up_down[0]) == 'X' and self.getChar(up_down[1]) == 'O')):
    					self.board[col][row] = '-';
    		#eliminate white pieces 
    		for wp in whitePieces:
    			col = wp[0];
    			row = wp[1];

    			left_right = [(col, row-1), (col, row+1)];
    			up_down = [(col-1, row), (col+1, row)];

    			if left_right[0][1] >=0 and left_right[1][1] <= 7:
    				if (self.getChar(left_right[0]) == '@' and self.getChar(left_right[1]) == '@') or (self.getChar(left_right[0]) == '@' and self.getChar(left_right[1]) == 'X') or (self.getChar(left_right[0]) == 'X' and self.getChar(left_right[1]) == '@'):
    					self.board[col][row] = '-';
    			if up_down[0][0] >= 0 and up_down[1][0] <= 7:
    				if (self.getChar(up_down[0]) == '@' and self.getChar(up_down[1]) == '@') or (self.getChar(up_down[0]) == '@' and self.getChar(up_down[1]) == 'X') or ((self.getChar(up_down[0]) == 'X' and self.getChar(up_down[1]) == '@')):
    					self.board[col][row] = '-';
    	else:
    		for wp in whitePieces:
    			col = wp[0];
    			row = wp[1];

    			left_right = [(col, row-1), (col, row+1)];
    			up_down = [(col-1, row), (col+1, row)];

    			if left_right[0][1] >=0 and left_right[1][1] <= 7:
    				if (self.getChar(left_right[0]) == '@' and self.getChar(left_right[1]) == '@') or (self.getChar(left_right[0]) == '@' and self.getChar(left_right[1]) == 'X') or (self.getChar(left_right[0]) == 'X' and self.getChar(left_right[1]) == '@'):
    					self.board[col][row] = '-';
    			if up_down[0][0] >= 0 and up_down[1][0] <= 7:
    				if (self.getChar(up_down[0]) == '@' and self.getChar(up_down[1]) == '@') or (self.getChar(up_down[0]) == '@' and self.getChar(up_down[1]) == 'X') or ((self.getChar(up_down[0]) == 'X' and self.getChar(up_down[1]) == '@')):
    					self.board[col][row] = '-';
    		for bp in blackPieces:
    			col = bp[0];
    			row = bp[1];

    			left_right = [(col, row-1), (col, row+1)];
    			up_down = [(col-1, row), (col+1, row)];

    			if left_right[0][1] >=0 and left_right[1][1] <= 7:
    				if (self.getChar(left_right[0]) == 'O' and self.getChar(left_right[1]) == 'O') or (self.getChar(left_right[0]) == 'O' and self.getChar(left_right[1]) == 'X') or (self.getChar(left_right[0]) == 'X' and self.getChar(left_right[1]) == 'O'):
    					self.board[col][row] = '-';
    			if up_down[0][0] >= 0 and up_down[1][0] <= 7:
    				if (self.getChar(up_down[0]) == 'O' and self.getChar(up_down[1]) == 'O') or (self.getChar(up_down[0]) == 'O' and self.getChar(up_down[1]) == 'X') or ((self.getChar(up_down[0]) == 'X' and self.getChar(up_down[1]) == 'O')):
    					self.board[col][row] = '-';

    		# self.board = copy.deepcopy(board);
    	return;

    def placePiece(self, destination, colour):
    	if colour == 'white':
    		self.board[destination[0]][destination[1]] = 'O';
    	elif colour == 'black':
    		self.board[destination[0]][destination[1]] = '@';


    #check if the given position is out of the board
    def isInsideBoardRange(self, pos):
    	if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
    		return False;
    	else:
    		return True;


def outputBoard(board):

    # for row in board:
    for row in zip(*board):

        for col in row:

            print("{} ".format(col), end="")

        print()

    print()