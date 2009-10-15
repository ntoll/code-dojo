"""
Nosetests for tic-tac-toe.py

see http://somethingaboutorange.com/mrl/projects/nose/
"""
import tic_tac_toe

class TestGameBoard(object):

    def setup(self):
        self.board = tic_tac_toe.GameBoard()


    def should_return_a_blank_board_on_initialisation_test(self):
        assert self.board.state == [ '_', '_', '_', '_', '_', '_', '_', '_', '_', ]

    def set_x_on_first_position_test(self):
        self.board.set(0, 0, 'X')
        assert self.board.state == [ 'X', '_', '_', '_', '_', '_', '_', '_', '_', ]
    
    def set_two_different_numbers_test(self):
        self.board.set(1, 2, 'X')
        assert self.board.state == [ '_', '_', '_', '_', '_', '_', '_', 'X', '_', ]
        
    def set_two_moves_test(self):
        assert self.board.set(1, 0, 'X')
        assert self.board.set(0, 2, 'O')
        assert self.board.state == [ '_', 'X', '_', '_', '_', '_', 'O', '_', '_', ]

    def attempt_illegal_move_test(self):
        assert self.board.set(0, 0, 'X')
        status = self.board.set(0, 0, 'O')
        assert self.board.state == [ 'X', '_', '_', '_', '_', '_', '_', '_', '_', ]
        assert not status

    def show_board_test(self):
        assert repr(self.board) == "___\n___\n___"

class TestGame(object):

    def setup(self):
        self.game = tic_tac_toe.Game()

    def test_new_game_has_empty_board(self):
        assert self.game.show_board() == """\
___
___
___"""

    def test_1st_move_is_X_test(self):
        self.game.take_turn(0,0)
        assert self.game.show_board() == """\
X__
___
___"""

    def test_2_moves(self):
        assert self.game.take_turn(0,0)
        assert self.game.take_turn(1,1)
        assert self.game.show_board() == """\
X__
_O_
___"""


    def test_invalid_move(self):
        assert self.game.take_turn(0,0)
        board_before = self.game.show_board()
        assert not self.game.take_turn(0,0)
        assert self.game.show_board() == board_before

    def test_winning(self):
        self.game.take_turn(0,0)
        self.game.take_turn(0,1)
        self.game.take_turn(1,0)
        self.game.take_turn(0,2)
        self.game.take_turn(2,0)
        assert self.game.get_winner() == 'X'
        



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
