
class BoardAnalyser():

    def __init__(self):
        self.board = None;
        self.goal = None;

    def formatInput(self):

        self.board = [];
        # Read board
        for i in range(0, 8):
            content = input();
            self.board.append(content.split());

        self.goal = input();

        print(self.board, self.goal);

    def getObject(self, pos):
    	pos_y = pos[0];
    	pos_x = pos[1];
    	o = self.board[pos_x][pos_y];

    	object_dict = {
    		"X" : "conner",
    		"O" : "white",
    		"@" : "black",
    		"-" : "space",
    	}

    	print(object_dict[o]);


if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();
    ba.getObject([5,1]);
