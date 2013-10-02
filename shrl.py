'''SHRL (c) Henre Botha'''

from random import randint

class Person(object):
    '''A character (playable or not) in the game.'''
    def __init__(self, st=2, ag=2, re=2, name="Thug"):
        '''Stats: st(rength), ag(ility), re(silience).'''
        self.st, self.ag, self.re = int(st), int(ag), int(re)
        self.hp_max = re * 3
        self.hp = hp_max
        self.name = str(name)

    def attack(self, target):
        if die_roll() == True:
            target.hp -= self.st
            print(self.name + " deals " + str(self.st) + " damage.")


def die_roll(agent, target):
    '''Calculates whether an attack hit successfully.'''
    r = randint(1,10)
    f = agent.ag - target.ag
    if r + f > 6:
        print(agent.name + " hits " + target.name + "!")
        return True
    else:
        print(agent.name + " misses " + target.name + ".")
        return False
