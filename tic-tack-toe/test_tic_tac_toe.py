"""
Nosetests for tic-tac-toe.py

see http://somethingaboutorange.com/mrl/projects/nose/
"""
import tic_tac_toe

def when_game_play_starts_state_should_be_OK_test():
    """ 

    """
    ttt = tic_tac_toe.game()
    status, state = ttt.play()
    assert state.OK()

class TestGameBoard(object):
    def should_return_a_blank_board_on_initialisation_test(self):
        board = tic_tac_toe.GameBoard()
        assert board.state == [ '_', '_', '_', '_', '_', '_', '_', '_', '_', ]
    

def not_yet():
    assert status == 'OK'
    status, state = ttt.play('X', 0)
    assert state == [ 'X', '_', '_', '_', '_', '_', '_', '_', '_', ]
    assert status == 'OK'

def not_yet():
    status, state = ttt.play('O', 5)
    assert state == [ 'X', '_', '_', '_', '_', 'O', '_', '_', '_', ]
    assert status == 'OK'
    status, state = ttt.play('X', 0)
    assert state == [ 'X', '_', '_', '_', '_', 'O', '_', '_', '_', ]
    assert status == 'TAKEN'
    status, state = ttt.play('O', 6)
    assert state == [ 'X', '_', '_', '_', '_', 'O', '_', '_', '_', ]
    assert status == 'BAD TURN'
    status, state = ttt.play('X', 1)
    assert state == [ 'X', 'X', '_', '_', '_', 'O', '_', '_', '_', ]
    assert status == 'OK'
    status, state = ttt.play('O', 6)
    assert state == [ 'X', 'X', '_', '_', '_', 'O', 'O', '_', '_', ]
    assert status == 'OK'
    status, state = ttt.play('X', 2)
    assert state == [ 'X', 'X', 'X', '_', '_', 'O', 'O', '_', '_', ]
    assert status == 'X WINS'
