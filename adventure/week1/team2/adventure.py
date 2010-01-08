from cmd import Cmd
import sys

rooms = [
	dict(
		name='Cabin',
    	desc="""
		Your cabin is full of sailors tossing in it.
		""", 
    	exits={'out': 'Corridor'},
	),
	dict(
		name='Corridor',
		desc='''
		Sailors run left and right, alarms are ring loudly.
		''',
		exits={
			'in': 'Cabin',
			'up': 'Deck'
		}
	),
	dict(
		name='Deck',
		desc='''
		The wind blows in your hair.
		''',
		exits={
			'aft': 'Stern',
			'fore': 'Prow',
			'down': 'Corridor',
		}
	),
	dict(
		name='Stern',
		desc='''
		You are missing all the excitement up at the front of the ship!
		''',
		exits={
			'fore': 'Deck',
		}
	),
	dict(
		name='Prow',
		desc='''
		The ship has run aground on a giant octpus, which stands firmly
		in the ocean, rising twenty feet above your head.
		''',
		exits={
			'aft': 'Deck',
			'octopus': 'Octopus'
		}
	),
	dict(
		name='Octopus',
		desc='''
		You are perched precariously on the head of a mildly-annoyed giant 
		octopus, who is waving its tentacles inquisitively up towards you.
		''',
		exits={
			'ship': 'Prow',
		}
	)
]

intro = '''
Welcome onboard HMS Calamity. You're in your cabin, good luck!

Electric lights keep everything in your room visible.  However you prefer
to write by candle light, so you've brought a dozen for your trip.

Suddenly, there is a thump!  Seconds layer a siren sounds, as the ship rocks.


Try `look'ing around or `go' where you want. `Win' to depart this journey.
'''


class Room(object):
    def __init__(self, name, exits, desc):
        self.name = name
        self.exits = exits
        self.desc = desc

room_map = dict((d['name'], Room(**d)) for d in rooms)
# get the exits as objects.
for k in room_map.keys():
    room_map[k].exit_objs = {}
    for direction, roomname in room_map[k].exits.items():
        aroom = room_map[roomname]
        room_map[k].exit_objs[direction] = aroom

        
class Game(Cmd):

    def __init__(self, room_map, start):
        Cmd.__init__(self)
        self.current_room = room_map[start]
        self.map = room_map
        self.done = False

    def do_look(self, _):
        exits = self.current_room.exits.keys()
        print self.current_room.name
        print self.current_room.desc
        print "There are the following exits: %s" % ", ".join(exits)

    def do_go(self, direction):
        if direction in self.current_room.exits:
            print "Going " + direction
            self.current_room = self.current_room.exit_objs[direction]
            self.do_look(None)
        else:
            print "Can't go " + direction

    def do_win(self, lala):
        print 'ya! you win'
        self.done = True
        import pygame.examples.aliens
        pygame.examples.aliens.main()

    def default(self, line):
        if line in self.current_room.exits:
            self.do_go(line)
        else:
            print "I don't know how to do that!"

    def postcmd(self, stop, x):
        return self.done
  
if __name__ == '__main__':
    g = Game(room_map, 'Cabin')
    g.cmdloop(intro)
    
