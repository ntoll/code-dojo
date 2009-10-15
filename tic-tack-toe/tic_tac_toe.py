class game:
    """
    A stub to change
    """
    


    def play(token=None, pos=None):
        """
        Please finish
        """
        print "Do you want to play a game?"
        return "OK", GameBoard()


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

