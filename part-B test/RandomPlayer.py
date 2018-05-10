from random import randint
import copy

class Player():
	def __init__(self, colour):
		self.ac_cnt = 0;
		self.up_cnt = 0;
		self.placingPhase = True;
		self.colour = colour;

		self.ba = BoardAnalyser();
		self.ba.createEmptyBoard();


	def action(self, turns):
		self.ac_cnt = self.ac_cnt + 1;
		if (self.ac_cnt > 12):
			self.placingPhase = False;

		paction = None;

		if self.placingPhase:
			# outputBoard(self.ba.board);
			allowedPositionsList = self.allowedPositions(True);
			while(1):
				rand_col = randint(0, 7);
				rand_row = randint(0, 7);
				rand_pos = (rand_col, rand_row);
				if rand_pos in allowedPositionsList:
					paction = rand_pos;
					self.ba.placePiece(paction, self.colour);
					self.ba.updateBoard(self.colour);
					return paction;
			
		else:#moving phase
			if turns == 128 or turns == 127:
				self.ba.first_shrink();
				self.ba.updateBoard(self.colour);
			if turns == 192 or turns == 191:
				self.ba.second_shrink();
				self.ba.updateBoard(self.colour); 

			allowedPositionsList = self.allowedPositions(False);
			startpos = ()
			endpos = ()

			if self.colour == 'white':
				selfSymbol = 'O';
			else:
				selfSymbol = '@';

			if self.checkIfCanMove(turns) == False:
					return None;
			print("board view " + self.colour)
			outputBoard(self.ba.board)

			while(1):
				selfPieces = self.ba.getPosOfChar(selfSymbol);
				randindex = randint(0, len(selfPieces)-1);
				startpos = selfPieces[randindex];

				moveList = self.randomMove(startpos, turns);
				if len(moveList) == 0:
					continue;
				else:
					randindex = randint(0, len(moveList)-1);
					endpos = moveList[randindex];
					break;

			self.ba.makeMove(startpos, endpos);
			self.ba.updateBoard(self.colour);

			return (startpos, endpos);


		return paction;


	def update(self, actions):
		self.up_cnt += 1;
		if self.up_cnt > 12:
			self.placingPhase = False;

		if self.colour == 'white':
			opponentColour = 'black';
		elif self.colour == 'black':
			opponentColour = 'white';

		if actions is None:
			return;

		if self.placingPhase:
			self.ba.placePiece(actions, opponentColour);
		else:
			self.ba.makeMove(actions[0], actions[1]);


		self.ba.updateBoard(opponentColour);
		return;



	def notAllowedPosition(self, isPlacingPhase):
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
		if isPlacingPhase:
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
		else:# moving phase
			notAllowedPositionList.append((0, 0));
			notAllowedPositionList.append((7 ,0));
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
	def allowedPositions(self, isPlacingPhase):
		notAllowedPositionList = self.notAllowedPosition(isPlacingPhase);
		allowedPositionsList = [];

		for i in range(0, 8):
			for j in range(0, 8):
				if (i ,j) in notAllowedPositionList:
					continue;
				else:
					allowedPositionsList.append((i, j));

		return allowedPositionsList;

	def randomMove(self, pos, turns):
		moveList = [];

		col = pos[0];
		row = pos[1];
		directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
		nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
		for i in range(0,4):
			#边界情况
			if (self.ba.isInsideBoardRange(directDots[i], turns) == False):
				continue;

			#check if can move directly
			if (self.ba.getChar(directDots[i]) == '-'):
				moveList.append(directDots[i]);
				continue;

			#check if can jump
			if (self.ba.getChar(directDots[i]) == 'O' or self.ba.getChar(directDots[i]) == '@'):

				if (self.ba.isInsideBoardRange(nextDirectDots[i], turns) and self.ba.getChar(nextDirectDots[i]) == '-'):
					endPos = nextDirectDots[i];
					moveList.append(endPos);
					continue;

		return moveList;

	def checkIfCanMove(self, turns):
		if self.colour == 'white':
			opponentSymbol = '@';
			selfSymbol = 'O';
			isWhite = True;
		elif self.colour == 'black':
			opponentSymbol = 'O';
			selfSymbol = '@';
			isWhite = False;

		availableMoveList = []

		selfPieces = self.ba.getPosOfChar(selfSymbol);
		for sp in selfPieces:
			col = sp[0];
			row = sp[1];

			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
			nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
			for i in range(0,4):
				#边界情况
				if (self.ba.isInsideBoardRange(directDots[i], turns) == False):
					continue;

				#check if can move directly
				if (self.ba.getChar(directDots[i]) == '-'):
					availableMoveList.append(directDots[i]);
					continue;
				#check if can jump
				if (self.ba.getChar(directDots[i]) == 'O' or self.ba.getChar(directDots[i]) == '@'):

					if (self.ba.isInsideBoardRange(nextDirectDots[i], turns) and self.ba.getChar(nextDirectDots[i]) == '-'):
						endPos = nextDirectDots[i];
						availableMoveList.append(endPos);
						continue;

					
		if len(availableMoveList) == 0:
			return False;
		else:
			return True;

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

    def first_shrink(self):
    	for i in range(0, 8):
    		#最上行和最下行为空
    		self.board[i][0] = '~';
    		self.board[i][7] = '~';
    		#最左行和最右行为空
    		self.board[0][i] = '~';
    		self.board[7][i] = '~';
    	self.board[1][1] = 'X';
    	self.board[6][1] = 'X';
    	self.board[1][6] = 'X';
    	self.board[6][6] = 'X';

    def second_shrink(self):
    	for i in range(1, 7):
    		#最上行和最下行为空
    		self.board[i][1] = '~';
    		self.board[i][6] = '~';
    		#最左行和最右行为空
    		self.board[1][i] = '~';
    		self.board[6][i] = '~';
    	self.board[2][2] = 'X';
    	self.board[2][5] = 'X';
    	self.board[5][2] = 'X';
    	self.board[5][5] = 'X';

    def placePiece(self, destination, colour):
    	if colour == 'white':
    		self.board[destination[0]][destination[1]] = 'O';
    	elif colour == 'black':
    		self.board[destination[0]][destination[1]] = '@';


    #check if the given position is out of the board
    def isInsideBoardRange(self, pos, turns):
        if turns < 128:
            if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                return False;
            else:
                return True;
        elif turns >= 128 and turns < 192:
            if pos[0] < 1 or pos[0] > 6 or pos[1] < 1 or pos[1] > 6:
                return False;
            else:
                return True;
        elif turns >= 192:
            if pos[0] < 2 or pos[0] > 5 or pos[1] < 2 or pos[1] > 5:
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