from queue import PriorityQueue
import copy

def outputBoard(board):

    # for row in board:
    for row in zip(*board):

        for col in row:

            print("{} ".format(col), end="")

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

        print(path[i+1], symbol)

        copyBoard[path[i+1][0]][path[i+1][1]] = symbol

    outputBoard(copyBoard)


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

        result = []
        for row in zip(*self.board):
            l = []
            for col in row:
                l.append(col)
            result.append(l)

        self.board = result

        self.goal = input();

        return True;

    def getChar(self, pos):

        if (pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0):
            return '';

        pos_x = pos[0];
        pos_y = pos[1];
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
                    resultPos.append((x, y));

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
        #super().__init__()
        self.environ = copy.deepcopy(environ)
        #self.path_cost = path_cost
        self.dist = self.GetDist()

    def GetDist(self):
        #priority
        if (self.value[0] == self.goal[0] and self.value[1] == self.goal[1]):
            return 0
        dist = abs(self.value[0] - self.goal[0]) + abs(self.value[1] - self.goal[1])
        return dist

    def CreateChildren(self):
    	#create nodes
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
                if ((theChar in ['O', '@', 'X']) and (newNextCol > 7 or newNextCol < 0 or newNextRow > 7 or newNextRow < 0)):
                    continue
                theNextChar = self.environ[newNextCol][newNextRow]
                if ((theChar in ['O','@', 'X']) and theNextChar in ['O','@']):
                    continue
                if ((theChar in ['O','@']) and theNextChar == '-'):
                    val = (newNextCol, newNextRow)
                    newEnviron = copy.deepcopy(self.environ)
                    newEnviron[self.value[0]][self.value[1]] = '-'
                    newEnviron[val[0]][val[1]] = 'O'
                    child = StatePieces(val, self, newEnviron, 0, 0)
                    self.children.append(child)

class AStar_Solver:

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

        if not self.path:
            print("Goal of " + str(self.goal) + " is not possible")
        return self.path

# Step1: Find all blackDots that have valid pair (blackdots that can be eliminated)

# Step2: Sort valid blackDots based on nearby whiteDots (The blackdot has the most and the closest whiteDots to be put the first)

    #1.1: First Priority:  if there is a whiteDot at the pair position
    #     Second Priority: Nearby closest whiteDots
    #     Third Priority:  Might be added in the future

# Step3: Try to eliminate the target blackDot and update the board and priorityQueue after its been eliminated

# Step4: Re-scan the board and jump to step1 until no  blackDots can be eliminated anymore
class DotEliminator():
    # DotType is the dot we use to eliminate dots
    # if dots are black, then dotType is white
    def __init__(self, dotType, dots, boardAnalyser):
        self.dots = dots;
        self.boardAnalyser = boardAnalyser;
        self.dotType = dotType;
        self.eliminateDotType = '@'
        self.direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]  #上下左右
        self.diagonal = [(-1, -1), (-1, 1), (-1, 1), (1, 1)]

        # Item format:( weight, [target position], (blackDot position) )
        # Weight = (distance of nearby 2 whiteDots) - (existed number of whiteDot within pair)*K
        # k = 1 (preset)
        self.priorityQueue = PriorityQueue()

    def printBlackDots(self):

        print(self.dots);

    def checkDotNeedRemove(self, dot):

        col = dot[0];
        row = dot[1];

        # Remove dot that between two dotType
        if (self.boardAnalyser.getChar( (col, row + 1)) in ['X', self.dotType] and self.boardAnalyser.getChar((col, row - 1)) in ['X', self.dotType] ):
            self.boardAnalyser.board[col][row] = '-';
        elif (self.boardAnalyser.getChar( (col - 1, row)) in ['X', self.dotType] and self.boardAnalyser.getChar((col + 1, row)) in ['X', self.dotType]):
            self.boardAnalyser.board[col][row] = '-';

    def getCanEliminateDotPairs(self):

        result = []

        for dot in self.boardAnalyser.getPosOfChar(self.eliminateDotType):

            col = dot[0]
            row = dot[1]

            self.checkDotNeedRemove(dot);

            pair = [];
            # Check up and down pair
            if (self.boardAnalyser.getChar( (col, row + 1)) == '-' and self.boardAnalyser.getChar((col, row - 1)) == '-' ):
                pair.append([2, [(col, row + 1), (col, row - 1)], dot]);
            # Check if up position has been taken by dotType we use
            elif (self.boardAnalyser.getChar( (col, row + 1)) in ['X', self.dotType] and self.boardAnalyser.getChar((col, row - 1)) == '-'):
                pair.append([1, [(col, row - 1), (col, row + 1)], dot]);
            # Check if down position has been taken by dotType we use
            elif (self.boardAnalyser.getChar( (col, row - 1)) in ['X', self.dotType] and self.boardAnalyser.getChar((col, row + 1)) == '-'):
                pair.append([1, [(col, row + 1), (col, row - 1)], dot]);


            # Check left and right pair
            if (self.boardAnalyser.getChar( (col - 1, row)) == '-' and self.boardAnalyser.getChar((col + 1, row)) == '-'):
                pair.append([2, [(col - 1, row), (col + 1, row)], dot]);
            # Check if left position has been taken by dotType we use
            elif (self.boardAnalyser.getChar( (col - 1, row)) in ['X', self.dotType] and self.boardAnalyser.getChar((col + 1, row)) == '-'):
                pair.append([1, [(col + 1, row), (col - 1, row)], dot]);
            # Check if right position has been taken by dotType we use
            elif (self.boardAnalyser.getChar( (col + 1, row)) in ['X', self.dotType] and self.boardAnalyser.getChar((col - 1, row)) == '-'):
                pair.append([1, [(col - 1, row), (col + 1, row)], dot]);


            if (len(pair) > 0):
                result.append(pair)

        # [[number of pairs, [pair coordinates], dot position], ... ]
        return result

    def findNearByDots(self):

        allDotsPairs = self.getCanEliminateDotPairs()

        for pairData in allDotsPairs:

            for pair in pairData:

                print(pair)

                weight = 0;
                # [(1st expandPos, path), (2nd expandPos, path)]
                foundPos = []

                # Each can eliminate pair coordinates
                if pair[0] == 1:

                    pos = pair[1][0];
                    # DotType already took this position
                    takenPos = pair[1][1];
                    expandResult = self.expandCheckNearby(pos, takenPos);

                    if (expandResult != None):

                        foundPos.append(expandResult);
                        pathLength = len(expandResult[1])
                        weight += pathLength;

                elif pair[0] == 2:

                    # Checks the first position within pair
                    pos1 = pair[1][0];
                    expandResult = self.expandCheckNearby(pos1);

                    if (expandResult != None):

                        foundPos.append(expandResult);
                        pathLength = len(expandResult[1])
                        weight += pathLength;

                    # Checks the second position within pair
                    pos2 = pair[1][1];
                    expandResult = self.expandCheckNearby(pos2);

                    if (expandResult != None):

                        foundPos.append(expandResult);
                        pathLength = len(expandResult[1])
                        weight += pathLength;

                if weight != 0:
                    self.priorityQueue.put([weight, foundPos, pair[1]])

    # return coordinates of dotType that has the shortest distance to the target position
    def expandCheckNearby(self, pos, takenPos=None):

        # print(pos)
        expandPos = pos;
        expandIndex = 1;
        allDots = []
        # print("start: {}".format(pos))

        while True:

            if expandIndex == max(7-pos[0], 7-pos[1]):
                break

            # Direct check 4 direction
            for i in range(0, 4):

                newCol = pos[0] + self.direction[i][0] * expandIndex;
                newRow = pos[1] + self.direction[i][1] * expandIndex;

                expandPos = (newCol, newRow);

                if (self.boardAnalyser.getChar(expandPos) == self.dotType) and takenPos != expandPos:
                    # print("Try direct: {}".format(expandPos))
                    a = AStar_Solver(expandPos, pos, ba.board)
                    a.Solve()
                    print("Try -> {}".format(expandPos))
                    if (len(a.path) == 0):
                        continue;
                    # drawPath(ba.board, a.path)
                    return (expandPos, a.path);

            # Diagonal check 4 direction
            for i in range(0, 4):

                newCol = pos[0] + self.diagonal[i][0] * expandIndex;
                newRow = pos[1] + self.diagonal[i][1] * expandIndex;

                expandPos = (newCol, newRow);

                if (self.boardAnalyser.getChar(expandPos) == self.dotType) and takenPos != expandPos:
                    # print("Try Diagonal: {}".format(expandPos))

                    a = AStar_Solver(expandPos, pos, ba.board)
                    a.Solve()
                    if (len(a.path) == 0):
                        continue;
                    # drawPath(ba.board, a.path)

                    return (expandPos, a.path);


            expandIndex += 1;

        # Couldn;t find any nearby piece
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

        # Empty PriorityQueue
        self.priorityQueue.empty();


    def execKilling(self):

        if self.priorityQueue.qsize() > 0:
            # Move DotType to target position
            data = self.priorityQueue.get(0);
            print(data)
            weight = data[0];
            foundPos = data[1];
            pair = data[2];

            # outputBoard(self.boardAnalyser.board);

            for moveDot in foundPos:

                dotPos = moveDot[0];
                path = moveDot[1];
                # targetPair = moveDot[2];
                # Update board
                drawPath(self.boardAnalyser.board, path);
                
                self.updateBoard(path[-1], dotPos);


            return True;

        else:
            return None;

if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();
    ba.printWBMoves();

    # start = (1, 7)       #a white piece position
    # goal = (7, 1)        #一个指定黑棋 周围的某个点
    # a = AStar_Solver(start, goal, copy.deepcopy(ba.board))
    # a.Solve()
    # for i in range(len(a.path)):
    #     print(a.path[i])
    # print("{} {}".format(ba.getChar((2, 2)), ba.getChar((2, 4))));

    print(ba.getPosOfChar("@"))
    bEliminator = DotEliminator("O", ba.getPosOfChar("@"), ba)

    while bEliminator.getCanEliminateDotPairs():

        bEliminator.findNearByDots();
        bEliminator.execKilling();

        for dot in ba.getPosOfChar("@"):
            bEliminator.checkDotNeedRemove(dot);

        outputBoard(bEliminator.boardAnalyser.board)

        print(len(bEliminator.getCanEliminateDotPairs()))


    # drawPath(ba.board, a.path)
