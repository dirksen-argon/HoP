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
    def slow_type(string):
        '''
        Take a string and print it in a unique way dictated by codes in the string
            preceded by the "@" symbol.

        Parameters:
            string (str): The string that will be printed. May contain codes preceded
                by the escape character "@".
        '''

        # by default, the delay between letters printing is 10 milliseconds, though
        # the print() function is slow enough that it might functionally act as a longer
        # delay
        delay = 10

        # by default, the letters will be printed one at a time rather than all at once
        slow_typing = True

        # used to store chunks of output string before printing all characters at once
        output = ""

        # create an iterator of the input string
        string = iter(string)

        # for each character in the string, print it unless it is @, in which case
        # get the command afterwards and change the function of displaying the letters
        # accordingly
        for letter in string:

            # if the letter is the escape character "@", get the code and change
            # the function accordingly
            if letter == "@":

                # get the next letter in the string (or None if no more letters exist)
                letter = next(string, None)

                # error if the end of the string was reached as the code is incomplete
                assert letter != None, "The \"@\" symbol must have a code after it"

                # if the first character in the code is "d", change the delay between letters
                if letter == "d":

                    # used to store the code representing the new delay
                    new_delay = ""

                    # get the next four characters and combine them
                    for i in range(4):

                        # get the next letter, or None if end of string is reached
                        letter = next(string, None)

                        # error if end of string is reached before full code is collected
                        assert letter != None, "The @dXXXX command requires a four digit number, but instead hit the end of the text"

                        # append the new digit to the 4 digit code
                        new_delay += letter

                    # if the new delay (milliseconds) isn't a number throw an error
                    assert new_delay.isnumeric(), "The @dXXXX command requires a four digit number, not " + new_delay

                    # convert to an integer and set the delay
                    delay = int(new_delay)

                    # restart the loop, checking the next letter
                    continue

                # if the first character in the code is "@", print the "@" symbol
                elif letter == "@":

                    # do nothing, thus keeping "@" in the letter variable to be printed later
                    pass

                # if the first character in the code is "w", wait for the specified amount of milliseconds
                elif letter == "w":

                    # used to store the code as a string
                    wait = ""

                    # get the next four characters as the code for how long to wait
                    for i in range(4):

                        # get the next letter, or None if end of string is reached
                        letter = next(string, None)

                        # error if end of string is reached before full code is collected
                        assert letter != None, "The @wXXXX command requires a four digit number, but instead hit the end of the text"

                        # append the new digit to the wait digits
                        wait += letter

                    # error if wait isn't only comprised of digits
                    assert wait.isnumeric(), "The @wXXXX command requires a four digit number, not " + wait

                    # convert wait to an integer
                    wait = int(wait)

                    # sleep for "wait" milliseconds
                    sleep(0.001 * wait)

                    # restart the loop checking for the next character
                    continue

                # if the first character in the code is "s", stop slow typing and begin saving up letters to print at once
                elif letter == "s":

                    # stop slow typing
                    slow_typing = False

                    # restart the loop checking for the next character
                    continue

                # if the first character in the code is "o", print out all stored letters and begin slow typing again
                elif letter == "o":

                    # begin slow typing
                    slow_typing = True

                    # print out all stored letters
                    print(output, end="")

                    # clear stored letters
                    output = ""

                    # restart the loop checking for the next character
                    continue

                # if the first character in the code doesn't match a command, raise an error
                else:
                    # raise error
                    raise AssertionError("@" + letter + " is not a valid command")

            # if slow typing is enabled, print the single character then wait a delay
            if slow_typing:

                # print the current letter
                print(letter, end="")

                # wait for "delay" milliseconds
                sleep(0.001 * delay)

            # if slow typing is disabled, store letters to be printed at once later
            else:

                # store the current letter for later
                output += letter

        # print out any stored letters that haven't been printed yet
        print(output, end="")
        

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


