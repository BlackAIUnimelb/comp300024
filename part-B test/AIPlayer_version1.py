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

			#对于白棋来说，先shrink board，再走
			if turns == 128:
				self.ba.first_shrink();
				self.ba.updateBoard(opponentColour);
			if turns == 192:
				self.ba.second_shrink();
				self.ba.updateBoard(opponentColour);   #先后顺序？


			if self.checkIfCanMove(turns) == False:
				return None;

			print("board view " + self.colour)
			outputBoard(self.ba.board)
			paction = self.movePiece(turns);

			print(paction)
			#update board
			startpos = paction[0];
			endpos = paction[1];
			self.ba.makeMove(startpos, endpos);
			self.ba.updateBoard(self.colour);


			#对于黑棋来说, 走完以后 shrink board
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
		eliminateBlackPosition = self.isOpponentKillable();
		if len(eliminateBlackPosition) == 0:
			#no black pieces to be eliminated
			#防守
			allowedPositionsList = self.allowedPositions();

			#check for defense
			defensiveMove = self.defensivePlacePostion(allowedPositionsList);
			#如果需要 defensive move的话
			if len(defensiveMove) > 0:
				paction = (defensiveMove[0][0], defensiveMove[0][1]);
				return paction;
			else:
				#如果不需要defense
				#随意place??
				while(1):
					paction = self.randomPlace(allowedPositionsList);
					return paction;

		#if there is an opponent piece to be killed 
		else:
			#假设 len(eliminateBlackPosition) 最大就是 1
			paction = (eliminateBlackPosition[0][0], eliminateBlackPosition[0][1]);
			return paction;


	#in placing phase, check if there is a black piece that is killable 
	#return list
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
				#边界情况
				if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
					continue;
				if self.ba.getChar(directDots[i]) == selfSymbol or self.ba.getChar(directDots[i]) == 'X':
					ind = (i + 2) % 4;
					if self.ba.isInsideBoardRange(directDots[ind], 0) and self.ba.getChar(directDots[ind]) == '-' and directDots[ind] not in eliminateBlackPosition:
						# 白棋只能放在第5行及以上
						if (directDots[ind][1] <= 5 and isWhite) or (isWhite == False and directDots[ind][1] >= 2):
							eliminateBlackPosition.append(directDots[ind]);

		return eliminateBlackPosition;

    #in placing phase, there are position where white pieces cannot place
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

		#if there are black pieces on the board
		if len(opponentPieces) > 0:
			for op in opponentPieces:
				col = op[0];
				row = op[1];
				notAllowedPositionList.append(op);

				#黑棋的4个方向
				directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
				nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
				for i in range(0, 4):
					#边界情况
					if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
						continue;

					if self.ba.getChar(directDots[i]) == '-' and self.ba.isInsideBoardRange(nextDirectDots[i], 0) and (self.ba.getChar(nextDirectDots[i]) == 'X' or self.ba.getChar(nextDirectDots[i]) == opponentSymbol or self.ba.getChar(nextDirectDots[i]) == '-'):
						if directDots[i] not in notAllowedPositionList:
							notAllowedPositionList.append(directDots[i]);

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

	# defensive move when white piece is surrounded by black piece
	# limitations:
	# 1. 当对面给我设置陷阱的时候
	# 2. 当虽然被包围，但是不需要defense的时候( 对面不可以摆在上两行，或者下两行 )
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

			#白棋的4个方向
			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
			for i in range(0, 4):
				#边界情况
				if (self.ba.isInsideBoardRange(directDots[i], 0) == False):
					continue;
				if self.ba.getChar(directDots[i]) == opponentSymbol:
					ind = (i + 2) % 4;
					if self.ba.isInsideBoardRange(directDots[ind], 0) and self.ba.getChar(directDots[ind]) == '-' and directDots[ind] in allowedPositionsList:
						defensiveMove.append(directDots[ind]);
						break;

		#假设整个棋盘上只有一个字要去defense
		return defensiveMove;

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

		# miniMax = MiniMax(node, depth);
		# bestMove = miniMax.minimax(node);
		ab_prunning = AlphaBeta(node, depth);
		bestMove = ab_prunning.alpha_beta_prunning(node);


		# if self.colour == 'white':
		# 	selfSymbol = 'O';
		# else:
		# 	selfSymbol = '@';
		# originalSelfPieces = self.ba.getPosOfChar(selfSymbol);

		# newSelfPieces = bestMove.board.getPosOfChar(selfSymbol);
		# startpos = ()
		# endpos = ()
		# for osp in originalSelfPieces:
		# 	if osp not in newSelfPieces:
		# 		startpos = osp;
		# 		break;
		# for nsp in newSelfPieces:
		# 	if nsp not in originalSelfPieces:
		# 		endpos = nsp;
		# 		break;

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

	#in moving phase
	# def notAllowedPosition_MP(self):
	# 	isWhite = True;
	# 	if self.colour == 'white':
	# 		isWhite = True;
	# 		opponentSymbol = '@';
	# 		selfSymbol = 'O';
	# 	elif self.colour == 'black':
	# 		isWhite = False;
	# 		opponentSymbol = 'O';
	# 		selfSymbol = '@';

	# 	notAllowedPositionList = [];
			
	# 	notAllowedPositionList.append((0, 0));
	# 	notAllowedPositionList.append((7 ,0));
	# 	notAllowedPositionList.append((0, 7));
	# 	notAllowedPositionList.append((7 ,7));

	# 	opponentPieces = self.ba.getPosOfChar(opponentSymbol);

	# 	#if there are opponent pieces on the board
	# 	if len(opponentPieces) > 0:
	# 		for op in opponentPieces:
	# 			col = op[0];
	# 			row = op[1];
	# 			notAllowedPositionList.append(op);

	# 			#黑棋的4个方向
	# 			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
	# 			nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
	# 			for i in range(0, 4):
	# 				#边界情况
	# 				if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
	# 					continue;

	# 				if self.ba.getChar(directDots[i]) == '-' and self.ba.isInsideBoardRange(nextDirectDots[i], 0) and (self.ba.getChar(nextDirectDots[i]) == 'X' or self.ba.getChar(nextDirectDots[i]) == opponentSymbol or self.ba.getChar(nextDirectDots[i]) == '-'):
	# 					if directDots[i] not in notAllowedPositionList:
	# 						notAllowedPositionList.append(directDots[i]);

	# 	selfPieces = self.ba.getPosOfChar(selfSymbol);
	# 	if len(selfPieces) > 0:
	# 		for sp in selfPieces:
	# 			notAllowedPositionList.append(sp);

	# 	return notAllowedPositionList;



#MiniMax Algorithm 
class MiniMax():
    def __init__(self, game_tree, depth):
        self.game_tree = game_tree;
        #self.root = game_tree.root;
        self.currentNode = None;
        self.successors = [];
        self.depth = depth;
        return

    def minimax(self, node):

        bestNodeList = [];

        bestVal = self.max_value(node, self.depth);

        bestMove = bestVal[1];

        return bestMove;

    def max_value(self, node, depth):
        if depth > 0:
            successors = self.getSuccessors(node);  #create children

        if self.isTerminal(node, depth):
            return [self.getUtility(node), []];

        infinity = float('inf');
        max_value = -infinity;
        i = None;

        # successors = self.getSuccessors(node);
        for child in successors:
            old_max_value = max_value;
            max_value = max(max_value, self.min_value(child, depth - 1)[0]);
            if (old_max_value < max_value):
                i = child;

        return [max_value, child];

    def min_value(self, node, depth):
        if depth > 0:
            successors = self.getSuccessors(node);  #create children

        if self.isTerminal(node, depth):
            return [self.getUtility(node), []];

        infinity = float('inf');
        min_value = infinity;
        i = None;

        # successors = self.getSuccessors(node);
        for child in successors:
        	old_min_value = min_value;
        	min_value = min(min_value, self.max_value(child, depth - 1)[0]);
        	if (old_min_value > min_value):
        		i = child;

        return [min_value, child];


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


class AlphaBeta():
	def __init__(self, game_tree, depth):
		self.game_tree = game_tree;
		self.depth = depth;
		return;

	def alpha_beta_prunning(self, node):
		infinity = float('inf');
		bestVal = -infinity;
		# alpha = bestVal;
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

		# successors = self.getSuccessors(node);
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

		# successors = self.getSuccessors(node)
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


#
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]);


#create children 
class Node():
    def __init__(self, ba, depth, player, value, rootPlayer, turns, move):
        self.depth = depth;
        # self.max_depth = max_depth;
        self.board = ba;   #state
        self.player = player;
        self.value = value;
        # self.maxSoFar = maxSoFar;
        self.rootPlayer = rootPlayer;
        self.turns = turns;
        self.move = move;

        # self.board.updateBoard();
        self.children = [];

        # self.createChildren();

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
            	#判断剩余数量是否为 0
            	return;
            for sp in selfPieces:
                col = sp[0];
                row = sp[1];

                directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
                nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
                for i in range(0,4):
                    #边界情况
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
    #
    def getValue(self, ba, value, depth, rootPlayer):
    	#对Player 来说 
    	#对MAX 来说

    	if depth > 0:
    		return 0;
    	else: 
    		#只计算最后一层的value
    		#假设传进来的 ba 就是最后一层的 board configuration
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
    		#棋盘上剩余的 己方和敌方 棋子数
    		#weight: 10 and -10
    		selfPieces = ba.getPosOfChar(selfSymbol);
    		if len(selfPieces) > 0:
    			selfPiecesLeft = len(selfPieces);
    			#己方的棋子剩的越多，value的值越大
    			num_of_selfPieces_weight = 10 * selfPiecesLeft;
    			pvalue += num_of_selfPieces_weight;

    		opponentPieces = ba.getPosOfChar(opponentSymbol);
    		if len(opponentPieces) > 0:
    			opponentPiecesLeft = len(opponentPieces);
    			#敌方的棋子剩的越少，value的值越大
    			num_of_opponentPieces_weight = (-99) * opponentPiecesLeft;
    			pvalue += num_of_opponentPieces_weight;

    		#feature 2:
    		#棋子离棋盘中心的距离
    		dist = 0
    		for sp in selfPieces:
    			dist += manhattanDistance(sp, (3,3))
    		#距离越近，value 的值越大
    		pvalue += (-1) * dist

    	return pvalue;



    def find_max_value(self):
        if len(self.children) == 0:
            return self.value;

        infinity = float('inf');
        max_value = -infinity;
        
        for child in self.children:
            tmp_value = child.find_max_value();
            max_value = max(max_value, tmp_value);

        self.value = max_value;
        #outputBoard(i.board.board);
        return max_value;


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

    #count the total possible moves of a given piece list
    #边界情况没有考虑?
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

            #the possible pieces around the given piece
            directDots = [(col+1, row), (col-1, row), (col, row+1), (col, row-1)];

            for i in range(0, 4):
                #边界情况
                if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
                    continue;

                #if it is possible to move directly 
                if (self.getChar(directDots[i]) == '-'):
                    total_moves += 1;

                #if it is possible to jump 
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

    	self.eliminate_when_shrink();

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
    			#边界情况
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


    #print all possible moves for white pieces and for black pieces  
    def printWBMoves(self):
        whiteDots = self.getPosOfChar('O');
        blackDots = self.getPosOfChar('@');
        print(self.countMoves(whiteDots));
        print(self.countMoves(blackDots));

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

# if __name__ == '__main__':
# 	p = Player('white');
# 	outputBoard(p.board);
