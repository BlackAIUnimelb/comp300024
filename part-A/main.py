from queue import PriorityQueue
import copy

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

        if (pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0):
            return '';

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
        super(StatePieces, self).__init__(value, parent, start, goal)
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
                if ((theChar in ['O','@']) and (newNextCol > 7 or newNextCol < 0 or newNextRow > 7 or newNextRow < 0)):
                    continue
                theNextChar = self.environ[newNextCol][newNextRow]
                if ((theChar in ['O','@']) and theNextChar in ['O','@']):
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
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))
        if not self.path:
            print("Goal of " + self.goal + " is not possible")
        return self.path

if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();
    ba.printWBMoves();

    start = (2, 6)       #a white piece position
    goal = (3, 3)        #一个指定黑棋 周围的某个点
    a = AStar_Solver(start, goal, copy.deepcopy(ba.board))
    a.Solve()
    for i in range(len(a.path)):
        print(a.path[i])
