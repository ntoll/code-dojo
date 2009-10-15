class game:
    """
    A stub to change
    """
    


    def play(token=None, pos=None):
        """
        Please finish
        """
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

