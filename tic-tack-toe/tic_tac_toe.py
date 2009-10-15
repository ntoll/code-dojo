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

class GameBoard():

    def __init__(self):
        self.state = [ "_" ] * 9

    def set(self, x, y, mark):
        index = y * 3 + x
        if self.state[index] != '_':
            return False
        self.state[index] = mark
        return True

    def __repr__(self):
        tmp = ''.join(self.state)
        return tmp[0:3] + "\n" + tmp[3:6] + "\n" + tmp[6:9]


