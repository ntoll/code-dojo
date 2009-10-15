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

    def OK(self):
        return True

    def set(self, x, y, mark):
        self.state[y * 3 + x] = mark
