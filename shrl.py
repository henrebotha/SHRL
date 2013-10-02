'''SHRL (c) Henre Botha'''

#imports------------------------------------------------------------------------
from random import randint

#constants----------------------------------------------------------------------
TURN_TIME = [1200, 600, 400, 300, 240] #time to act for ag=1,2,3...

#class definitions--------------------------------------------------------------
class Person(object):
    '''A character (playable or not) in the game.'''
    def __init__(self, st=2, ag=2, re=2, name="Thug", faction="AI"):
        '''Stats: st(rength), ag(ility), re(silience).'''
        self.st, self.ag, self.re = int(st), int(ag), int(re)
        self.hp_max = re * 3
        self.hp = self.hp_max
        self.name = str(name)
        self.faction = faction
        self.in_front = False
        self.alive = True

    def attack(self, target):
        '''Attack an enemy!'''
        if (randint(1,10) + self.ag - target.ag) > 5:
            print(self.name + " hits " + target.name + "!")
            target.hp -= self.st
            print(self.name + " deals " + str(self.st) + " damage.")
        else:
            print(self.name + " misses " + target.name + ".")

    def move(self):
        '''Change battlefield position.'''
        self.in_front ^= True
        if self.in_front == True:
            position = "front"
        else:
            position = "back"
        print(self.name + " moved to the " + position + ".")

    def take_action(self, combatants):
        '''Prompt the player for combat action.
        Takes a list of combatants as an argument.'''
        valid_choice = False
        while valid_choice == False:
            i = input(self.name + "'s turn. [A]ttack or [M]ove? -> ")
            if i.lower()[0] == "a":
                print("Attacking!")
                target = get_target(combatants)
                self.attack(target)
                valid_choice = True
            elif i.lower()[0] == "m":
                print("Moving!")
                self.move()
                valid_choice = True
            else:
                print("Invalid input.")
        print()

#function definitions-----------------------------------------------------------
def combat(combatants):
    '''The main combat loop.'''
    t = 0
    while check_pulse(combatants) == True:
        t += 10
        for i in range(len(combatants)): #BUG: won't stop dead units from acting
            if t % TURN_TIME[combatants[i].ag - 1] == 0:
                combatants[i].take_action(combatants)
        if t % TURN_TIME[0] == 0:
            t = 0
    else:
        print("---GAME OVER---")

def check_pulse(persons):
    '''Returns True if everyone is still alive.'''
    if False in (p.alive for p in persons):
        return False
    else:
        return True

def get_target(combatants):
    print("Available targets:")
    for i in range(len(combatants)):
        print(str(i+1) + ". " + combatants[i].name)
    valid_choice = False
    while valid_choice == False:
        t = input("Enter target #: -> ")
        t = int(t) - 1
        if (t) in range(len(combatants)):
            valid_choice = True
            return combatants[int(t)]

#main code----------------------------------------------------------------------
hero = Person(3, 3, 3, "Solar Man", faction="P1")
bad_guy = Person()

everyone = [hero, bad_guy]

combat(everyone)
