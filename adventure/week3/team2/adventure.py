#!/usr/bin/python

from cmd import Cmd

DIRECTIONS = 'N', 'E', 'S', 'W'
NORTH, EAST, SOUTH, WEST = DIRECTIONS

class Player(object):
    def __init__(self, location, name='Player'):
        assert isinstance(location, Location)
        self.location = location
        self.name = name
        self.inventory = {}

class GameObject(object):
    
    def __init__(self, name):
        self.name = name

class Location(object):
    def __init__(self, name, description=""):
        self.name = name
        self.description = description 
        self.exits = dict()
        self.objects = {}
    
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
        if self.objects:
            out += "There are the following items here:\n"
        for object in self.objects.keys():
            out += "\t%s" % object
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

def load_locations(content):
    location = first_location = None
    locations = {}

    for line in content:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.startswith("*"):
            break

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

def load_gameobjects(content):
    
    lines = list(content)
    
    indexes = [i for i, j in enumerate(lines) if j.startswith("*")]
    
    current_game_object = None
    game_state = []
    
    for index in indexes:
        current_game_object = GameObject(lines[index][1:].strip())
        current_game_object.location = lines[index+1].strip()
        current_game_object.description = lines[index+2].strip()
        if lines[index+3].strip() != "":
            current_game_object.aliases = lines[index+3].replace(" ", "").split(",")
        game_state.append(current_game_object)

    return game_state

def load_universe(content):
    locations, start_room = load_locations(content)
    game_objects = load_gameobjects(content)

    for object in game_objects:
        locations[object.location].objects[object.name] = object

    return locations, start_room, game_objects
    
class Game(Cmd):

    def __init__(self, gamefile, player_name):
        Cmd.__init__(self)
        self.locations, self.start_room, self.gameobjects = load_universe(file(gamefile))
        self.player = Player(self.start_room, player_name)
        print self.player.location.describe()

    def do_move(self, direction):
        direction = direction.upper()
       
        newroom = self.player.location.exits.get(direction,None)
        if newroom == None:
            print "No pass around!"
            return
        
        self.player.location = self.player.location.exits[direction]

    do_go = do_move

    def do_look(self, what):
        location = self.player.location
        if what == "":
            location.describe()
        elif what in location.exits:
            # TODO validate where
            newroom = location.exits[where]
            print newroom.describe()
        elif what in location.objects:
            print location.objects[what].description
        else:
            print "What are you looking at punk!"
        
    def postcmd(self, stop, x):
        print self.player.location.describe()
    
    def do_bye(self, foo):
        sys.exit()

    def do_pickup(self, object):
        if object in self.player.location.objects:
            self.player.inventory[object] = self.player.location.objects.pop(object)
            print "Picked up %s" % object
        else:
            print "No %s here" % object

    def do_drop(self, object):
        if object in self.player.inventory:
            self.player.location.objects[object] = self.player.inventory.pop(object)
            print "Dropped %s" % object
        else:
            print "your not holding %s" % object


def play(gamefile):
    #start_room = _create_universe()
    
    player_name = raw_input('Player name?: ') or 'No name'
    g = Game(gamefile, player_name)    
    
    g.cmdloop()
	
'''    while True:
        

        if not player.location.exits:
            print "No more exits! GAME OVER!"
            break

        next_direction = raw_input('Where to next? ').upper()


        while next_direction not in player.location.exits.keys():
            next_direction = raw_input('Where to next? (%s) ' %\
            ', '.join(player.location.exits.keys())).upper()
        player.location = player.location.exits[next_direction]
'''

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Usage: %s DATAFILE" % sys.argv[0]
        sys.exit(1)
    if sys.argv[1] == 'test':
        test_location()
        test_player()
        sys.exit(0)

    try:
        play(sys.argv[1])        
    except KeyboardInterrupt:
        pass
