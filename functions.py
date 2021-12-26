if __name__ != "__main__":

    import json
    from time import sleep
    from random import choice
    
    # "slow_type" used for text scroll. Default speed can be
    # altered by ending a string, typing a comma, and then
    # entering a number. Note that the new number represents
    # the space bewteen letters, not the speed of the letters.
    # Higher numbers result in slower speeds, and vice-versa.
    # "slow_type does not accept input() statements, so
    # always put those outisde of it.
    def slow_type(string, speed = 0.01):
        for letter in string:
            print(letter, end = "")
            sleep(speed)
        
    # "pick_door" used to pick out singular doors. Not used in the starting
    # room or the elevator room, but used most other places.
    def pick_door(current_room):
        file = open("Test HoP data.json", "r")
        doors = json.loads(file.read())
        file.close()
        if current_room == "red":
            x = (1, 2, 3, 4, 5)
        elif current_room == "green":
            x = (0, 2, 3, 4, 5)
        elif current_room == "purple":
            x = (0, 1, 3, 4, 5)
        elif current_room == "yellow":
            x = (0, 1, 2, 4, 5)
        elif current_room == "blue":
            x = (0, 1, 2, 3, 5)
        elif current_room == "brown":
            x = (0, 1, 2, 3, 4)
        else:
            x = (0, 1, 2, 3, 4, 5)
        y = choice(x)
        door = doors["Doors"][y]
        return door

    # "pick_box" used to put random items into the boxes. There aren't
    # many items, but then there aren't many boxes. Unlike "pick_door",
    # "pick_box" has to check if the item is already in the player's
    # inventory, which are then eliminated as options by the .pop command.
    def pick_box(backpack):
        file = open("Test HoP data.json", "r")
        box_items = json.loads(file.read())
        file.close()
        x = [0, 1, 2, 3, 4, 5]
        for thing in backpack:
            if "Dagger" == thing:
                x.pop(0)
            if "Hatchet" == thing:
                x.pop(1)
            if "Nightstick" == thing:
                x.pop(2)
        y = choice(x)
        box = box_items["Box_Items"][y]
        return box
else:
    print("Huh? This file is running? Why is this file running? Has there been some \n" + \
          "mistake? Who are you? Why did you try to run the functions file? Don't \n" + \
          "you want to play the game? Open the game you fool! It's the one labeled \n" + \
          "\"main\" if you're really THAT lost. I mean, have to lost your mind? Are \n" + \
          "you stupid? No really, are you STUPID? WHO GAVE YOU PERMISSION TO RUN THIS?\n" + \
          "I spend years making a game, fine-tuning it for you, balancing it, and \n" + \
          "pain-stakingly writing in EACH and EVERY choice you get to make, AND YOU \n" + \
          "OPEN THE FUNTIONS FILE??!!!!\n\n" + \

          "Sorry. It's just been a little rough for me lately. Grandmother died last \n" + \
          "night. I mean, I wasn't sad-sad, I was more just sad for my dad. She was \n" + \
          "HIS mother, see. Apparently a pretty sweet woman, though I've also heard \n" + \
          "she had her downsides? Like, apparently she was super protective of her \n" + \
          "oven for some reason. Like, whenever my dad or any of his siblings got \n" + \
          "close to it she'd bash them over the head with a wooden spoon. Kinda \n" + \
          "me wonder why he loved her so much...? Anyway, he was super sad 'n shit \n" + \
          "and I just feel really bad for him. He was in a super good mood today, \n" + \
          "but I think he's faking it because he's never in a good mood before work. \n" + \
          "Makes be kinda scared to get a job myself, if I'm completely honest. Like, \n" + \
          "what do you even do in a job? Is it like school, but you actually get a \n" + \
          "reward for binding your personality and forcing yourself to be happy about \n" + \
          "it? Grown-ups are weird. I hope I never become one. What was I talking \n" + \
          "about again? Right, grandma. She was always really nice to me, though I \n" + \
          "didn't get to see her much. I remember before she died, like, she was in \n" + \
          "the hospital 'n shit and she gave me a kiss on the cheek and it felt like \n" + \
          "getting kissed by wax paper. Why do old people feel like wax paper? I always \n" + \
          "expected wrinkles to feel really rough, but it just feels weird.\n\n" + \

          "Anyways, yeah, this isn't the game. Good try though!")
