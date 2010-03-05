from cmd import Cmd
import random

DIRECTIONS = 'N', 'E', 'S', 'W'
NORTH, EAST, SOUTH, WEST = DIRECTIONS



class Player(object):
    def __init__(self, location, name='Player'):
        assert isinstance(location, Location)
        self.location = location
        self.backpack = []
        self.name = name
    
    def remove_object(self, thing):
        for o in self.backpack:
            if o.name == thing:
               self.backpack.remove(o)
               return o
        return None

class Monster(Player):
    def __init__(self, location, name, world):
        Player.__init__(self, location, name)
        self.world = world

    def random_action(self):
        random.choice([self.rnd_move, self.rnd_drop])()

    def rnd_move(self):
        self.location = random.choice(self.location.exits.values())
        #print "Monster moved to", self.location.name

    def rnd_drop(self):
        pass

class Object(object):
    def __init__(self, name):
        self.name = name
        self.description = ""

    def add_description(self, desc):
        self.description += desc

    def __repr__(self):
        return self.name

        
class Location(object):
    def __init__(self, name, description=""):
        self.name = name
        self.description = description 
        self.exits = dict()
        self.objects = []
    
    def __str__(self):
        return self.name

    def add_direction(self, direction, other_location):
        assert direction in DIRECTIONS
        self.exits[direction] = other_location

    def add_object(self, obj):
        self.objects.append(obj)
    
    def remove_object(self, thing):
        for o in self.objects:
            if o.name == thing:
               self.objects.remove(o)
               return o
        return None

    def describe(self):
        out = ''
        out += "Current location: %s\n%s\n" % (self.name, self.description)
        for direction, location in self.exits.items():
            out += "\t%s (%s)\n" % (location, direction)
        if self.objects:
            out += "You can see " + ", ".join([("a " + x.name) for x in self.objects]) + ".\n"
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

def load_universe(content):
    location = first_location = None
    locations = {}

    current_object = None
    object_location = None

    for line in content:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith(':'):
            location = Location(line[1:])
            locations[line[1:]] = location
            if not first_location:
                first_location = location
        elif line.startswith('*'):
            location = None
            current_object = Object(line[1:])
        elif location is not None and not location.description:
            location.description = line
        elif location is not None:
            direction, destination = line.split(':', 1)
            location.add_direction(direction, destination)
        elif current_object:
            if object_location is None:
                object_location = line
                locations[object_location].add_object(current_object)
            else:
                current_object.add_description(line)

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
        self.monsters = [Monster(self.start_room, "Monster", self)]
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

    def do_inventory(self, something):
        if self.player.backpack:
            print "You are carrying:", ", ".join([str(x) for x in self.player.backpack])
        else:
            print "You are carrying nothing"

    def do_pickup(self, thing):
        object = self.player.location.remove_object(thing) 
        if object == None:
            print "Object",thing,"was not in the room!"
        else:
            self.player.backpack.append(object)

    def do_leave(self, thing):
        object = self.player.remove_object(thing) 
        if object == None:
            print "Object",thing,"was not in your backpack!"
        else:
            self.player.location.add_object(object)

    do_drop = do_leave

    def postcmd(self, stop, x):
        print self.player.location.describe()
        monsters = [monster for monster in self.monsters if monster.location == self.player.location]
        if monsters:
            print "You see %d monsters" % len(monsters)
        for monster in monsters:
            monster.random_action()
    

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
    if sys.argv[:1] == ['test']:
        test_location()
        test_player()
        sys.exit(0)

    try:
        play(sys.argv[1])        
    except KeyboardInterrupt:
        pass
