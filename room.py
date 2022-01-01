from json import loads              # for converting json to dict
from os.path import dirname, exists # for finding files
import sys                          # for sys.exit() for ending the program
from random import choice           # for running the random command
from functions import slow_type     # for printing text in specific ways

class Room:
    '''
    Represents a text adventure scenario with multiple options for the user to pick from.

    Attributes:
        __name (string): The name of the room and its corresponding .json file.
        __text (string): The text displayed when the room is first entered.
        __options (list[dict]): The options the user will choose from.
        __constants (list[?]): List of constants to be utilize by commands.
        __flags (dict[string:list]): The flags keeping track of user choices organized into namespaces based on the room names
    '''

    # initialize dict of flags
    __flags = {}

    def __init__(self, name):
        '''
        The constructor for Room class.

        Paramaters:
            name (string): The name of the room and its corresponding .json file
        '''

        #
        # verify that the room name is valid
        #

        # ensure name is a string
        assert isinstance(name, str), "room name must be a string"

        # ensure json file matching name exists
        assert exists(dirname(__file__) + "/" + name + ".json"), "no file named \"" + name + ".json\" at " + dirname(__file__)


        #
        # get attributes from json file
        #

        # open json file
        json_handle = open(name + ".json", "r")

        # get text from json file
        room_json = json_handle.read()

        # close json file
        json_handle.close()

        # convert json text to dictionary
        room_dict = loads(room_json)

        # set name of room
        self.__name = name

        # get room_text from json dict if it exists
        if "room_text" in room_dict:

            # get the room text
            self.__text = room_dict["room_text"]

        # if there is no room text, note that
        else:

            # there is no room text
            self.__text = None

        # initialize list of options
        self.__options = []

        # error if no options list in the json
        assert "options" in room_dict, "A list of options is mandatory to run a room"
        
        # get options from json dict
        for option in room_dict["options"]:
            
            # add option to options list
            self.__options.append(option)

        # initialize list of constants
        self.__constants = {}

        # get constants from the json dict
        if "constants" in room_dict.keys():

            # error if "constants" isn't a list as intended
            assert isinstance(room_dict["constants"], dict), "\"constants\" must be a a dictionary"

            # add every constant to the constants dict
            for constant in room_dict["constants"].keys():

                # add the constant to the constants dict
                self.__constants[constant] = room_dict["constants"][constant]

        # if there are commands to run on startup, run them
        if "commands" in room_dict.keys():

            # error if "commands" is not a list
            assert isinstance(room_dict["commands"], list), "\"commands\" must be a list"

            # run the startup commands
            self.__run_results(room_dict["commands"][:])
                

    def run(self):
        '''
        Describe the room to the user and allow them to interact using set options
        '''

        # print out the room's introduction text
        if self.__text:
            slow_type(self.__text + "\n\n")

        # show options and get user input, loop until done with room
        running = True  # flag for loop
        while (running):    

            #display options to the user
            shown_options = self.__display_options()

            # get input from the user
            chosen_option = self.__get_input(shown_options)

            # if input was not gotten successfully, restart loop to try again
            if not(chosen_option):

                # restart loop
                continue
            
            # if there is "result_text" in our option, print it
            if "result_text" in chosen_option:
                
                # print the result_text
                slow_type(chosen_option["result_text"] + "\n\n")

            # if there is a result list in our option, run each command in the list
            if "result" in chosen_option:

                # get the list of commands
                results = chosen_option["result"][:]

                # error if results isn't a list
                assert isinstance(results, list), "\"result\" must be a list"
                
                # run the results of the choice
                running = self.__run_results(results, chosen_option)
            
                    
    def __display_options(self):
        '''
        display the user's options

        Returns:
            shown_options (list[dict]): list of options that have been shown to the player
        '''
        
        # initialize list of options that meet all requirements and can be shown to players
        shown_options = []

        # check if each option's requirements are met
        for option in self.__options:

            # if option has requirements, verify they are met
            if "req" in option:

                # if requirements are met, append the option to be displayed later
                if self.__check_requirements(option["req"]):

                    # append the option so that it is displayed later
                    shown_options.append(option)

            # if there are no requiremnts, requirements are assumed to be met
            else:

                # requirements are met
                shown_options.append(option)

        # error if no options to show
        assert len(shown_options) > 0, "No options met the requrements to be shown. At least one option must be able to be shown"

        # options are ordered by letter, so keep track of the current letter in ASCII from starting with "A"
        letter_ascii = ord("A")

        # display every option passing requirements to the user
        for option in shown_options:

            # if the corresponding letter to the option would be past "Z", stop showing options
            if letter_ascii > ord("Z"):
                break   # stop showing options

            # print the corresponding letter of the option to its left
            slow_type(chr(letter_ascii) + ": ")

            # increment the letter by 1 up the alphabet
            letter_ascii += 1

            # print the option's text
            slow_type(option["option_text"] + "\n")

        # return the list of options shown to the user
        return shown_options
    

    def __get_input(self, shown_options):
        '''
        get input from the user

        Parameters:
            shown_options (list[dict]): list of options in JSON that the user can pick from

        Returns:
            option (dict): option chosen by the user
        '''
        
        # get input from user and convert to uppercase
        user_input = input("\n").upper()

        # print a newline
        print()

        # validate user input
        # if user input is not a single character
        if len(user_input) != 1:
            return False    # reprint options and get user input again
        
        # if user input is not in the range A-? where ? is the letter corresponding to the last printed option
        elif ord(user_input) < ord("A") or ord(user_input) > ord("A") + len(shown_options) - 1:
            return False    # reprint options and get user input again

        # convert user input to an index and get the corresponding option
        option = shown_options[ord(user_input) - ord("A")]

        # return the option the user picked
        return option
        

    def __run_results(self, results, option={}):
        '''
        Evaluate and run the results set to happen for the chosen option

        Parameters:
            option: an option to parse through and run the results of picking that option

        Returns:
            game_running (bool): Boolean value dictating whether to stop running the game
        '''

        # keep track of whether a result would end the game
        game_running = True
            
        # iterate through each command in the list
        for result in results:

            # error if command isn't a string
            assert isinstance(result, str), "commands in the result list must be strings, not " + str(type(result))

            # remove spaces from the command
            result = result.replace(" ", "")

            if "-" in result:
                
                # split the command into a command-argument pair by splitting at the first "-"
                command, argument = result.split("-", 2)

            # if no argument is given, count it as ""
            else:

                # keep the command
                command = result

                # count the argument as ""
                argument = ""

            # if the argument has a ":" in it, split it into its namespace and argument
            if ":" in argument:
                
                # get the namespace (left of the ":") and the argument (right of the ":")
                namespace, argument = argument.split(":", 2)

                # verify that there are no more colons
                assert ":" not in argument, "too many \":\" in flag " + flag
                
            # if there is no ":" in the argument, then the namespace is the same as the room name
            else:
                
                # the namespace is the same as the room's name
                namespace = self.__name

            # if the command is "set", add the argument to the flags list as a flag to keep track of it
            if command == "set":

                # if the namespace for the new flag doesn't exist yet in the flag dict, create it
                if namespace not in Room.__flags.keys():

                    # create the namespace in the form of an empty list with the namespace name as the dict key
                    Room.__flags[namespace] = []

                # if there is no argument, set the namespace rather than an individual flag
                if argument != "":

                    # error if argument is "!"
                    assert argument != "!", "The \"set\" command argument cannot be \"!\""
                        
                    # add the argument to the flags list as a flag
                    Room.__flags[namespace].append(argument)
                
                continue    # continue to the next command
            
            # if the command is "unset", remove a flag from the flags list if it exists
            elif command == "unset":

                # error if argument is "!"
                assert argument != "!", "The \"unset\" command argument cannot be \"!\""
                
                # if the namespace exists in the flag dict, remove all occurences of the argument flag
                if namespace in Room.__flags.keys():

                    # if no argument, delete the entire namespace
                    if argument == "":

                        # delete the namespace
                        del Room.__flags[namespace]

                    # if there is an argument, remove occurences of it from the namespace
                    else:
                        
                        # while there are occurences of the argument flag, remove them
                        while argument in Room.__flags[namespace]:
                            
                            # remove an occurence of the argument flag
                            Room.__flags[namespace].remove(argument)
                            
                continue    # continue to the next command

        # if hte command is "reset", end the game
            elif command == "reset":

                # if no argument is given, assume it is intended to be "game"
                argument = "game" if argument == "" else argument

                # if the argument is "game", end the game
                if argument == "game":

                    # get input from the user regarding whether to replay or quit
                    getting_input = True    # True while user hasn't yet inputted valid input
                    while getting_input:

                        # get input from user
                        slow_type("Continue? (Y/N): ")
                        user_input = input().upper()

                        # make sure input is "Y" or "N"
                        getting_input = False if isinstance(user_input, str) and (user_input == "Y" or user_input == "N") else True

                    # if the user inputted "Y", restart the game by ending all running rooms but keeping the program running
                    if user_input == "Y":

                        # removing all active flags
                        Room.__flags = {}
                            
                        # end all running rooms but keeps program running
                        game_running = False

                        # print newline
                        print()

                    # if the user inputted "N", end the program
                    else:

                        # end the program
                        sys.exit()

                # if the argument is invalid raise an error
                else:
                    
                    # raise an error due to invalid argument
                    raise AssertionError(argument + " is not a valid argument of reset")

            # if the quit command is run, exit the program
            elif command == "quit":

                # if the quit command has any arguments, raise an error
                assert argument == "", argument + " is not a valid argument of \"quit\""

                # exit the program
                sys.exit()

            # if the command is "move", stop running the current room and run a new room
            elif command == "move":

                assert argument != "", "argument for \"move\" cannot be empty"

                # create a new room with argument being the room's name
                next_room = Room(argument)

                # run the new room
                next_room.run()

                # stop running the current room
                game_running = False

            # if the command is "print", print out a string with the argument as its name
            elif command == "print":

                # error if there is no argument
                assert argument != "", "the \"print\" command requires an argument"

                # check if the target text is in the curretn option
                if argument in option:

                    # store the found text
                    text = option[argument]

                # check if the target text is in the constants dictionary
                elif argument in self.__constants.keys():

                    # store the found text
                    text = self.__constants[argument]

                # error if argument doesn't match any element in the option object or constants dict
                else:

                    # raise error
                    raise AssertionError("Cannot print " + argument + " as it does not exist")

                # error if argument is not the label of a string
                assert isinstance(text, str), "The argument for \"print\" must be the label of a string, not a " + str(type(text))

                # print out the string
                slow_type(text + "\n\n")

            # if the command is "random", choose a random set of commands and run them
            elif command == "random":

                # error if no argument for "random" command
                assert argument != "", "the \"random\" command requires an argument"

                # check if table is in option object
                if argument in option:

                    # get table from option object
                    table = option[argument]

                # check if table is in constants dictionary
                elif argument in self.__constants.keys():

                    # get table from constants dictionary
                    table = self.__constants[argument]
                    
                # error if no random table matching argument
                else:

                    # raise error
                    raise AssertionError("Cannot find random table: \"" + argument + "\"")

                # error if random table is not a list
                assert isinstance(table, list), argument + " must be the label of a list, not a " + str(type(table))

                # create list for storing each occurence of lists of commands to be chosen randomly
                bag = []

                # add each command list to the random bag taking into accout its weight
                for random_group in table:

                    # if weight is an attribute, use it to set the weight | weight is the relative likelihood of a list being chosen
                    if "weight" in random_group:

                        # error if weight is not an integer
                        assert isinstance(random_group["weight"], int), "weight must be an integer, not a " + str(type(random_group["weight"]))

                        # set weight from the JSON
                        weight = random_group["weight"]

                    # if weight is not specified, set it to 1
                    else:
                        
                        # set the weight to 1
                        weight = 1

                    # if there are requirements tied to this group, verify they are met
                    if "req" in random_group:

                        # error if req is not a list
                        assert isinstance(random_group["req"], list), "\"req\" must be the name of a list, not a " + str(type(random_group["req"]))

                        # check the requirements of the random group
                        requirements_met = self.__check_requirements(random_group["req"])

                    # if there are no requiremnts, then requirements are assumed to be met
                    else:

                        # requirements are met
                        requirements_met = True

                    # if requirements are not met, do not use this random group
                    if requirements_met == False:

                        # set weight to 0, effectivly preventing this group from being used
                        weight = 0

                    # error if no commands list
                    assert "commands" in random_group, "Every object in a random table must have a \"commands\" list"

                    # error if commands list is not a list
                    assert isinstance(random_group["commands"], list), "\"commands\" must be a list, not a " + str(type(random_group["commands"]))

                    # add 1 occurence of the command list for every weight point
                    for i in range(weight):

                        # add an occurence of the command list to the random bag
                        bag.append(random_group["commands"])

                # error if the bag is empty
                assert bag != [], "No choices were found in random table: " + argument

                # get a random command list from the bag
                chosen_command_list = choice(bag)

                # add the commands from the randomly selected command list to the list of commands running right now
                results += chosen_command_list

            # if the command is not a valid command raise an error
            else:

                # raise an error due to an invalid command
                raise AssertionError(command + " is not a valid command")

        # return whether the game would end
        return game_running

    def __check_requirements(self, requirements):

        # check each requirement
        for req in requirements:

            # make sure req isn't empty
            assert req != "", "empty strings in JSON req lists are not allowed"

            # make sure req isn't an exclamation mark
            assert req != "!", "\"\!\" is used for inverting requirements and is not allowed by itself in a JSON req list"

            # if there is a ":" in the requirement, its flag is under a different namespace
            if ":" in req:
                
                # get the namespace (left of the ":") and the requirement (right of the ":")
                namespace, req = req.split(":", 2)

                # make sure there are no more colons
                assert not(":" in req), "too many \":\" in requirement " + req
                
            # if there isn't a ":", the namespace is the same as the Room name
            else:
                
                # set the namespace to be the room's name
                namespace = self.__name
                
            # if requirement is empty, check if the namespace exits instead
            if req == "":

                # if the first character is "!", requirement is met if namespace doesn't exist
                if namespace[0] == "!":

                    # the namespace is everything but the first "!"
                    namespace = namespace[1:]

                    # if the namespace exists, the requirement isn't met
                    if namespace in Room.__flags.keys():
                        break   # stop checking requirements for this option

                # if the first character isn't "!", requirement is met if namespace exists
                else:

                    # if namespace doesn't exist, requirement isn't met
                    if namespace not in Room.__flags.keys():
                        break   # stop checking requirements for this option
                    
            # if requirement starts with "!" and the following string is marked as a flag, requirement is not met
            elif req[0] == "!":

                if namespace in Room.__flags.keys() and req[1:] in Room.__flags[namespace]:
                    break   # stop checking requirements for this option
                
            # if requirement is not marked as a flag, requirement is not met
            elif namespace not in Room.__flags.keys() or (namespace in Room.__flags.keys() and req not in Room.__flags[namespace]):
                break   # stop checking requirements for this option
            
        # if all requirements have been verified without issue, add the option to the shown_options list
        else:

            # return True as all requirments were met
            return True

        # return False as at least one requirment is not met
        return False
