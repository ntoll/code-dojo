class Game(object):
    """
    A stub to change
    """
    
    def __init__(self):
        self.board = GameBoard()
        self.current_marker = "X"

    def play(token=None, pos=None):
        """
        Please finish
        """
        print "Do you want to play a game?"
        return "OK", GameBoard()

    def take_turn(self,x,y):
        marker = self.current_marker
        if self.board.set(x, y, marker):
            self.current_marker = marker == 'X' and 'O' or 'X'
            return True
        return False
        

    def show_board(self):
        return repr(self.board)

    def get_winner(self):
        winposs = [
            ((0,0), (0,1), (0,2)),
            ((1,0), (1,1), (1,2)),
            ((2,0), (2,1), (2,2)),
            ((0,0), (0,1), (0,2)),
            ((1,0), (1,1), (1,2)),
            ((2,0), (2,1), (2,2)),
            ((0,0), (1,1), (2,2)),
            ((0,2), (1,1), (2,0)),
]
        import pdb; pdb.set_trace()
        board = self.board
        for poss in winposs:
            marks = [board.get(x,y) for x, y in poss]
            if marks == ['X' ] * 3:
                return 'X'
            if marks == ['O'] * 3:
                return 'O'


            
class GameBoard():

    def __init__(self):
        self.state = [ "_" ] * 9

    def get(self, x, y):
        index = y * 3 + x
        return self.state[index]

    def set(self, x, y, mark):
        index = y * 3 + x
        if self.state[index] != '_':
            return False
        self.state[index] = mark
        return True

    def __repr__(self):
        tmp = ''.join(self.state)
        return tmp[0:3] + "\n" + tmp[3:6] + "\n" + tmp[6:9]


