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
		self.cnt = self.cnt + 1;
		if (self.cnt > 12):
			self.placingPhase = False;

		#User input 
		# paction = None;
		# if self.placingPhase:
		# 	pos = input("Placing Phase White Player:");
		# 	# tmplist = ();
		# 	pos = pos.split();
		# 	a = int(float(pos[0]));
		# 	b = int(float(pos[1]));
		# 	paction = (a ,b);
		# else:
		# 	pos = input("Moving Phase White Player:");
		# 	# tmplist = ();
		# 	pos = pos.split();
		# 	a = int(float(pos[0]));
		# 	b = int(float(pos[1]));
		# 	c = int(float(pos[2]));
		# 	d = int(float(pos[3]));
		# 	paction = ((a ,b), (c, d));

		#if it is in placing phase 
		if self.placingPhase:

			paction = ();
			eliminateBlackPosition = self.isBPKillable();
			if len(eliminateBlackPosition) == 0:
				#no black pieces to be eliminated
				#防守
				allowedPositionsList = self.allowedPositions();

				#如果需要 defensive move的话
				defensiveMove = self.defensivePlacePostion(allowedPositionsList);
				if len(defensiveMove) > 0:
					paction = (defensiveMove[0][0], defensiveMove[0][1]);
					self.ba.placePiece(paction, 'white');
					self.ba.updateBoard();
					return paction;
				else:
					#如果不需要defense
					#随意place??
					while(1):
						rand_col = randint(0, 7);
						rand_row = randint(2, 3);
						rand_pos = (rand_col, rand_row);
						if rand_pos in allowedPositionsList:
							paction = rand_pos;
							self.ba.placePiece(paction, 'white');
							self.ba.updateBoard();
							return paction;
						else:
							rand_row = 1;
							rand_pos = (rand_col, rand_row);
							if rand_pos in allowedPositionsList:
								paction = rand_pos;
								self.ba.placePiece(paction, 'white');
								self.ba.updateBoard();
								return paction;
							else:
								rand_row = 0;
								rand_pos = (rand_col, rand_row);
								if rand_pos in allowedPositionsList:
									paction = rand_pos;
									self.ba.placePiece(paction, 'white');
									self.ba.updateBoard();
									return paction;


			else:
				#假设 len(eliminateBlackPosition) 最大就是 1
				paction = (eliminateBlackPosition[0][0], eliminateBlackPosition[0][1]);
				self.ba.placePiece(paction, 'white');
				self.ba.updateBoard();
				return paction;

		#if it is in moving phase
		else:
			paction = ();



		self.ba.placePiece(paction, 'white');
		self.ba.updateBoard();
		return paction;


	def update(self, actions):
		self.ba.placePiece(actions, 'black');
		self.ba.updateBoard();

		return;

	#helper functions

	#in placing phase, check if there is a black piece that is killable 
	#return list
	def isBPKillable(self):
		blackPieces = self.ba.getPosOfChar('@');
		if len(blackPieces) == 0:
			return [];

		eliminateBlackPosition = [];

		for bp in blackPieces:
			col = bp[0];
			row = bp[1];

			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
			for i in range(0, 4):
				#边界情况
				if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
					continue;
				if self.ba.getChar(directDots[i]) == 'O' or self.ba.getChar(directDots[i]) == 'X':
					ind = (i + 2) % 4;
					if self.ba.isInsideBoardRange(directDots[ind]) and self.ba.getChar(directDots[ind]) == '-' and directDots[ind] not in eliminateBlackPosition:
						# 白棋只能放在第5行及以上
						if directDots[ind][1] <= 5:
							eliminateBlackPosition.append(directDots[ind]);

		return eliminateBlackPosition;

    #in placing phase, there are position where white pieces cannot place
	def notAllowedPosition(self):
		notAllowedPositionList = [];
		#对白棋来说，最下面两行不可以place
		for i in range(6, 8):
			for j in range(0, 8):
				notAllowedPositionList.append((j,i));
		notAllowedPositionList.append((0, 0));
		notAllowedPositionList.append((7 ,0));

		blackPieces = self.ba.getPosOfChar('@');

		#if there are black pieces on the board
		if len(blackPieces) > 0:
			for bp in blackPieces:
				col = bp[0];
				row = bp[1];

				#黑棋的4个方向
				directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
				nextDirectDots = [(col+2, row), (col, row+2), (col-2, row), (col, row-2)];
				for i in range(0, 4):
					#边界情况
					if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
						continue;

					if self.ba.getChar(directDots[i]) == '-' and self.ba.isInsideBoardRange(nextDirectDots[i]) and (self.ba.getChar(nextDirectDots[i]) == 'X' or self.ba.getChar(nextDirectDots[i]) == '@' or self.ba.getChar(nextDirectDots[i]) == '-'):
						if directDots[i] not in notAllowedPositionList:
							notAllowedPositionList.append(directDots[i]);

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
	def defensivePlacePostion(self, allowedPositionsList):
		defensiveMove = [];
		whitePieces = self.ba.getPosOfChar('O');
		if len(whitePieces) == 0:
			return [];

		defensiveMove = [];

		for wp in whitePieces:
			col = wp[0];
			row = wp[1];

			#白棋的4个方向
			directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
			for i in range(0, 4):
				#边界情况
				if (self.ba.isInsideBoardRange(directDots[i]) == False):
					continue;
				if self.ba.getChar(directDots[i]) == '@':
					ind = (i + 2) % 4;
					if self.ba.isInsideBoardRange(directDots[ind]) and self.ba.getChar(directDots[ind]) == '-' and directDots[ind] in allowedPositionsList:
						defensiveMove.append(directDots[ind]);
						break;

		#假设整个棋盘上只有一个字要去defense
		return defensiveMove;



#MiniMax Algorithm 
class MiniMax():
    def __init__(self, game_tree):
        self.game_tree = game_tree;
        #self.root = game_tree.root;
        self.currentNode = None;
        self.successors = [];
        return

    def minimax(self, node):
        bestNodeList = [];

        while not self.isTerminal(node):

            bestVal = self.max_value(node);

            successors = self.getSuccessors(node);
            bestMove = None;

            for child in successors:                  #??
                if child.value == bestVal.value:
                    bestMove = child;
                    break;

            node = bestMove;
            bestNodeList.append(node);

        return bestNodeList;

    def max_value(self, node):
        if self.isTerminal(node):
            return self.getUtility(node);

        infinity = float('inf');
        max_value = -infinity;
        i = None;

        successors = self.getSuccessors(node);
        for child in successors:
            old_max_value = max_value;
            max_value = max(max_value, child.value);
            if (old_max_value < max_value):
                i = child;

        #outputBoard(i.board.board);
        return i;

    def getSuccessors(self, node):
        assert node is not None;
        return node.children;

    def isTerminal(self, node):
        assert node is not None;
        return len(node.children) == 0;

    def getUtility(self, node):
        assert node is not None;
        return node.value;



#
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]);


#create children 
class Node():
    def __init__(self, ba, depth, player, value, maxSoFar, max_depth):
        self.depth = depth;
        self.max_depth = max_depth;
        self.board = ba;   #state
        self.player = player;
        self.value = value;
        self.maxSoFar = maxSoFar;

        self.board.updateBoard();
        self.children = [];

        if self.depth >= 0:
            if self.value < self.maxSoFar[self.max_depth - self.depth]:
                return;
            else:
                self.maxSoFar[self.max_depth - self.depth] = self.value;

        self.createChildren();

    def createChildren(self):
        if self.depth >= 0 and len(self.board.getPosOfChar('@')) > 0:
            whitePieces = self.board.getPosOfChar('O');         #return all white pieces positions 
            for wp in whitePieces:
                col = wp[0];
                row = wp[1];

                directDots = [(col+1, row), (col-1, row), (col, row+1), (col, row-1)];
                for i in range(0,4):
                    #边界情况
                    if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
                        continue;

                    #check if can move directly
                    if (self.board.getChar(directDots[i]) == '-'):
                        newBoard = copy.deepcopy(self.board);
                        endPos = directDots[i];
                        newBoard.makeMove(wp, endPos);
                        self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1), self.maxSoFar, self.max_depth));
                        continue;
                    #check if can jump
                    if (self.board.getChar(directDots[i]) == 'O' or self.board.getChar(directDots[i]) == '@'):
                        ccol = directDots[i][0];
                        rrow = directDots[i][1];
                        newBoard = copy.deepcopy(self.board);

                        # down
                        if (i == 0 and ccol+1 <= 7 and self.board.getChar((ccol + 1, rrow)) == '-'):
                            endPos = (ccol + 1, rrow);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1), self.maxSoFar, self.max_depth));
                            continue;

                        # up
                        if (i == 1 and ccol-1 >= 0 and self.board.getChar((ccol - 1, rrow)) == '-'):
                            endPos = (ccol - 1, rrow);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1), self.maxSoFar, self.max_depth));
                            continue;

                        # Right
                        if (i == 2 and rrow+1 <= 7 and self.board.getChar((ccol, rrow + 1)) == '-'):
                            endPos = (ccol, rrow + 1);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1), self.maxSoFar, self.max_depth));
                            continue;

                        # Left
                        if (i == 3 and rrow-1 >= 0 and self.board.getChar((ccol, rrow - 1)) == '-'):
                            endPos = (ccol, rrow - 1);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1), self.maxSoFar, self.max_depth));
                            continue;

    #evaluation function 
    #start position is the position of the white piece
    def getValue(self, ba, value, startPos, endPos, depth):
        blackPieces = ba.getPosOfChar('@');
        if len(blackPieces) == 0:
            return value;

        distListFromStart = [];
        distListFromEnd = [];
        newValue = 0;

        eliminateBlackPosition = [];
        # isBpHasWpAround = [];

        distFromStartToebp = [];
        distFromEndToebp = [];

        numberOfWpAroundBp = [];
        for j in range(0, len(blackPieces)):
            numberOfWpAroundBp.append(0);
        j = 0;


        for bp in blackPieces:

            # 检查周围是否有白棋
            col = bp[0];
            row = bp[1];

            directDots = [(col+1, row), (col, row+1), (col-1, row), (col, row-1)];
            for i in range(0, 4):
                #边界情况
                if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
                    continue;
                if ba.getChar(directDots[i]) == 'O' or ba.getChar(directDots[i]) == 'X':
                    # numberOfWpAroundBp[j] = numberOfWpAroundBp[j] + 1;
                    ind = (i + 2) % 4;
                    if ba.isInsideBoardRange(directDots[ind]) and ba.getChar(directDots[ind]) == '-' and directDots[ind] not in eliminateBlackPosition:
                        eliminateBlackPosition.append(directDots[ind]);
                        break;

            for i in range(0, 4):
                if (directDots[i][0] < 0 or directDots[i][0] > 7 or directDots[i][1] < 0 or directDots[i][1] > 7):
                    continue;
                if ba.getChar(directDots[i]) == 'O' or ba.getChar(directDots[i]) == 'X':
                    numberOfWpAroundBp[j] = numberOfWpAroundBp[j] + 1;

            #保存距离
            dist = manhattanDistance(bp, startPos);          #指定白棋 到所有黑棋的 距离
            distListFromStart.append(dist);

            dist = manhattanDistance(bp, endPos);        #指定白棋 位移之后 到所有黑棋的 距离
            distListFromEnd.append(dist);

            j = j + 1;

        minDist = min(distListFromStart);
        minIndex = distListFromStart.index(minDist);
        goodBlackPiece = blackPieces[minIndex];             #距离指定白棋最近的那颗黑棋

        if len(eliminateBlackPosition) > 0:
            for ebp in eliminateBlackPosition:
                dist = manhattanDistance(ebp, startPos);       
                distFromStartToebp.append(dist);

                dist = manhattanDistance(ebp, endPos);
                distFromEndToebp.append(dist);

            minDistToebp = min(distFromStartToebp);
            cnt = 0;

            for h in distFromStartToebp:
                if h == minDistToebp:
                    cnt = cnt + 1;

            minIndexToebp = distFromStartToebp.index(minDistToebp);

            if distListFromStart[minIndex] == 1 and numberOfWpAroundBp[minIndex] == 1:   #如果白棋还没移动前，已经在黑棋旁边了 ??  并且 黑棋周围不能有两颗白棋
                newValue = 3;
            elif distFromEndToebp[minIndexToebp] == 0 and numberOfWpAroundBp[minIndex] != 2:
                newValue = 999;
            elif distFromEndToebp[minIndexToebp] < distFromStartToebp[minIndexToebp]:
                newValue = 19 + (-1)*distFromStartToebp[minIndexToebp];         #越近的白棋，value 越高
            else:
                newValue = -19;
            return value + newValue + ((-1)*(0.5)**(depth))*1000;



        if distListFromStart[minIndex] == 1:   #如果白棋还没移动前，已经在黑棋旁边了
            newValue = 3;

        elif distListFromEnd[minIndex] == 1:
            newValue = 60;      #如果白棋走到那颗黑棋旁边

        elif distListFromEnd[minIndex] < distListFromStart[minIndex]: #白棋向那颗黑棋靠近
            newValue = 9 + (-1)*distListFromStart[minIndex];  #approaching is good       #越近的白棋，value 越高

        else:
            newValue = -9;

        return value + newValue + ((-1)*(0.5)**(depth))*1000;

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
    def updateBoard(self):
        board = copy.deepcopy(self.board);
        blackPieces = self.getPosOfChar('@');
        for bp in blackPieces:
            col = bp[0];
            row = bp[1];

            left_right = [(col, row-1), (col, row+1)];
            up_down = [(col-1, row), (col+1, row)];

            if left_right[0][1] >=0 and left_right[1][1] <= 7:
                if (self.getChar(left_right[0]) == 'O' and self.getChar(left_right[1]) == 'O') or (self.getChar(left_right[0]) == 'O' and self.getChar(left_right[1]) == 'X') or (self.getChar(left_right[0]) == 'X' and self.getChar(left_right[1]) == 'O'):
                    board[col][row] = '-';
            if up_down[0][0] >= 0 and up_down[1][0] <= 7:
                if (self.getChar(up_down[0]) == 'O' and self.getChar(up_down[1]) == 'O') or (self.getChar(up_down[0]) == 'O' and self.getChar(up_down[1]) == 'X') or ((self.getChar(up_down[0]) == 'X' and self.getChar(up_down[1]) == 'O')):
                    board[col][row] = '-';
        self.board = copy.deepcopy(board);
        return;

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

# if __name__ == '__main__':
# 	p = Player('white');
# 	outputBoard(p.board);
