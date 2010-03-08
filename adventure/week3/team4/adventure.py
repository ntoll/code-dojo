from cmd import Cmd
from item import Item

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
        
    def __hash__ (self):
        return hash (self.name)
        
    def __eq__ (self, other):
        return self.name == other.name

    def add_direction(self, direction, other_location):
        assert direction in DIRECTIONS
        self.exits[direction] = other_location   
    

    def describe(self):
        out = ''
        out += "Current location: %s\n%s\n" % (self.name, self.description)
        for direction, location in self.exits.items():
            out += "\t%s (%s)\n" % (location, direction)
        return out

def load_universe(content):
    location = first_location = None
    locations = {}
    items = []
    
    location_item = {}
    content = (i.strip () for i in iter(content))

    for line in content:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        #print line or "***"
        if line.startswith(':'):
            location = Location(line[1:])
            locations[line[1:]] = location
            if not first_location:
                first_location = location
        elif line.startswith("*"):
            item = Item(line[1:])
            items.append(item)
            line2 = content.next()
            if line2.strip ():
                location_item.setdefault (line2, []).append (item)
                line3 = content.next ()
                if line3.strip ():
                    item.description = line3
                    line4 = content.next ()
                    if line4:
                        item.aliases = [s.strip () for s in line4.split (",")]
                        
            #location_item.setdefault(content.next (), []).append (item)
            #item.description = content.next()
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

    item_location = dict((locations[k], v) for k,v in location_item.items())
    return locations, first_location, items, item_location
            
class Game(Cmd):

    def __init__(self, gamefile, player_name):
        Cmd.__init__(self)
        self.locations, self.start_room, self.items, self.item_location = load_universe(file(gamefile))
        self.player = Player(self.start_room, player_name)
        print self.player.location.describe()
        self.show_whats_here ()

    def show_whats_here (self):
        print "You can see:", ", ".join (item.name for item in self.item_location.get (self.player.location, [])) or "Nothing"        
    
    def do_move(self, direction):
        direction = direction.upper()
       
        newroom = self.player.location.exits.get(direction,None)
        if newroom is None:
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
        
    def postcmd(self, stop, x):
        print self.player.location.describe()
        self.show_whats_here ()
    

def play(gamefile):
    player_name = raw_input('Player name?: ') or 'No name'
    g = Game(gamefile, player_name)    
    
    g.cmdloop()

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
