from cmd import Cmd
import re

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
        self.props = []
    
    def __str__(self):
        return self.name

    def add_direction(self, direction, other_location):
        assert direction in DIRECTIONS
        self.exits[direction] = other_location   
    
    def describe(self):
        out = ''
        out += "Current location: %s\n%s\n\n" % (self.name, self.description)
        for direction, location in self.exits.items():
            out += "\t%s (%s)\n" % (location, direction)
        if self.props:
            plural = len(self.props) > 1
            out += "\n%s item%s may come in handy (hint hint):\n\t%s" \
            % (['This', 'These'][plural], ['', 's'][plural], '\n\t'.join(prop.aliases[0] for prop in self.props))
        return out

class Prop(object):
    def __init__(self, name):

        self.description = None
        self.location = None
        self.aliases = [name]


def test_location():
    startroot = Location('Start room')
    kitchen = Location('Kitchen')
    startroot.add_direction(NORTH, kitchen)
    
def test_player():
    lobby = Location('Lobby')
    john = Player(lobby, 'John')

def load_universe(content):
    location = first_location = None
    locations = {}
    props = {}
    
    #parts = re.split(r"(?:\n|\r\n|\r){2,}", content.read())
    parts = content.read().split('\r\n\r\n')
    
    import pdb
    for part in parts:
        location = None
        prop = None
        for line in part.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            #if line == 'N:Hall':
            #    pdb.set_trace()
            if not location and not prop:
                # first line
                if line.startswith(':'):
                    location = Location(line[1:])
                    locations[line[1:]] = location
                    if not first_location:
                        first_location = location

                if line.startswith('*'):
                    prop = Prop(line[1:])
                    props[line[1:]] = prop


            else:
                if location:
                    #print 'line', line
                    if not location.description or line[1] != ':':
                        location.description+= line
                    else:
                        direction, destination = line.split(':', 1)
                        #print 'direction, destination', direction, destination
                        location.add_direction(direction, destination)
                else:
                    if not prop.location:
                        items_location = locations[line]
                        prop.location = items_location
                        items_location.props.append(prop)
                    elif not prop.description:
                        prop.description = line
                    elif line.startswith("A:"):
                        # aliases
                        #A:flashlight
                        prop.aliases = [x.strip() for x in line[2:].split(',')]

                

    for location in locations.values():
       for direction, destination in location.exits.items():
           try:
               location.add_direction(direction, locations[destination])
           except KeyError:
               raise SystemError("Your universe file sucks! %s" % destination)
        
    return locations, first_location
            
class Game(Cmd):

    def __init__(self, gamefile, player_name):
        Cmd.__init__(self)
        self.locations, self.start_room = load_universe(file(gamefile))
        self.player = Player(self.start_room, player_name)
        print self.player.location.describe()

    def do_move(self, direction):
        direction = direction.upper()
       
        newroom = self.player.location.exits.get(direction,None)
        if newroom == None:
            print "No pass around!"
            return
        
        self.player.location = self.player.location.exits[direction]

    def do_look(self, where):
        if where == "":
            self.player.location.describe()
        else:
            # TODO validate where
            newroom = self.player.location.exits.get(where,None)
            print newroom.describe()
            pass

    def do_joke(self, ok):
        print "that is not funny.  What don't you try a pun?"
        if hasattr(self, 'joke'):
           print 'this is funny:%s' % self.joke
        self.joke = ok
        
    def postcmd(self, stop, x):
        #pass
        if not hasattr(self, 'joke'):
            print self.player.location.describe()
            #print self.player.location.describe()
    

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
    if sys.argv[1] == 'test':
        test_location()
        test_player()
        sys.exit(0)

    try:
        play(sys.argv[1])        
    except KeyboardInterrupt:
        pass
