
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

if __name__ == '__main__':

    ba = BoardAnalyser();
    ba.formatInput();
