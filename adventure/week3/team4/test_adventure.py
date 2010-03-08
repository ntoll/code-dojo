import adventure
import item

from nose.tools import *

def test_one_room ():
  room = """
:Room
This is a room
""".splitlines ()
  rooms, first_location, items, item_location = adventure.load_universe (room)
  assert rooms.keys () == ['Room']
  assert first_location.name == "Room"
  
def test_one_rooms_exits ():
  room = """
:Room
Shut it!
E:Room
W:Room
""".splitlines ()
  rooms, first_location, items, item_location = adventure.load_universe (room)
  assert 'E' in rooms['Room'].exits.keys ()
  assert 'W' in rooms['Room'].exits.keys ()

def test_load_item ():
  universe = """
:Balcony
This is a room  
  
*Flowers
Balcony
A wilted bouquet of flowers. There is a card with a note that has been obliterated by rain or tears.
A:bouquet, flower
""".splitlines()
  rooms, first_location, items, item_location = adventure.load_universe (universe)
  assert len(items) == 1
  assert item_location.has_key(adventure.Location("Balcony"))
  

def test_item ():
  item1 = item.Item ("Item1", "One Item")
  
def test_hashable_location ():
  d = {}
  d[adventure.Location ("location")] = 1
  d[adventure.Location ("location")] = 2
  assert_true (len (d) == 1)

def test_game ():
  assert adventure.Game ("data.txt", "Fred")

if __name__ == "__main__":
  import sys
  import nose
  nose.runmodule (exit=False)
  if sys.stdout.isatty (): raw_input ("Press enter...")
