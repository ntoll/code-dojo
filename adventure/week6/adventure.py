#!/usr/bin/python
import re
try:
    from reverend.thomas import Bayes
except ImportError:
    Bayes = None
from cmd import Cmd

DIRECTIONS = 'N', 'E', 'S', 'W'
NORTH, EAST, SOUTH, WEST = DIRECTIONS

all_item_names = {}

class Player(object):
    def __init__(self, location, name='Player'):
        assert isinstance(location, Location)
        self.location = location
        self.name = name
        self.items = {}

    def inventory(self):
        if not self.items:
            return "Your hands are empty!"
        return "You are carrying: " + ", ".join(self.items)
    

class Location(object):
    def __init__(self, name, description=""):
        self.name = name
        self.description = description 
        self.exits = {}
        self.items = {}
    
    def __str__(self):
        return self.name

    def add_direction(self, direction, other_location):
        assert direction in DIRECTIONS
        self.exits[direction] = other_location   
    
    def describe(self):
        out = ''
        out += "Current location: %s\n%s\n" % (self.name, self.description)
        out += "You can see: "
        out += ", ".join(item.name
            for item in self.items.itervalues() if not item.hidden)
        out += "\n"
        for direction, location in self.exits.iteritems():
            out += "\t%s (%s)\n" % (location, direction)
        return out


class Item(object):
    def __init__(self, name, description="", location=None):
      self.name = name
      self.description = description
      self.location = location
      self.aliases = []
      self.fixed = False
      self.hidden = False

    def __str__(self):
      return self.name

    def add_aliases(self, aliases):
      self.aliases.extend(aliases)

    def describe(self):
      return self.description



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


def find_item(items, name):
    name = name.lower()
    for item in items.itervalues():
	if name == item.name.lower() or name in item.aliases:
	   return item
    return None


def load_universe(content):
    location = first_location = None
    item = None
    locations = {}
    items = {}

    for line in content:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith(':'):
            item = None
            location = Location(line[1:])
            locations[line[1:]] = location
            if not first_location:
                first_location = location
        elif line.startswith('*'):
            location = None
            item = Item(line[1:])
            items[line[1:]] = item
        elif location is not None and not location.description:
            location.description = line
        elif location is not None:
            direction, destination = line.split(':', 1)
            location.add_direction(direction, destination)
        elif item is not None and not item.location and not item.description:
            item.location = line
        elif item is not None and not item.description:
            item.description = line
        elif item is not None:
            cmd, arg = line.split(':', 1)
            if cmd == 'A':
              item.add_aliases(s.strip().lower() for s in arg.split(','))
            elif cmd == "F":
              item.fixed = arg
            elif cmd == "H":
              item.hidden = True

    for location in locations.itervalues():
       for direction, destination in location.exits.items():
           try:
               location.add_direction(direction, locations[destination])
           except KeyError:
               raise SystemError("Your universe file sucks! %s" % destination)

    for item in items.itervalues():
        location = locations[item.location]
        location.items[item.name] = item
        
        all_item_names[item.name] = item.name
        for alias in item.aliases:
            all_item_names[alias] = item.name
            
            
    return locations, first_location

            
class Game(Cmd):

    def __init__(self, gamefile, player_name):
        Cmd.__init__(self)
        self.locations, self.start_room = load_universe(file(gamefile))
        self.player = Player(self.start_room, player_name)
        
        
        self.guesser = self._load_guesser()
        if self.guesser is not None:
            # check that you can guess that 'grab' aliases to 'take'
            assert self.guesser.guess('grab')
        
        print self.player.location.describe()
        
    def _load_guesser(self):
        if Bayes is None:
            return None
        guesser = Bayes()
        print guesser
        print dir(guesser)
        guesser.load('commands.bays')
        return guesser

    def do_move(self, direction):
        direction = direction.upper()
       
        newroom = self.player.location.exits.get(direction,None)
        if newroom == None:
            print "No pass around!"
            return
        
        self.player.location = self.player.location.exits[direction]
        print self.player.location.describe()

    def do_go(self, direction):
        return self.do_move(direction)

    def do_look(self, where):
        if where == "":
            print self.player.location.describe()
        else:
            # TODO validate where
            target = self.player.location.exits.get(where.upper())
            if target:
                print target.describe()
                return
            item = find_item(self.player.location.items, where)
            if not item:
                item = find_item(self.player.items, where)
            if item:
                print item.describe()
            else:
                print "You can't see", where

    def do_examine(self, where):
        return self.do_look(where)
            
    def do_ex(self, where):
        return self.do_look(where)

    def do_get(self, target):
        item = find_item(self.player.location.items, target)
        if item:
            if item.fixed:
                print item.fixed
                return
            del self.player.location.items[item.name]
            self.player.items[item.name] = item
            print "Taken", item.name
        else:
            print "You can't see", target

    def do_take(self, target):
        return self.do_get(target)
            
    def do_drop(self, target):
        item = find_item(self.player.items, target)
        if item:
            del self.player.items[item.name]
            self.player.location.items[item.name] = item
            print "Dropped", item.name
        else:
            print "You don't have", target

    def do_inventory(self, target):
        print self.player.inventory()

    def do_inv(self, target):
        return self.do_inventory(target)

    def do_i(self, target):
        return self.do_inventory(target)

    def do_put(self, target):
        return self.do_drop(target)
            
    def postcmd(self, stop, x):
        pass
    
    def default(self, line):
        # failed all the above, 
        if self.guesser is not None:
            # let's use Bayes
            all_item_names['north'] = 'N'
            all_item_names['east'] = 'E'
            all_item_names['west'] = 'W'
            all_item_names['south'] = 'S'
            all_item_names['N'] = 'N'
            all_item_names['E'] = 'E'
            all_item_names['W'] = 'W'
            all_item_names['S'] = 'S'
            for name in all_item_names:
                if re.search(r'\b%s\b' % re.escape(name), line, re.I):
                    guesses = self.guesser.guess(line.replace(name,''))
                    print guesses
                    if guesses:
                        method_name = guesses[0][0]
                        getattr(self, method_name)(all_item_names[name])
                        return
            
def play(gamefile):
    #start_room = _create_universe()
    
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
