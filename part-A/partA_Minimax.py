from queue import PriorityQueue
import copy

#-------------------------------------------------------------------
#Display functions 

def outputBoard(board):

    # for row in board:
    for row in zip(*board):

        for col in row:

            print("{} ".format(col), end="")

        print()

    print()

def drawPath(board, path):

    if (len(path) == 0):
        return

    copyBoard = copy.deepcopy(board);

    symbol = '~';

    copyBoard[path[0][0]][path[0][1]] = symbol

    for i in range(0, len(path)-1):

        # Up direction (col equals but row is not)
        if (path[i+1][1] < path[i][1] and path[i+1][0] == path[i][0]):
            symbol = '↑';
        # Down
        elif (path[i+1][1] > path[i][1] and path[i+1][0] == path[i][0]):
            symbol = '↓'
        # Left
        elif (path[i+1][0] < path[i][0] and path[i+1][1] == path[i][1]):
            symbol = '←'
        else:
            symbol = '→'

        # print(path[i+1], symbol)

        copyBoard[path[i+1][0]][path[i+1][1]] = symbol
    outputBoard(copyBoard)


def outputPath(path):

    for i in range(1, len(path)):

        print("{} -> {}".format(path[i-1], path[i]));

#------------------------------------------------------------------------------

#Board Analyser class for analysing the board and store pieces into list 

class BoardAnalyser():

    def __init__(self):
        self.board = None;
        self.command = None;
        self.chars = ['-', 'X', 'O', '@'];

    def formatInput(self):

        self.board = [];
        # Read board
        for i in range(0, 8):
            content = input();
            self.board.append(content.split());

        result = []                       #why write twice?
        for row in zip(*self.board):
            l = []
            for col in row:
                l.append(col)
            result.append(l)

        self.board = result

        self.command = input();

        return True;

    def getChar(self, pos):

        if (pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0):
            return '';

        pos_x = pos[0];
        pos_y = pos[1];
        o = self.board[pos_x][pos_y];

        # object_dict = {
        #     "X" : "conner",
        #     "O" : "white",
        #     "@" : "black",
        #     "-" : "space",
        # }

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


    #print all possible moves for white pieces and for black pieces  
    def printWBMoves(self):
        whiteDots = self.getPosOfChar('O');
        blackDots = self.getPosOfChar('@');
        print(self.countMoves(whiteDots));
        print(self.countMoves(blackDots));

    #这两个function 暂时没用
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

#-------------------------------------------------------------------------------


def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]);

class Node():
    def __init__(self, ba, depth, player, value):
        self.depth = depth;
        self.board = ba;   #state
        self.player = player;
        self.value = value;

        self.board.updateBoard();

        self.children = [];
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
                        self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1)));
                    #check if can jump
                    if (self.board.getChar(directDots[i]) == 'O' or self.board.getChar(directDots[i]) == '@'):
                        ccol = directDots[i][0];
                        rrow = directDots[i][1];
                        newBoard = copy.deepcopy(self.board);

                        # down
                        if (i == 0 and ccol+1 <= 7 and self.board.getChar((ccol + 1, rrow)) == '-'):
                            endPos = (ccol + 1, rrow);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1)));
                            continue;

                        # up
                        if (i == 1 and ccol-1 >= 0 and self.board.getChar((ccol - 1, rrow)) == '-'):
                            endPos = (ccol - 1, rrow);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1)));
                            continue;

                        # Right
                        if (i == 2 and rrow+1 <= 7 and self.board.getChar((ccol, rrow + 1)) == '-'):
                            endPos = (ccol, rrow + 1);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1)));
                            continue;

                        # Left
                        if (i == 3 and rrow-1 >= 0 and self.board.getChar((ccol, rrow - 1)) == '-'):
                            endPos = (ccol, rrow - 1);
                            newBoard.makeMove(wp, endPos);
                            self.children.append(Node(newBoard, self.depth-1, self.player, self.getValue(copy.deepcopy(self.board), self.value, wp, endPos, self.depth-1)));
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
        distFromStartToebp = [];
        distFromEndToebp = [];


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
                    ind = (i + 2) % 4;
                    if ba.getChar(directDots[ind]) == '-' and directDots[ind] not in eliminateBlackPosition:
                        eliminateBlackPosition.append(directDots[ind]);

            #保存距离
            dist = manhattanDistance(bp, startPos);          #指定白棋 到所有黑棋的 距离
            distListFromStart.append(dist);

            dist = manhattanDistance(bp, endPos);        #指定白棋 位移之后 到所有黑棋的 距离
            distListFromEnd.append(dist);

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
            minIndexToebp = distFromStartToebp.index(minDistToebp);

            if distListFromStart[minIndex] == 1:   #如果白棋还没移动前，已经在黑棋旁边了
                newValue = 0;
            elif distFromEndToebp[minIndexToebp] == 1:
                newValue = 999;
            elif distFromEndToebp[minIndexToebp] < distFromStartToebp[minIndexToebp]:
                newValue = 9;
            else:
                newValue = -9;
            return value + newValue + (depth);



        if distListFromStart[minIndex] == 1:   #如果白棋还没移动前，已经在黑棋旁边了
            newValue = 0;

        elif distListFromEnd[minIndex] == 1:
            newValue = 99;      #如果白棋走到那颗黑棋旁边

        elif distListFromEnd[minIndex] < distListFromStart[minIndex]: #白棋向那颗黑棋靠近
            newValue = 9;  #approaching is good 

        else:
            newValue = -9;

        return value + newValue + (depth);


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
            if (old_max_value != max_value):
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

if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();        #get input

    depth = 5;
    player = 1;
    value = 0;
    node = Node(ba, depth, player, value);

    miniMax = MiniMax(node);
    bm = miniMax.minimax(node);

    for i in bm:
        outputBoard(i.board.board); 

    print("finish");