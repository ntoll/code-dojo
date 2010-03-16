import adventure

def test_one_room ():
  room = """
:Room
This is a room
""".splitlines ()
  rooms, first_location = adventure.load_universe (room)
  assert rooms.keys () == ['Room']
  assert first_location.name == "Room"
  
def test_one_rooms_exits ():
  room = """
:Room
Shut it!
E:Room
W:Room
""".splitlines ()
  rooms, first_location = adventure.load_universe (room)
  assert 'E' in rooms['Room'].exits.keys ()
  assert 'W' in rooms['Room'].exits.keys ()
