from reverend.thomas import Bayes


guesser = Bayes()

for each in ('north','south','east','west'):
    guesser.train('do_move', 'to the %s' % each)
    guesser.train('do_move', 'head %s' % each)
    guesser.train('do_move', 'spin %s' % each)
    
    # if we don't do this 'do_move' is going to get too dominant
    guesser.train('do_take', 'grab')
    guesser.train('do_take', 'grab the')
    guesser.train('do_take', 'pick up')
    guesser.train('do_take', 'pick up the')
    guesser.train('do_take', 'lift')
    guesser.train('do_take', 'lift the')
    guesser.train('do_take', 'fetch')
    guesser.train('do_take', 'fetch the')

bulk = """wear suit of armour
put on suit of armour
use armor
climb into armour
wear the armor
place armour on me
place armor on self"""
for line in bulk.splitlines():
    guesser.train('do_take', line)

guesser.save('commands.bays')
#print guesser.guess('fetch')
              
              