from json import loads              # for converting json to dict
from os.path import dirname, exists # for finding files
import sys                          # for sys.exit() for ending the program

class Room:
    '''
    Represents a text adventure scenario with multiple options for the user to pick from.

    Attributes:
        name (string): The name of the room and its corresponding .json file.
        text (string): The text displayed when the room is first entered.
        options (list[dict]): The options the user will choose from.
        flags (dict[string:list]): The flags keeping track of user choices organized into namespaces based on the room names
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
        assert isinstance(name, str), "name must be a string"

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

        # get room_text from json dict
        self.__text = room_dict["room_text"]  

        # initialize list of options
        self.__options = []
        
        # get options from json dict
        for option in room_dict["options"]:
            # add option to options list
            self.__options.append(option)


    def run(self):
        '''
        Describe the room to the user and allow them to interact using set options
        '''

        # print out the room's introduction text
        print(self.__text + "\n")

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

            # run the results of the choice
            running = self.__run_results(chosen_option)
            
                    
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

                # check each requirement
                for req in option["req"]:

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
                        
                    # if requirement starts with "!" and the following string is marked as a flag, requirement is not met
                    if req[0] == "!":
                        
                        if namespace in Room.__flags.keys() and req[1:] in Room.__flags[namespace]:
                            break   # stop checking requirements for this option
                        
                    # if requirement is not marked as a flag, requirement is not met
                    elif namespace not in Room.__flags.keys() or (namespace in Room.__flags.keys() and req not in Room.__flags[namespace]):
                        break   # stop checking requirements for this option
                    
                # if all requirements have been verified without issue, add the option to the shown_options list
                else:
                    
                    # add the option to the shown_options list
                    shown_options.append(option)
                    
            # if no requirements were specified, room passes all requirements
            else:
                
                # add the option to the shown_options list
                shown_options.append(option)

        # options are ordered by letter, so keep track of the current letter in ASCII from starting with "A"
        letter_ascii = ord("A")

        # display every option passing requirements to the user
        for option in shown_options:

            # if the corresponding letter to the option would be past "Z", stop showing options
            if letter_ascii > ord("Z"):
                break   # stop showing options

            # print the corresponding letter of the option to its left
            print(chr(letter_ascii), end=": ")

            # increment the letter by 1 up the alphabet
            letter_ascii += 1

            # print the option's text
            print(option["option_text"])

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
        

    def __run_results(self, option):
        '''
        Evaluate and run the results set to happen for the chosen option

        Parameters:
            option: an option to parse through and run the results of picking that option

        Returns:
            game_running (bool): Boolean value dictating whether to stop running the game
        '''

        # keep track of whether a result would end the game
        game_running = True
        
        # if there is "result_text" in our option, print it
        if "result_text" in option:
            
            # print the result_text
            print(option["result_text"] + "\n")

        # if there is a result list in our option, run each command in the list
        if "result" in option:
            
            # iterate through each command in the list
            for result in option["result"]:

                if "-" in result:
                    # split the command into a command-argument pair by splitting at the first "-"
                    command, argument = result.split("-", 2)
                else:
                    command = result
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

                    assert argument != "" and argument != "!", "The \"set\" command requires an argument and cannot be \"!\""
                    
                    # if the namespace for the new flag doesn't exist yet in the flag dict, create it
                    if not(namespace in Room.__flags.keys()):
                        
                        # create the namespace in the form of an empty list with the namespace name as the dict key
                        Room.__flags[namespace] = []
                        
                    # add the argument to the flags list as a flag
                    Room.__flags[namespace].append(argument)
                    
                    continue    # continue to the next command
                
                # if the command is "unset", remove a flag from the flags list if it exists
                elif command == "unset":

                    assert argument != "" and argument != "!", "The \"unset\" command requires an argument and cannot be \"!\""
                    
                    # if the namespace exists in the flag dict, remove all occurences of the argument flag
                    if namespace in Room.__flags.keys():
                        
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
                            user_input = input("Continue? (Y/N): ").upper()

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

                # if the command is not a valid command raise an error
                else:

                    # raise an error due to an invalid command
                    raise AssertionError(command + " is not a valid command")

        # return whether the game would end
        return game_running


