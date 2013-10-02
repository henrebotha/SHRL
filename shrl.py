'''SHRL (c) Henre Botha'''

#imports------------------------------------------------------------------------
from random import randint

#constants----------------------------------------------------------------------
TURN_TIME = [1200, 600, 400, 300, 240] #time to act for ag=1,2,3...

#class definitions--------------------------------------------------------------
class Person(object):
    '''A character (playable or not) in the game.'''
    def __init__(self, st=2, ag=2, re=2, name="Thug"):
        '''Stats: st(rength), ag(ility), re(silience).'''
        self.st, self.ag, self.re = int(st), int(ag), int(re)
        self.hp_max = re * 3
        self.hp = self.hp_max
        self.name = str(name)
        self.in_front = False
        self.alive = True

    def attack(self, target):
        if (randint(1,10) + self.ag - target.ag) > 5:
            print(self.name + " hits " + target.name + "!")
            target.hp -= self.st
            print(self.name + " deals " + str(self.st) + " damage.")
        else:
            print(self.name + " misses " + target.name + ".")

    def move(self):
        self.in_front ^= True
        if self.in_front == True:
            position = "front"
        else:
            position = "back"
        print(self.name + " moved to the " + position + ".")

    def take_action(self):
        valid_choice = False
        while valid_choice == False:
            i = input(self.name + "'s turn. [A]ttack or [M]ove? -> ")
            if i.lower()[0] == "a":
                print("Attacking!")
                valid_choice = True
            elif i.lower()[0] == "m":
                print("Moving!")
                self.move()
                valid_choice = True
        print()

#function definitions-----------------------------------------------------------
def combat(combatants):
    t = 0
    #while check_pulse(combatants) == False:
    while True:
        t += 10
        for i in range(len(combatants)):
            if t % TURN_TIME[combatants[i].ag - 1] == 0:
                combatants[i].take_action()
        if t % TURN_TIME[0] == 0:
            t = 0

def check_pulse(persons):
    '''See if anyone is still alive.'''
    if False in (p.alive for p in persons):
        return False
    else:
        return True

#main code----------------------------------------------------------------------
hero = Person(3, 3, 3, "Solar Man")
bad_guy = Person()

combat((hero, bad_guy))
