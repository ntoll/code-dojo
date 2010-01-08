from game import *

class TestGame(object):
    def setup(self):
        northRoom = Room("You are in a passageway, it is still dark")
        eastRoom = Room("Swamp, dark")
        firstRoom = Room("You are in a dark cave", north=northRoom, east=eastRoom)
        self.g = Game(firstRoom)

    def test_inital_look(self):
        assert self.g.cmd("LOOK") == "You are in a dark cave. There are exits to the north and east"

    def test_look_is_not_case_sensitive(self):
        assert self.g.cmd("Look") == "You are in a dark cave. There are exits to the north and east"
        
    def test_south(self):
        assert self.g.cmd("SOUTH") == "You can't do that"

    def test_movement(self):
        assert self.g.cmd("NORTH") == "You go north"
        assert self.g.cmd("LOOK") == "You are in a passageway, it is still dark. There are exits to the south"
        assert self.g.cmd("SOUTH") == "You go south"
        assert self.g.cmd("LOOK") == "You are in a dark cave. There are exits to the north and east"

        
    def test_invalid_command(self):
        assert self.g.cmd("WIBBLE") == "You can't do that"
