import cells
import random

       

class AgentMind(object):

    def __init__(self, junk):
        if random.random() > 0.2:
            self.state = self.eater()
        else:
            self.state = self.explorer()
        self.state.next()
        
    def act(self, view, msg):
        return self.state.send((view, msg))

    def eater(self):
        yield 1
        while True:
            view, msg = yield cells.Action(cells.ACT_EAT)
            me = view.get_me()
            agents = view.get_agents()
            plants = view.get_plants()
#            print me.x, me.y, me.energy, me.loaded
            view, msg = yield cells.Action(cells.ACT_MOVE, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1)))
            view, msg = yield cells.Action(cells.ACT_MOVE, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1)))
            view, msg = yield cells.Action(cells.ACT_SPAWN, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1), self))  
            view, msg = yield cells.Action(cells.ACT_EAT)
            view, msg = yield cells.Action(cells.ACT_MOVE, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1)))
            view, msg = yield cells.Action(cells.ACT_MOVE, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1)))


    def explorer(self):
        yield 1
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        distance = random.randint(10, 100)

        for x in xrange(distance):
            view, msg = yield cells.Action(cells.ACT_EAT)
            me = view.get_me()
            view, msg = yield cells.Action(cells.ACT_MOVE, (me.x + dx, me.y + dy))

        while True:  
            view, msg = yield cells.Action(cells.ACT_EAT)
            me = view.get_me()
            view, msg = yield cells.Action(cells.ACT_SPAWN, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1), self))  
            view, msg = yield cells.Action(cells.ACT_MOVE, (me.x+random.randint(-1, 1), me.y+random.randint(-1, 1)))

