from queue import PriorityQueue
import copy

# Global function to output sequence of moves for a given path
def outputPath(path):

    for i in range(1, len(path)):

        print("{} -> {}".format(path[i-1], path[i]));

# Process board data and format them into 2D matrix
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

        result = []
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

    # Count the number of moves for a given series of pieces
    def countMoves(self, pieces):

        total_moves = 0;

        if (len(pieces) == 0):
            return 0;

        # Counts direct moves
        for piece in pieces:

            col = piece[0];
            row = piece[1];

            # loop through 4 directions
            directPieces = [(col+1, row), (col-1, row), (col, row+1), (col, row-1)];

            for i in range(0, 4):

                if (self.getChar(directPieces[i]) == '-'):
                    total_moves += 1;

                if (self.getChar(directPieces[i]) == 'O' or self.getChar(directPieces[i]) == '@'):

                    ccol = directPieces[i][0];
                    rrow = directPieces[i][1];

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

        whitePieces = self.getPosOfChar('O');
        blackPieces = self.getPosOfChar('@');
        print(self.countMoves(whitePieces));
        print(self.countMoves(blackPieces));

    # Return sequeces of moves to eliminate all enemy pieces
    def calcMassacreMove(self):

        bEliminator = PieceEliminator("O", self.getPosOfChar("@"), ba)
        while len(bEliminator.getCanEliminatePiecePairs()) > 0:

            bEliminator.findNearByPieces();
            bEliminator.execElimination();

            for piece in self.getPosOfChar("@"):
                bEliminator.checkPieceNeedRemove(piece);


class State(object):
    def __init__(self, value, parent, start = 0, goal = 0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

        def GetDist(self):
            pass
        def CreateChildren(self):
            pass

class StatePieces(State):
    def __init__(self, value, parent, environ, start = 0, goal = 0):
        super().__init__(value, parent, start, goal)
        self.environ = copy.deepcopy(environ)
        self.dist = self.GetDist()

    def GetDist(self):
        # Huristic function that returns manhattan distance
        if (self.value[0] == self.goal[0] and self.value[1] == self.goal[1]):
            return 0
        dist = abs(self.value[0] - self.goal[0]) + abs(self.value[1] - self.goal[1])
        return dist

    def CreateChildren(self):
    	#Generate node path
        if not self.children:

            direction = [
                (0, -1), (0, 1), (-1, 0), (1, 0)    #上下左右??
            ]
            for i in range(0, 4):
            	#下一个点 考虑直接走的情况
                newCol = self.value[0] + direction[i][0]
                newRow = self.value[1] + direction[i][1]
                if (newCol > 7 or newCol < 0 or newRow > 7 or newRow < 0):
                    continue
                val = (newCol, newRow)

                theChar = self.environ[newCol][newRow]
                if theChar == '-':
                    newEnviron = copy.deepcopy(self.environ)
                    newEnviron[self.value[0]][self.value[1]] = '-'
                    newEnviron[val[0]][val[1]] = 'O'
                    child = StatePieces(val, self, newEnviron, 0, 0)
                    self.children.append(child)
                    continue

                # 再下一个点   考虑跳的情况
                newNextCol = newCol + direction[i][0]
                newNextRow = newRow + direction[i][1]

                if ((theChar in ['O','@','X']) and (newNextCol > 7 or newNextCol < 0 or newNextRow > 7 or newNextRow < 0)):
                    continue

                theNextChar = self.environ[newNextCol][newNextRow]
                if ((theChar in ['O','@','X']) and theNextChar in ['O','@','X']):
                    continue

                if ((theChar in ['O','@']) and theNextChar == '-'):
                    val = (newNextCol, newNextRow)
                    newEnviron = copy.deepcopy(self.environ)
                    newEnviron[self.value[0]][self.value[1]] = '-'
                    newEnviron[val[0]][val[1]] = 'O'
                    child = StatePieces(val, self, newEnviron, 0, 0)
                    self.children.append(child)

class Path_Solver:

    def __init__(self, start, goal, environ):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.environ = environ

    def Solve(self):
        startState = StatePieces(self.start, 0, self.environ, self.start, self.goal)
        count = 0
        self.priorityQueue.put((0, count, startState))
        while(not self.path and self.priorityQueue.qsize()):
        	#expand most desirable node
            closestChild = self.priorityQueue.get()[2]
            closestChild.CreateChildren()

            self.visitedQueue.append(closestChild.value)

            for child in closestChild.children:
                if child.value not in self.visitedQueue:
                    count +=1
                    # Reaches to goal that is the distance is equal to 0
                    if child.dist == 0:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))

        if self.path:
            # print("Goal of " + str(self.goal) + " is not possible")
            return [];

        return self.path

# Step1: Find all blackPieces that can be eliminated
# Step2: Sort valid blackPieces based on nearby whitePieces (The blackpiece has the most and the closest whitePieces to be put the first)
# Step3: Try to eliminate the target blackPiece and update the board and priorityQueue after its been eliminated
# Step4: Re-scan the board and jump to step1 until no more blackPieces can be eliminated
class PieceEliminator():
    # PieceType is the piece we use to eliminate pieces
    # if pieces are black, then pieceType is white
    def __init__(self, pieceType, pieces, boardAnalyser):
        self.pieces = pieces;
        self.boardAnalyser = boardAnalyser;
        self.pieceType = pieceType;
        self.eliminatePieceType = '@'
        self.usedPieces = [];
        self.totalCost = 0;

        # Item format:( weight, [position of two eliminating pieces], (blackPiece position) )
        # Weight = (costs of the shortest path of nearby 2 whitePieces)
        self.priorityQueue = PriorityQueue();

    def printBlackPieces(self):

        print(self.pieces);

    def checkPieceNeedRemove(self, piece):

        col = piece[0];
        row = piece[1];

        # Remove piece that between two pieceType
        if (self.boardAnalyser.getChar( (col, row + 1)) in ['X', self.pieceType] and self.boardAnalyser.getChar((col, row - 1)) in ['X', self.pieceType] ):
            self.boardAnalyser.board[col][row] = '-';
        elif (self.boardAnalyser.getChar( (col - 1, row)) in ['X', self.pieceType] and self.boardAnalyser.getChar((col + 1, row)) in ['X', self.pieceType]):
            self.boardAnalyser.board[col][row] = '-';

    def getCanEliminatePiecePairs(self):

        result = []

        for piece in self.boardAnalyser.getPosOfChar(self.eliminatePieceType):

            col = piece[0]
            row = piece[1]

            self.checkPieceNeedRemove(piece);

            pair = [];
            # Check up and down pair
            if (self.boardAnalyser.getChar( (col, row + 1)) == '-' and self.boardAnalyser.getChar((col, row - 1)) == '-' ):
                pair.append([2, [(col, row + 1), (col, row - 1)], piece]);
            # Check if up position has been taken by pieceType we use
            elif (self.boardAnalyser.getChar( (col, row + 1)) in ['X', self.pieceType] and self.boardAnalyser.getChar((col, row - 1)) == '-'):
                    pair.append([1, [(col, row - 1), (col, row + 1)], piece]);
                # Check if down position has been taken by pieceType we use
            elif (self.boardAnalyser.getChar( (col, row - 1)) in ['X', self.pieceType] and self.boardAnalyser.getChar((col, row + 1)) == '-'):
                    pair.append([1, [(col, row + 1), (col, row - 1)], piece]);


            # Check left and right pair
            if (self.boardAnalyser.getChar( (col - 1, row)) == '-' and self.boardAnalyser.getChar((col + 1, row)) == '-'):
                pair.append([2, [(col - 1, row), (col + 1, row)], piece]);
            # Check if left position has been taken by pieceType we use
            elif (self.boardAnalyser.getChar( (col - 1, row)) in ['X', self.pieceType] and self.boardAnalyser.getChar((col + 1, row)) == '-'):
                    pair.append([1, [(col + 1, row), (col - 1, row)], piece]);
                # Check if right position has been taken by pieceType we use
            elif (self.boardAnalyser.getChar( (col + 1, row)) in ['X', self.pieceType] and self.boardAnalyser.getChar((col - 1, row)) == '-'):
                    pair.append([1, [(col - 1, row), (col + 1, row)], piece]);


            if (len(pair) > 0):
                result.append(pair)

        # [[number of pairs, [pair coordinates], piece position], ... ]
        return result

    def findNearByPieces(self):

        allPiecesPairs = self.getCanEliminatePiecePairs()

        for pairData in allPiecesPairs:

            for pair in pairData:

                weight = 0;
                # [(1st expandPos, path), (2nd expandPos, path)]
                foundPos = []
                # Each can eliminate pair coordinates
                if pair[0] == 1:

                    pos = pair[1][0];
                    takenPiece = pair[1][1]
                    # PieceType already took this position
                    expandResult = self.expandCheckNearby(pos, takenPiece);

                    if (expandResult != None):

                        # Records piece position and path
                        foundPos.append(expandResult[1:]);
                        pathLength = expandResult[0]
                        weight += pathLength;

                elif pair[0] == 2:

                    takenPiece = ();
                    # Checks the first position within pair
                    pos1 = pair[1][0];
                    expandResult1 = self.expandCheckNearby(pos1);

                    if (expandResult1 != None):

                        foundPos.append(expandResult1[1:]);
                        pathLength = expandResult1[0]
                        weight += pathLength;

                        takenPiece = expandResult1[1]

                    # Checks the second position within pair
                    pos2 = pair[1][1];
                    expandResult2 = self.expandCheckNearby(pos2, takenPiece, pos1);

                    if (expandResult1 != None and expandResult2 != None):

                        foundPos.append(expandResult2[1:]);
                        pathLength = expandResult2[0]
                        weight += pathLength;
                    else:
                        continue;

                if weight != 0:
                    # pair[1] are (two pairs)
                    # print("put ->{}".format([weight, foundPos, pair[1]]))
                    self.priorityQueue.put([weight, foundPos, pair[1]])

    # return coordinates of pieceType that has the shortest distance to the target position
    def expandCheckNearby(self, pos, takenPiece = None, takenDestination=None):

        expandPos = pos;
        expandIndex = 1;
        allPieces = []
        pQueue = PriorityQueue();

        allPieceTypePieces = self.boardAnalyser.getPosOfChar(self.pieceType);

        for piece in allPieceTypePieces:

            if piece != takenPiece:

                tempBoard = self.boardAnalyser.board;

                if takenDestination != None and self.boardAnalyser.getChar(takenDestination) == '-':
                    tempBoard = copy.deepcopy(self.boardAnalyser.board);
                    tempBoard[takenDestination[0]][takenDestination[1]] = self.pieceType;

                a = Path_Solver(piece, pos, tempBoard)
                a.Solve()
                if len(a.path) != 0:
                    pQueue.put([len(a.path), piece, a.path]);

        if pQueue.qsize():

            nearestPiece = pQueue.get();

            return nearestPiece;

        # Couldn't find any nearby piece
        return None;

    def updateBoard(self, origin, replace):

        colOrigin = origin[0];
        rowOrigin = origin[1];

        colReplace = replace[0];
        rowReplace = replace[1];

        if self.boardAnalyser.board[colOrigin][rowOrigin] == '-':
            self.boardAnalyser.board[colOrigin][rowOrigin] = self.boardAnalyser.getChar(replace);
            self.boardAnalyser.board[colReplace][rowReplace] = '-';
        else:
            print("Update failed");

        # Init a new priorityQueue
        self.priorityQueue = PriorityQueue();

    def execElimination(self):

        if self.priorityQueue.qsize() > 0:
            # Move PieceType to target position
            data = self.priorityQueue.get();
            foundPos = data[1];
            pair = data[2];

            index = 0;
            for movePiece in foundPos:

                piecePos = movePiece[0];
                path = movePiece[1];
                self.totalCost += len(path)
                # Update board
                self.updateBoard(pair[index], piecePos);
                # Output the sequeces of moves
                outputPath(path)

                index += 1

            return True;

        else:
            return None;

if __name__ == '__main__':

    # Init boardAnalyser object
    ba = BoardAnalyser();
    # Process baord data and format them as a 2D matrix
    ba.formatInput();

    # Execute Move command
    if ba.command == 'Moves':
        # Print number of moves that black pieces and whites pieces can make
        ba.printWBMoves();

    # Execute Massacre command
    elif ba.command == 'Massacre':
        # Return sequeces of moves to eliminate all enemy pieces
        ba.calcMassacreMove();
