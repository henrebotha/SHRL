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
            if target.hp <= 0:
                target.hp = 0
                target.alive = False
                print(target.name + " is knocked out!")
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
        if self.faction == "AI":
            self.take_action_npc(combatants)
        else:
            self.take_action_pc(combatants)

    def take_action_pc(self, combatants):
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

    def take_action_npc(self, combatants):
        '''NPC always chooses to attack the hero.'''
        self.attack(hero)


class Area(object):
    def __init__(self, inhabitants, name="Dark alley"):
        self.name = str(name)
        self.inhabitants = inhabitants

#function definitions-----------------------------------------------------------
def combat(area):
    '''The main combat loop.'''
    t = 0
    combatants = [hero]
    for i in area.inhabitants:
        combatants.append(i)
    print("As you step into " + area.name + ", you are attacked!")
    while check_pulse(combatants) == True:
        t += 10
        for i in range(len(combatants)):
            if t % TURN_TIME[combatants[i].ag - 1] == 0:
                if combatants[i].alive == True:
                    combatants[i].take_action(combatants)
        if t % TURN_TIME[0] == 0:
            t = 0
    else:
        if hero.alive == True:
            print("Your opponent finally keels over.")
            print("You make your way downtown...\n")

def check_pulse(persons):
    '''Returns True if everyone is still alive.'''
    if False in (p.alive for p in persons):
        return False
    else:
        return True

def get_target(combatants):
    '''The menu for choosing targets.'''
    print("Available targets:")
    for i in range(len(combatants)):
        print(str(i+1) + ". " + combatants[i].name,end="")
        print(" (hp: " + str(combatants[i].hp) + "/"
              + str(combatants[i].hp_max) + ")")
    valid_choice = False
    while valid_choice == False:
        t = input("Enter target #: -> ")
        t = int(t) - 1
        if (t) in range(len(combatants)):
            valid_choice = True
            return combatants[int(t)]

#main code----------------------------------------------------------------------
hero = Person(3, 3, 3, "Solar Man", faction="P1")

while hero.alive == True:
    area = Area([Person()])
    combat(area)
else:
    print("You fought bravely...\n\n---GAME OVER---")
