import os
import time


def intro():
    title = """                       .-'~~~-.
                     .'o  oOOOo`.
                    :~~~-.oOo   o`.
                     `. \ ~-.  oOOo.
                       `.; / ~.  OO:
                       .'  ;-- `.o.'
                      ,'  ; ~~--'~
                      ;  ;
_______\|/__________\\;_\\//___\|/________

        #######################
        #### Wild Foraging ####
        #######################
        
__________________________________________       

"""
    
    print(title)

    
def intro_question(player_choice1):
    
    print("You wake up and find yourself in the middle of the woods")
    time.sleep(2)
    
    print("You look around and see nothing but mountains, trees, wilderness, and the sound of running water close by")
    time.sleep(2)
    
    print("You see a bag on the ground and look inside")
    time.sleep(2)
    
    print("What do you find?")
    
    print("(A)Hatchet (B)Flare (C)Canteen (D)Compass")
    starting_tool = input("What do you choose?: ").upper()
    
    if starting_tool == "A":
        player_choice1['tool'] = 'Hatchet'
        print("You find a Hatchet in the bag. Lookin' sharp.")
        
    elif starting_tool == "B":
        player_choice1['tool'] = 'Flare'
        print("You find a Flare in the bag. Maybe shouldn't use it for a fireworks show")
        
    elif starting_tool == "C":
        player_choice1['tool'] = 'Canteen'
        print("You find a Canteen. Of course there's no water in it.")
        
    elif starting_tool == "D":
        player_choice1['tool'] = 'Compass'
        print("You find a Compass. Too bad you dont know where anything is.")
        
    else:
        print("That answer doesn't do anything pal")
    time.sleep(2)
    
    return player_choice1

def question2(player_choice1):
    
    print("You're walking towards the sound of running water")
    time.sleep(2)
    print("You sense something up ahead")
    time.sleep(2)
    print("Something is about to jump out at you!")
    time.sleep(2)
    
    attack = input("Do you to use the tool in your bag? (yes/no): ").lower()
    
    if player_choice1.get('tool') == 'Hatchet':
        if attack == 'yes':
            print("You swing at the lunging creature and hit your foot. The creature eats you")
        else:
            print("You were too slow anyways. The lunging creature eats your face")
    elif player_choice1.get('tool') == 'Flare':
        if attack == 'yes':
            print("You try to light the flare towards the creature. Instead it shoots back at your face and you die")
        else:
            print("Well, it was either death by fire or creature. You die.")
    elif player_choice1.get('tool') == 'Canteen':
        if attack == 'yes':
            print("Whats that supposed to do? The creature eats your face. You die.")
        else:
            print("If you had swung it really fast, you might have got it")
    elif player_choice1.get('tool') == 'Compass':
        if attack == 'yes':
            print("I mean, its better than nothing. You miss the throw though. You die by creature bite.")
        else:
            print("Maybe you should have thrown it in the direction of safety and followed that. You die.")
    else:
        print("You were going to die no matter what")
    time.sleep(2)
    
    return
    

def main():
    player_choice1 = {}
    intro()
    intro_question(player_choice1)
    question2(player_choice1)
    print("You did you best!")
    
if __name__ == "__main__":
    main()