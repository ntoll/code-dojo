DIRECTIONS = 'N', 'E', 'S', 'W'
NORTH, EAST, SOUTH, WEST = DIRECTIONS

class Player(object):
    def __init__(self, location, name='Player'):
        assert isinstance(location, Location)
        self.location = location
        self.name = name
    

class Location(object):
    def __init__(self, name, description=""):
        self.name = name
        self.description = description 
        self.exits = dict()
    
    def __str__(self):
        return self.name

    def add_direction(self, direction, other_location):
        assert direction in DIRECTIONS
        self.exits[direction] = other_location   
    

    def describe(self):
        out = ''
        out += "Current location: %s\n%s\n" % (self.name, self.description)
        for direction, location in self.exits.items():
            out += "\t%s (%s)\n" % (location, direction)
        return out
sample_universe = """
:Garage
You are in the garage. There are no cars here currently.
E:Bedroom
W:Kitchen

:Kitchen
The kitchen is immaculate. You suspect that nobody has ever actually prepared any food here.
E:Garage

"""

def test_location():
    startroot = Location('Start room')
    kitchen = Location('Kitchen')
    startroot.add_direction(NORTH, kitchen)
    
def test_player():
    lobby = Location('Lobby')
    john = Player(lobby, 'John')

def _load_universe(content):
    location = first_location = None
    locations = {}

    for line in content:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith(':'):
            location = Location(line[1:])
            locations[line[1:]] = location
            if not first_location:
                first_location = location
        elif location is not None and not location.description:
            location.description = line
        else:
            direction, destination = line.split(':', 1)
            location.add_direction(direction, destination)

    for location in locations.values():
       for direction, destination in location.exits.items():
           try:
               location.add_direction(direction, locations[destination])
           except KeyError:
               raise SystemError("Your universe file sucks! %s" % destination)
        
    return locations, first_location
            
def _create_universe():
    start = Location('Start room')
    kitchen = Location('Kitchen')
    garage = Location('Garage')
    start.add_direction(NORTH, kitchen)
    start.add_direction(WEST, garage)
    hobby_room = Location('Hobby room')
    garage.add_direction(EAST, hobby_room)
    
    return start


def play(gamefile):
    #start_room = _create_universe()
    locations, start_room = _load_universe(file(gamefile))
    player_name = raw_input('Player name?: ') or 'No name'
    player = Player(start_room, player_name)
    while True:
        print player.location.describe()

        if not player.location.exits:
            print "No more exits! GAME OVER!"
            break

        next_direction = raw_input('Where to next? ').upper()
        while next_direction not in player.location.exits.keys():
            next_direction = raw_input('Where to next? (%s) ' %\
            ', '.join(player.location.exits.keys())).upper()
        player.location = player.location.exits[next_direction]

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'test':
        test_location()
        test_player()
        sys.exit(0)

    try:
        play(sys.argv[1])        
    except KeyInterupt:
        pass
 
   
          
        
        

