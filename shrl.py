'''SHRL (c) Henre Botha'''

#imports------------------------------------------------------------------------
from random import randint

#constants----------------------------------------------------------------------
TURN_TIME = [1200, 600, 400, 300, 240] #time to act for ag=1,2,3...

#class definitions--------------------------------------------------------------
class Person(object):
    '''A character (playable or not) in the game.'''
    def __init__(self, st=2, ag=2, re=2, name="Thug", player_controlled=False):
        '''Stats: st(rength), ag(ility), re(silience).'''
        self.st, self.ag, self.re = int(st), int(ag), int(re)
        self.hp_max = re * 3
        self.hp = self.hp_max
        self.name = str(name)
        self.player_controlled = player_controlled
        self.in_front = False
        self.alive = True
        self.defenders = [] #who's defending me
        self.defending = [] #who am I defending
        self.ai = {"turns since defend": 0}

    def attack(self, target):
        '''Attack an enemy!'''
        for i in target.defenders:
            i.counter(self, target)
        if self.alive == False:
            return
        if self.attack_roll(target) > 5:
            print(self.name + " hits " + target.name + "!")
            target.hp -= self.st
            print(self.name + " deals " + str(self.st) + " damage.")
            if target.hp <= 0:
                target.hp = 0
                target.alive = False
                print(target.name + " is knocked out!")
        else:
            print(self.name + " misses " + target.name + ".")

    def attack_roll(self, target):
        '''Calculate odds of hitting'''
        hit_factor = randint(1,10) + self.ag - target.ag
        if self.in_front == False:
            hit_factor -= 2 #it's harder to hit with melee if you're in the back
        return hit_factor
    
    def defend(self, target):
        '''Prepare to counter any attacks aimed at the target.'''
        target.defenders.append(self)
        self.defending.append(target)
        print(self.name + " is defending " + target.name + "...")
    
    def counter(self, target, recipient):
        '''Return an attack.'''
        print(self.name + " is countering!")
        self.attack(target)
        recipient.defenders.remove(self)
        self.defending.remove(recipient)

    def move(self):
        '''Change battlefield position.'''
        self.in_front ^= True
        if self.in_front == True:
            position = "front"
        else:
            position = "back"
        print(self.name + " moved to the " + position + ".")

    def turn_start(self):
        for i in self.defending:
            i.defenders.remove(self)
            self.defending.remove(i)
    
    def take_action(self, combatants):
        if self.player_controlled == False:
            self.take_action_npc(combatants)
        else:
            self.take_action_pc(combatants)

    def take_action_pc(self, combatants):
        '''Prompt the player for combat action.
        Takes a list of combatants as an argument.'''
        valid_choice = False
        while valid_choice == False:
            i = input(self.name + "'s turn. [A]ttack, [D]efend, or [M]ove? -> ")
            if i.lower()[0] == "a":
                print("Attacking!")
                target = get_target(combatants)
                self.attack(target)
                valid_choice = True
            elif i.lower()[0] == "d":
                print("Defending!")
                target = get_target(combatants)
                self.defend(target)
                valid_choice = True
            elif i.lower()[0] == "m":
                print("Moving!")
                self.move()
                valid_choice = True
            else:
                print("Invalid input.")
        print()

    def take_action_npc(self, combatants):
        '''NPC always chooses to attack the hero, except on first round.'''
        if self.in_front == False:
            self.move()
        else:
            if self.ai["turns since defend"] >= 2 and randint(1,5) >= 4:
                self.defend(self)
                self.ai["turns since defend"] = 0
            else:
                self.attack(hero)
                self.ai["turns since defend"] += 1


class Area(object):
    def __init__(self, inhabitants=[], name="Dark alley"):
        self.name = str(name)
        self.inhabitants = inhabitants
        if len(self.inhabitants) > 0:
            self.description = ("As you step into a " + self.name + ", a "
            + inhabitants[0].name + " attacks you!")
        else:
            self.description = ("This " + self.name
                                + " is completely devoid of activity.")

#function definitions-----------------------------------------------------------
def combat(area):
    '''The main combat loop.'''
    global score, progress
    t = 0
    combatants = [hero]
    for i in area.inhabitants:
        combatants.append(i)
    for i in combatants:
        i.in_front = False
    print(str(progress+1) + ". " + area.description)
    while check_pulse(combatants) == True:
        t += 10
        for i in range(len(combatants)):
            if t % TURN_TIME[combatants[i].ag - 1] == 0:
                if combatants[i].alive == True:
                    combatants[i].turn_start()
                    combatants[i].take_action(combatants)
        if t % TURN_TIME[0] == 0:
            t = 0
    else:
        if hero.alive == True:
            print("Your opponent finally keels over.")
            score += 100
            print("You make your way downtown...\n")

def event(area):
    global progress
    if len(area.inhabitants) > 0:
        combat(area)
    else:
        print(str(progress+1) + ". " + area.description)
        print("You move on...\n")
    progress += 1

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

def make_area():
    if randint(1,10) > 3:
        return Area([Person()])
    else:
        return Area()

def game_on(hero):
    global score
    while hero.alive == True:
        area = make_area()
        event(area)
    else:
        print("You fought bravely...\n\n---GAME OVER---")
        print("FINAL SCORE: " + str(score))


#main code----------------------------------------------------------------------
print("You wake in your apartment, aware of a new innate power.\n"
      + "What will your superhero name be?")
hero_name = input("Name: -> ")
hero = Person(3, 3, 3, hero_name, player_controlled=True)
score = 0
progress = 0
game_on(hero)
