'''
Defines an agent mind that attacks any opponent agents within its view,
attaches itself to the strongest plant it finds, eats when its hungry, 
'''

import random, cells
import math
import pprint


class AgentMind(object):
    def __init__(self, junk):
       
        #initial setup parameters
        self.my_plant = None
        self.mode = 1
        self.target_range = random.randrange(50, 1000)

    def length(self, a, b):
        return int(math.sqrt((a * a) + (b * b)))

    #called on each frame 
    def act(self, view, msg):
      
        x_sum = 0
        y_sum = 0
        dir = 1
        me = view.get_me()
        mp = (mx, my)= me.get_pos()
    
        # Attack any opponents.
        opponentCount = 0 
        teamCount = 0
        for a in view.get_agents():
            if a.get_team() != me.get_team():
                opponentCount += 1
            else:
                teamCount += 1 


        #Only attack if we have superiority
        if opponentCount > 0:
            if teamCount < opponentCount:
                print 'call for help %s ' % str(mp)
                #Bring reinforcements
                msg.send_message((my,mx))

            print 'attack %s' % str(a.get_pos())
            return cells.Action(cells.ACT_ATTACK, a.get_pos())

        #Listen for reinforcement messages
        largestDiff = 100000
        targetX = 0
        targetY = 0
        msgCount = 0
        for m in msg.get_messages():
            (tx,ty) = m
            msgCount += 1

            #Is this the nearest one? 
            currentDiff = abs((tx - mx)) + abs((ty - my))
            if currentDiff < largestDiff:
                targetX = tx
                targetY = ty 
                largestDiff = currentDiff
        
        if msgCount > 0:
            moveToX = mx
            moveToY = my
            if mx > targetX:
                moveToX -= 1
            elif mx < targetX:
                moveToX += 1

            if my > targetY:
                moveToY -= 1
            elif my < targetY:
                moveToY += 1
        
            
            return cells.Action(cells.ACT_MOVE, (moveToX, moveToY))
            


        # Attach to the strongest plant found.
        if view.get_plants():
            plant = view.get_plants()[0]
            if not self.my_plant:
                self.my_plant = plant
            elif self.my_plant.eff < plant.eff:
                self.my_plant = plant
    
        # Eat if hungry or if this is an exceptionally energy-rich spot.
        hungry = (me.energy < self.target_range)
        energy_here = view.get_energy().get(mx, my)
        food = (energy_here > 0)
        if hungry and food or energy_here > 100:
            return cells.Action(cells.ACT_EAT)

        if self.my_plant:
            plant_pos = self.my_plant.get_pos()
            plant_dist = self.length(
                abs(mx - plant_pos[0]), 
                abs(my - plant_pos[1]))
            
            if (not me.loaded and
                (plant_dist % 5 or abs(mx - plant_pos[0]) < 2)
                and random.random() > 0.5):
                return cells.Action(cells.ACT_LIFT)
            if me.loaded and plant_dist % 5 == 0 and abs(mx - plant_pos[0]) >= 2:
                return cells.Action(cells.ACT_DROP)
            if me.energy < plant_dist * 1.5:
                (mx, my) = plant_pos
                pos = (mx + random.randrange(-1, 2), my + random.randrange(-1, 2))
                return cells.Action(cells.ACT_MOVE, pos)

        pos = (mx + random.randrange(-1, 2), my + random.randrange(-1, 2))
        action = cells.ACT_SPAWN if random.random() > 0.9 else cells.ACT_MOVE
        return cells.Action(action, pos)
