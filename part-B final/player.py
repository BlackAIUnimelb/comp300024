#BlackAI version 2.0

from random import randint
import copy

class Player():
	def __init__(self, colour):
		self.ac_cnt = 0;
		self.up_cnt = 0;
		self.placingPhase = True;
		self.colour = colour;
		#initialising the board
		self.ba = BoardAnalyser();
		self.ba.createEmptyBoard();

		return;


	def action(self, turns):
		self.ac_cnt = self.ac_cnt + 1;
		if (self.ac_cnt > 12):
			self.placingPhase = False;

		#if it is in placing phase 
		if self.placingPhase:
			paction = self.placePiece();
			self.ba.placePiece(paction, self.colour);
			self.ba.updateBoard(self.colour);
			return paction;

		#if it is in moving phase
		else:
			if self.colour == 'white':
				opponentColour = 'black';
			elif self.colour == 'black':
				opponentColour = 'white';

			#For white player, shrink the board first before move
			if turns == 128:
				self.ba.first_shrink();
				self.ba.updateBoard(opponentColour);
			if turns == 192:
				self.ba.second_shrink();
				self.ba.updateBoard(opponentColour);

			#if there is no available moves, return None
			if self.checkIfCanMove(turns) == False:
				return None;

			paction = self.movePiece(turns);

			#update board
			startpos = paction[0];
			endpos = paction[1];
			self.ba.makeMove(startpos, endpos);
			self.ba.updateBoard(self.colour);

			#For black player, move first before shrink the board 
			if turns == 127:
				self.ba.first_shrink();
				self.ba.updateBoard(opponentColour);
			if turns == 191:
				self.ba.second_shrink();
				self.ba.updateBoard(opponentColour); 

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


	#helper functions
	#place a piece
	def placePiece(self):
		paction = ();
		#if there is an opponent's piece to be killed 
		eliminateBlackPosition = self.isOpponentKillable();
		if len(eliminateBlackPosition) == 0:
			#no black pieces to be eliminated
			allowedPositionsList = self.allowedPositions();

			#check for defense
			defensiveMove = self.defensivePlacePostion(allowedPositionsList);
			#if player needs to defense
			if len(defensiveMove) > 0:
				paction = (defensiveMove[0][0], defensiveMove[0][1]);
				return paction;
			else:
				#place a piece randomly 
				while(1):
					paction = self.randomPlace(allowedPositionsList);
					return paction;

		#if there is an opponent piece to be killed 
		else:
			#kill the piece
			paction = (eliminateBlackPosition[0][0], eliminateBlackPosition[0][1]);
			return paction;


	#in placing phase, check if there is an opponent piece that is killable 
	#retuen list
	def isOpponentKillable(self):
		isWhite = True;
		if self.colour == 'white':
			opponentSymbol = '@';
			selfSymbol = 'O';
			isWhite = True;
		elif self.colour == 'black':
			opponentSymbol = 'O';
			selfSymbol = '@';
			isWhite = False;

		opponentPieces = self.ba.getPosOfChar(opponentSymbol);
		if len(opponentPieces) == 0:
			return [];

		eliminateBlackPosition = [];

		for op in opponentPieces:
			col = op[0];
			row = op[1];

			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
			for i in range(0, 4):

				if (self.ba.isInsideBoardRange(directDots[i], 0) == False):
					continue;
				if self.ba.getChar(directDots[i]) == selfSymbol or self.ba.getChar(directDots[i]) == 'X':
					ind = (i + 2) % 4;
					if self.ba.isInsideBoardRange(directDots[ind], 0) and self.ba.getChar(directDots[ind]) == '-' and directDots[ind] not in eliminateBlackPosition:
						# check if valid 
						if (directDots[ind][1] <= 5 and isWhite) or (isWhite == False and directDots[ind][1] >= 2):
							eliminateBlackPosition.append(directDots[ind]);

		return eliminateBlackPosition;

    #in placing phase, there are position where player cannot place a piece
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

		#if there are opponent's pieces on the board
		if len(opponentPieces) > 0:
			for op in opponentPieces:
				col = op[0];
				row = op[1];
				notAllowedPositionList.append(op);

				directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
				nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
				for i in range(0, 4):

					if (self.ba.isInsideBoardRange(directDots[i], 0) == False):
						continue;
					if self.ba.getChar(directDots[i]) == '-' and self.ba.isInsideBoardRange(nextDirectDots[i], 0) and (self.ba.getChar(nextDirectDots[i]) == 'X' or self.ba.getChar(nextDirectDots[i]) == opponentSymbol or self.ba.getChar(nextDirectDots[i]) == '-'):
						if directDots[i] not in notAllowedPositionList:
							notAllowedPositionList.append(directDots[i]);

		selfPieces = self.ba.getPosOfChar(selfSymbol);
		if len(selfPieces) > 0:
			for sp in selfPieces:
				notAllowedPositionList.append(sp);

		return notAllowedPositionList;

	#in placing phase, return the allowed positions for player to place a piece
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

	# defensive move when player's piece is surrounded by opponent's pieces
	def defensivePlacePostion(self, allowedPositionsList):
		if self.colour == 'white':
			selfSymbol = 'O';
			opponentSymbol = '@';
		elif self.colour == 'black':
			selfSymbol = '@';
			opponentSymbol = 'O';

		defensiveMove = [];
		selfPieces = self.ba.getPosOfChar(selfSymbol);
		if len(selfPieces) == 0:
			return [];

		defensiveMove = [];

		for wp in selfPieces:
			col = wp[0];
			row = wp[1];

			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
			for i in range(0, 4):

				if (self.ba.isInsideBoardRange(directDots[i], 0) == False):
					continue;
				if self.ba.getChar(directDots[i]) == opponentSymbol:
					ind = (i + 2) % 4;
					if self.ba.isInsideBoardRange(directDots[ind], 0) and self.ba.getChar(directDots[ind]) == '-' and directDots[ind] in allowedPositionsList:
						defensiveMove.append(directDots[ind]);
						break;

		return defensiveMove;

	#place a piece randomly on board
	def randomPlace(self, allowedPositionsList):
		isWhite = True;
		if self.colour == 'white':
			isWhite = True;
		elif self.colour == 'black':
			isWhite = False;

		while(1):
			if isWhite:
				rand_col = randint(0, 7);
				rand_row = randint(2, 3);
			else:
				rand_col = randint(0, 7);
				rand_row = randint(4, 5);

			rand_pos = (rand_col, rand_row);
			if rand_pos in allowedPositionsList:
				paction = rand_pos;
				return paction;
			else:
				if isWhite:
					rand_row = 1;
				else:
					rand_row = 6;
				rand_pos = (rand_col, rand_row);
				if rand_pos in allowedPositionsList:
					paction = rand_pos;
					return paction;
				else:
					if isWhite:
						rand_row = 0;
					else:
						rand_row = 7;
					rand_pos = (rand_col, rand_row);
					if rand_pos in allowedPositionsList:
						paction = rand_pos;
						return paction;

	#Moving phase 
	#Minimax
	def movePiece(self, turns):
		depth = 3;
		player = self.colour;  #player colour
		value = 0;
		move = ();
		node = Node(self.ba, depth, player, value, player, turns, move);

		ab_prunning = AlphaBeta(node, depth);
		bestMove = ab_prunning.alpha_beta_prunning(node);

		return bestMove.move;

	#check if self pieces can move 
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


#search algorithm 
class AlphaBeta():
	def __init__(self, game_tree, depth):
		self.game_tree = game_tree;
		self.depth = depth;
		return;

	def alpha_beta_prunning(self, node):
		infinity = float('inf');
		bestVal = -infinity;
		beta = infinity;

		successors = self.getSuccessors(node);
		for child in successors:
			value = self.min_value(child, bestVal, beta, self.depth - 1)
			if value > bestVal:
				bestVal = value;
				bestState = child;
		return bestState;

	def max_value(self, node, alpha, beta, depth):
		if depth > 0:
			successors = self.getSuccessors(node);  #create children

		if self.isTerminal(node, depth):
			return self.getUtility(node)

		infinity = float('inf')
		value = -infinity;

		for child in successors:
			value = max(value, self.min_value(child, alpha, beta, depth - 1));
			if value >= beta:
				return value;
			alpha = max(alpha, value);
		return value;

	def min_value(self, node, alpha, beta, depth):
		if depth > 0:
			successors = self.getSuccessors(node);  #create children

		if self.isTerminal(node, depth):
			return self.getUtility(node)

		infinity = float('inf')
		value = infinity;

		for child in successors:
			value = min(value, self.max_value(child, alpha, beta, depth - 1));
			if value <= alpha:
				return value;
			beta = min(beta, value);
		return value;

	def getSuccessors(self, node):
		assert node is not None;
		node.createChildren();
		return node.children;

	def isTerminal(self, node, depth):
		assert node is not None;
		if depth == 0:
			return True;
		return len(node.children) == 0;

	def getUtility(self, node):
		assert node is not None;
		return node.value;


#calculate manhattan distance
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]);


#create children and calculate utility value
class Node():
    def __init__(self, ba, depth, player, value, rootPlayer, turns, move):
        self.depth = depth;
        self.board = ba;   #state
        self.player = player;
        self.value = value;
        self.rootPlayer = rootPlayer;
        self.turns = turns;
        self.move = move;
        self.children = [];


    def createChildren(self):

        if self.depth >= 0:
            isWhite = True;
            if self.player == 'white':
            	selfSymbol = 'O';
            	opponentSymbol = '@';
            	isWhite = True;
            	opponentColour = 'black';
            elif self.player == 'black':
            	selfSymbol = '@';
            	opponentSymbol = 'O';
            	isWhite = False;
            	opponentColour = 'white';

            selfPieces = self.board.getPosOfChar(selfSymbol);         #return all white pieces positions 
            if len(selfPieces) == 0:
            	return;
            for sp in selfPieces:
                col = sp[0];
                row = sp[1];

                directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
                nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
                for i in range(0,4):
                    if (self.board.isInsideBoardRange(directDots[i], self.turns) == False):
                        continue;

                    #check if can move directly
                    if (self.board.getChar(directDots[i]) == '-'):
                        newBoard = copy.deepcopy(self.board);
                        endPos = directDots[i];
                        newBoard.makeMove(sp, endPos);
                        newBoard.updateBoard(self.player);
                        move = (sp, endPos)
                        self.children.append(Node(newBoard, self.depth-1, opponentColour, self.getValue(newBoard, self.value, self.depth-1, self.rootPlayer), self.rootPlayer, self.turns+1, move));
                        continue;

                    #check if can jump
                    if (self.board.getChar(directDots[i]) == selfSymbol or self.board.getChar(directDots[i]) == opponentSymbol):
                        newBoard = copy.deepcopy(self.board);

                        if (self.board.isInsideBoardRange(nextDirectDots[i], self.turns) and self.board.getChar(nextDirectDots[i]) == '-'):
                            endPos = nextDirectDots[i];
                            newBoard.makeMove(sp, endPos);
                            newBoard.updateBoard(self.player);
                            move = (sp, endPos)
                            self.children.append(Node(newBoard, self.depth-1, opponentColour, self.getValue(newBoard, self.value, self.depth-1, self.rootPlayer), self.rootPlayer, self.turns+1, move));
                            continue;


    #evaluation function 
    def getValue(self, ba, value, depth, rootPlayer):

    	if depth > 0: 
    		return 0;
    	else: 
    		pvalue = 0;

    		if rootPlayer == 'white':
    			isWhite = True;
    			selfSymbol = 'O';
    			opponentSymbol = '@';
    		else:
    			isWhite = False;
    			selfSymbol = '@';
    			opponentSymbol = 'O';

    		#feature 1: 
    		#The number of player's pieces and the number of opponent's pieces
    		#weight: 10 and -99
    		selfPieces = ba.getPosOfChar(selfSymbol);
    		if len(selfPieces) > 0:
    			selfPiecesLeft = len(selfPieces);
    			#The more the number of player's pieces is, the bigger the value becomes.
    			num_of_selfPieces_weight = 10 * selfPiecesLeft;
    			pvalue += num_of_selfPieces_weight;

    		opponentPieces = ba.getPosOfChar(opponentSymbol);
    		if len(opponentPieces) > 0:
    			opponentPiecesLeft = len(opponentPieces);
    			#The more the number of opponent's pieces is, the less the value becomes. 
    			num_of_opponentPieces_weight = (-99) * opponentPiecesLeft;
    			pvalue += num_of_opponentPieces_weight;

    		#feature 2:
    		#The distance from each player's piece to the center of the board. 
    		dist = 0
    		for sp in selfPieces:
    			dist += manhattanDistance(sp, (3,3))
    		#The closer the pieces to the center is, the bigger the value becomes.
    		pvalue += (-1) * dist

    	return pvalue;


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
                    resultPos.append((x, y));

        return resultPos;

    #move a piece to a given position
    def makeMove(self, piece, destination):
        tmp_col = piece[0];
        tmp_row = piece[1];
        tmp_piece_type = self.board[tmp_col][tmp_row];

        self.board[tmp_col][tmp_row] = '-';
        self.board[destination[0]][destination[1]] = tmp_piece_type;


    #Update the board and check elimination
    def updateBoard(self, colour):
    	isWhite = True;
    	if colour == 'white':
    		isWhite = True;
    	elif colour == 'black':
    		isWhite = False;

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

    	return;

    #shrink the board when turns = 128
    def first_shrink(self):
    	for i in range(0, 8):
    		self.board[i][0] = '~';
    		self.board[i][7] = '~';
    		self.board[0][i] = '~';
    		self.board[7][i] = '~';
    	self.board[1][1] = 'X';
    	self.board[6][1] = 'X';
    	self.board[1][6] = 'X';
    	self.board[6][6] = 'X';

    	self.eliminate_when_shrink();

    #shrink the board when turns = 192
    def second_shrink(self):
    	for i in range(1, 7):
    		self.board[i][1] = '~';
    		self.board[i][6] = '~';
    		self.board[1][i] = '~';
    		self.board[6][i] = '~';
    	self.board[2][2] = 'X';
    	self.board[2][5] = 'X';
    	self.board[5][2] = 'X';
    	self.board[5][5] = 'X';

    	self.eliminate_when_shrink();

    def eliminate_when_shrink(self):
    	#cornor elimination
    	cornorPieces = []
    	cornors = self.getPosOfChar('X');
    	cornorPieces.append(cornors[0]);
    	cornorPieces.append(cornors[1]);
    	cornorPieces.append(cornors[3]);
    	cornorPieces.append(cornors[2]);
    	for cp in cornorPieces:
    		col = cp[0]
    		row = cp[1]

    		directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
    		nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
    		for i in range(0,4):
    			if (self.isInsideBoardRange(directDots[i], 0) == False):
    				continue;
    			if self.getChar(directDots[i]) == 'O' and self.getChar(nextDirectDots[i]) == '@':
    				self.board[directDots[i][0]][directDots[i][1]] = '-';
    			if self.getChar(directDots[i]) == '@' and self.getChar(nextDirectDots[i]) == 'O':
    				self.board[directDots[i][0]][directDots[i][1]] = '-';


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

