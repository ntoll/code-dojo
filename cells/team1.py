import random,cells

class AgentMind:
  def __init__(self, args):
    # decide if you're a sitting Buddha or hungry ghost
    self.buddha = (random.random() > 0.9)
    self.my_plant = None
    self.target_range = random.randrange(100,300)

  def act(self,view,msg):
    me = view.get_me()
    mp = (mx,my)= me.get_pos() 

    if self.buddha:
      # sit
      if (random.random()>0.99):
	# Chance of spawning
        return cells.Action(cells.ACT_SPAWN,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))
      else:
	return cells.Action(cells.ACT_MOVE, me.get_pos())
    else:
      # Hungry Ghost

      # 1. Find best food
      if len(view.get_plants()) > 0:
      	if (not self.my_plant):
      	  self.my_plant = view.get_plants()[0]
      	elif self.my_plant.get_eff()<view.get_plants()[0].get_eff():
      	  self.my_plant = view.get_plants()[0]

      # 2. Eat it 
      if (me.energy < self.target_range) and (view.get_energy().get(mx, my) > 0):
        return cells.Action(cells.ACT_EAT)

      # If we have a plant in our sights
      if self.my_plant:
        dist = max(abs(mx-self.my_plant.get_pos()[0]),abs(my-self.my_plant.get_pos()[1]))
        if me.energy < dist*1.2:
	  # If it's woth getting to th plant then go there and eat it
          (mx,my) = self.my_plant.get_pos()
          return cells.Action(cells.ACT_MOVE,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))

      if (random.random()>0.8888):
	# Chance of spawning
        return cells.Action(cells.ACT_SPAWN,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))
      else:
	# if not spawning then move
        return cells.Action(cells.ACT_MOVE,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))
