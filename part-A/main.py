from queue import PriorityQueue
import copy

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

        if self.path:
            # print("Goal of " + str(self.goal) + " is not possible")
            return [];

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
        # self.direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]  #上下左右
        # self.diagonal = [(-1, -1), (-1, 1), (-1, 1), (1, 1)]
        self.usedDots = [];
        self.totalCost = 0;

        # Item format:( weight, [target position], (blackDot position) )
        # Weight = (distance of nearby 2 whiteDots) - (existed number of whiteDot within pair)*K
        # k = 1 (preset)
        self.priorityQueue = PriorityQueue();

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

                weight = 0;
                # [(1st expandPos, path), (2nd expandPos, path)]
                foundPos = []
                # Each can eliminate pair coordinates
                if pair[0] == 1:

                    pos = pair[1][0];
                    takenDot = pair[1][1]
                    # DotType already took this position
                    expandResult = self.expandCheckNearby(pos, takenDot);

                    if (expandResult != None):

                        # Records dot position and path
                        foundPos.append(expandResult[1:]);
                        pathLength = expandResult[0]
                        weight += pathLength;

                elif pair[0] == 2:

                    takenDot = ();
                    # Checks the first position within pair
                    pos1 = pair[1][0];
                    expandResult1 = self.expandCheckNearby(pos1);

                    if (expandResult1 != None):

                        foundPos.append(expandResult1[1:]);
                        pathLength = expandResult1[0]
                        weight += pathLength;

                        takenDot = expandResult1[1]

                    # Checks the second position within pair
                    pos2 = pair[1][1];
                    expandResult2 = self.expandCheckNearby(pos2, takenDot, pos1);

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

    # return coordinates of dotType that has the shortest distance to the target position
    def expandCheckNearby(self, pos, takenDot = None, takenDestination=None):

        # print(pos)
        expandPos = pos;
        expandIndex = 1;
        allDots = []
        # print("start: {}".format(pos))

        pQueue = PriorityQueue();


        allDotTypeDots = self.boardAnalyser.getPosOfChar(self.dotType);

        for dot in allDotTypeDots:

            if dot != takenDot:

                tempBoard = self.boardAnalyser.board;

                if takenDestination != None and self.boardAnalyser.getChar(takenDestination) == '-':
                    tempBoard = copy.deepcopy(self.boardAnalyser.board);
                    tempBoard[takenDestination[0]][takenDestination[1]] = self.dotType;
                    # outputBoard(tempBoard);

                a = AStar_Solver(dot, pos, tempBoard)
                a.Solve()
                if len(a.path) != 0:
                    pQueue.put([len(a.path), dot, a.path]);

        if pQueue.qsize():

            nearestDot = pQueue.get();
            # print("nearest -> {}".format(nearestDot[1]))
            # print(nearestDot)
            # self.usedDots.append(nearestDot[1]);

            return nearestDot;

        # Couldn't find any nearby piece
        return None;

    def updateBoard(self, origin, replace):

        colOrigin = origin[0];
        rowOrigin = origin[1];

        colReplace = replace[0];
        rowReplace = replace[1];
        # print("did {} <- {}".format(origin, replace))

        if self.boardAnalyser.board[colOrigin][rowOrigin] == '-':
            self.boardAnalyser.board[colOrigin][rowOrigin] = self.boardAnalyser.getChar(replace);
            self.boardAnalyser.board[colReplace][rowReplace] = '-';
            # print("updated -> {}".format(origin))
        else:
            print("Update failed");

        # Empty PriorityQueue
        # self.priorityQueue.empty();
        self.priorityQueue = PriorityQueue();

    def execKilling(self):

        if self.priorityQueue.qsize() > 0:
            # Move DotType to target position
            data = self.priorityQueue.get();
            # print("Get -> {}".format(data))
            # weight = data[0];
            foundPos = data[1];
            pair = data[2];

            # print(pair)
            index = 0;
            # outputBoard(self.boardAnalyser.board);
            for moveDot in foundPos:
                # print("--> {}".format(moveDot));

                dotPos = moveDot[0];
                path = moveDot[1];
                self.totalCost += len(path)
                # Update board
                self.updateBoard(pair[index], dotPos);
                outputPath(path)
                # drawPath(self.boardAnalyser.board, path);
                # outputBoard(self.boardAnalyser.board)
                index += 1

            return True;

        else:
            return None;

if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();

    if ba.command == 'Moves':
        ba.printWBMoves();
    # execute Massacre
    elif ba.command == 'Massacre':

        bEliminator = DotEliminator("O", ba.getPosOfChar("@"), ba)
        while len(bEliminator.getCanEliminateDotPairs()) > 0:

            bEliminator.findNearByDots();
            bEliminator.execKilling();

            for dot in ba.getPosOfChar("@"):
                bEliminator.checkDotNeedRemove(dot);

