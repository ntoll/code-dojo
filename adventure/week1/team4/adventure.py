from cmd import Cmd
from types import DictType

class Room(DictType):
	def __init__(self, desc, objects = None):
		super(Room, self).__init__()
		self.desc = desc
		self.objects = objects or []

class Item(object):
	def __init__ (self, name):
		self.name = name

	def __repr__ (self):
		return self.name


table = Item("table")
chair = Item("chair")

office = Room("Office",([table, chair]))
kitchen = Room("Kitchen")
hall = Room("Hall")
toilet = Room("Toilet")

office['E'] = kitchen
kitchen['W'] = office
office['S'] = hall
hall['N'] = office
kitchen['N'] = toilet
toilet['S'] = kitchen

world = [office, kitchen, hall, toilet] 

class Player(Cmd):
	def __init__(self, location):
		Cmd.__init__(self)
		self.location = location
		self.intro = "You are in a maze of twisty passages..."

	def do_move(self, direction):
		newloc = self.location.get(direction,None)
		if newloc:
			self.go_room(newloc)
		else:
			print "You can't go that way."
		

	def do_east(self, obj):
		self.do_move('E')

	def do_west(self, obj):
		self.do_move('W')

	def do_north(self, obj):
		self.do_move('N')

	def do_south(self, obj):
		self.do_move('S')

	def go_room(self, newloc):
		self.location = newloc
		self.do_look()

	def do_look(self, obj=None):
		print self.location.desc
		print "Contains:", ", ".join([str(x) for x in self.location.objects])
		print "Exits: ", ", ".join(self.location.keys())


#	def postcmd(self, stop, line):
#		print "hola!"


player = Player(office)
player.cmdloop()
