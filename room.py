from json import loads, dumps       # for converting json to dict and vice versa
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

        # -------------------
        # get json from files
        # -------------------

        # FIND AND GET DATA FROM ROOM JSON FILE

        # ensure name is a string
        assert isinstance(name, str), "room name must be a string"
        # ensure json file matching name exists
        assert exists(dirname(__file__) + "/rooms/" + name + ".json"), "no file named \"" + name + ".json\" at " + dirname(__file__)
        # open json file
        json_handle = open(dirname(__file__) + "/rooms/" + name + ".json", "r")
        # get text from json file
        room_json = json_handle.read()
        # close json file
        json_handle.close()

        # -------------------------------------
        # asign values from json where needed
        # name, text, flags, options, constants
        # -------------------------------------

        # NAME
        room_dict = loads(room_json)    # convert json text to dictionary
        self.__name = name              # set name of room


        # TEXT
        self.__text = room_dict["room_text"] if "room_text" in room_dict else None  # get room_text from json dict if it exists


        # FLAGS
        # if data.json exists, get its flags for Room.__flags
        if exists(dirname(__file__) + "/data.json"):
            data_handle = open("data.json", "r")    # open data.json 
            data_json = data_handle.read()          # get the text from data.json
            Room.__flags = loads(data_json)         # convert to dict and use it to set Room.__flags


        # OPTIONS
        self.__options = []                                                             # initialize list of options
        assert "options" in room_dict, "A list of options is mandatory to run a room"   # error if no options list in the json
        
        # get options from json dict
        for option in room_dict["options"]:            
            self.__options.append(option)   # add option to options list


        # CONSTANTS
        self.__constants = {}   # initialize list of constants
        
        # get constants from the json dict
        if "constants" in room_dict.keys():
            assert isinstance(room_dict["constants"], dict), "\"constants\" must be a a dictionary" # error if "constants" isn't a list as intended
            
            # add every constant to the constants dict
            for constant in room_dict["constants"].keys():
                self.__constants[constant] = room_dict["constants"][constant]   # add the constant to the constants dict


        # --------------------
        # run startup commands
        # --------------------

        # if there are commands to run on startup, run them
        if "commands" in room_dict.keys():
            assert isinstance(room_dict["commands"], list), "\"commands\" must be a list"                   # error if "commands" is not a list
            command_result = self.__run_results(room_dict["commands"][:])                                   # run the startup commands
            assert command_result == True, "commands such as reset are not allowed at startup of a room"    # error if disallowed command is run

        # ---------------------
        # display the room text
        # ---------------------

        # print out the room's introduction text
        if self.__text:
            slow_type(self.__text + "\n\n")




    def run(self):
        '''
        Describe the room to the user and allow them to interact using set options
        '''

        # ---------------------------
        # run game loop for this room
        # ---------------------------

        running = True  # flag for loop
        # show options and get user input, loop until done with room
        while (running):    


            # -------------------------
            # show the user the options
            # -------------------------
            
            #display options to the user
            shown_options = self.__display_options()


            # --------------
            # get user input
            # --------------

            # get input from the user
            chosen_option = self.__get_input(shown_options)

            # ------------------------------------------
            # carry out the results of the chosen option
            # print the text, run the commands
            # ------------------------------------------

            # PRINT THE TEXT
            # if there is "result_text" in our option, print it
            if "result_text" in chosen_option:                
                slow_type(chosen_option["result_text"] + "\n\n")    # print the result_text

            # RUN THE COMMANDS
            # if there is a result list in our option, run each command in the list
            if "result" in chosen_option:
                results = chosen_option["result"][:]                            # get the list of commands
                assert isinstance(results, list), "\"result\" must be a list"   # error if results isn't a list              
                running = self.__run_results(results, chosen_option)            # run the results of the choice
            


  
    def __display_options(self):
        '''
        display the user's options

        Returns:
            shown_options (list[dict]): list of options that have been shown to the player
        '''

        
        # -------------------------------------
        # check the requirements of the options
        # -------------------------------------

        shown_options = []  # initialize list of options that meet all requirements and can be shown to players

        # check if each option's requirements are met
        for option in self.__options:

            # if option has requirements, verify they are met
            if "req" in option:

                # if requirements are met, append the option to be displayed later
                if self.__check_requirements(option["req"]):
                    shown_options.append(option)    # append the option so that it is displayed later

            # if there are no requiremnts, requirements are assumed to be met
            else:
                shown_options.append(option)    # requirements are met

        assert len(shown_options) > 0, "No options met the requrements to be shown. At least one option must be able to be shown"   # error if no options to show


        # -----------------------------
        # print out the options
        # print options, return options
        # -----------------------------

        # PRINT OPTIONS
        letter_ascii = ord("A") # options are ordered by letter, so keep track of the current letter in ASCII from starting with "A"

        # display every option passing requirements to the user
        for option in shown_options:

            # if the corresponding letter to the option would be past "Z", stop showing options
            if letter_ascii > ord("Z"):
                break   # stop showing options

            slow_type(chr(letter_ascii) + ": ")     # print the corresponding letter of the option to its left
            letter_ascii += 1                       # increment the letter by 1 up the alphabet
            slow_type(option["option_text"] + "\n") # print the option's text

        # RETURN OPTIONS
        return shown_options    # return the list of options shown to the user
    



    def __get_input(self, shown_options):
        '''
        get input from the user

        Parameters:
            shown_options (list[dict]): list of options in JSON that the user can pick from

        Returns:
            option (dict): option chosen by the user
        '''


        # ------------------------------
        # loop until we have valid input
        # loop, return input
        # ------------------------------
        
        # LOOP
        valid_input = False # flag for running loop

        # loop until valid input is obtained from the user
        while not(valid_input):


            # --------------
            # get user input
            # --------------
            
            user_input = input("\n").upper()            # get input from user and convert to uppercase
            user_input = user_input.replace(" ", "")    # remove spaces
            print()                                     # print a newline


            # -------------------
            # validate user input
            # -------------------

            # if user input is not a single character
            if len(user_input) != 1:
                continue # reprint options and get user input again
            
            # if user input is not in the range A-? where ? is the letter corresponding to the last printed option
            elif ord(user_input) < ord("A") or ord(user_input) > ord("A") + len(shown_options) - 1:
                continue # reprint options and get user input again

            option = shown_options[ord(user_input) - ord("A")]  # convert user input to an index and get the corresponding option
            valid_input = True                                  # valid input is obtained so we can stop looping

        # RETURN INPUT
        return option   # return the option the user picked


    

    def __run_results(self, results, option={}):
        '''
        Evaluate and run the results set to happen for the chosen option

        Parameters:
            results (list[str]): List of commands to run
            option (dict[???]): Dictionary that may contain values affecting certain commands

        Returns:
            game_running (bool): Boolean value dictating whether to stop running the game
        '''

        # ----------------
        # run each command
        # ----------------
        
        game_running = True # keep track of whether a result would end the game
            
        # iterate through each command in the list
        for result in results:

            
            assert isinstance(result, str), "commands in the result list must be strings, not " + str(type(result)) # error if command isn't a string
            result = result.replace(" ", "")                                                                        # remove spaces from the command
            command, argument = result.split("-", 2) if "-" in result else (result, "")                             # split the result into a command and an argument

            # if the argument has a ":" in it, split it into its namespace and argument
            if ":" in argument:
                namespace, argument = argument.split(":", 2)                    # get the namespace (left of the ":") and the argument (right of the ":")
                assert ":" not in argument, "too many \":\" in flag " + flag    # verify that there are no more colons
                
            # if there is no ":" in the argument, then the namespace is the same as the room name
            else:
                namespace = self.__name # the namespace is the same as the room's name


            # if the command is "set", add the argument to the flags list as a flag to keep track of it
            if command == "set":
                self.__set(namespace, argument) # set the flag/namespace
                continue                        # continue to the next command
            
            # if the command is "unset", remove a flag from the flags list if it exists
            elif command == "unset":
                self.__unset(namespace, argument)   # unset the flag/namespace
                continue                            # continue to the next command
            
            # if the command is "reset", end the game
            elif command == "reset":
                game_running = self.__reset(argument)   # end the game in some way determined by the argument
                continue

            # if the command is "move", stop running the current room and run a new room
            elif command == "move":
                assert argument != "", "argument for \"move\" cannot be empty"  # error if argument is empty
                next_room = Room(argument)                                      # create a new room with argument being the room's name
                next_room.run()                                                 # run the new room
                game_running = False                                            # stop running the current room

            # if the command is "print", print out a string with the argument as its name
            elif command == "print":
                self.__print(argument)  # print out a string with the label matching the argument
                continue                # continue to the next command

            # if the command is "random", choose a random set of commands and run them
            elif command == "random":
                self.__run_results(self.__random(argument, option), option) # get a random list of commands and run them
                continue                                                    # continue to the next command

            # if the command is not a valid command raise an error
            else:
                raise AssertionError(command + " is not a valid command")   # raise an error due to an invalid command

        return game_running     # return whether the game would end


    

    def __check_requirements(self, requirements):
        '''
        Return whether or not a list of requirements are met.

        Parameters:
            requirements (list[str]): a list of requirements usually in the form of flags that must be checked
        '''

        # check each requirement
        for req in requirements:


            # ------------------------------
            # get data from the requirement
            # ------------------------------
        
            assert req != "", "empty strings in JSON req lists are not allowed"                                             # make sure req isn't empty
            assert req != "!", "\"\!\" is used for inverting requirements and is not allowed by itself in a JSON req list"  # make sure req isn't an exclamation mark

            # if there is a ":" in the requirement, its flag is under a different namespace
            if ":" in req:
                namespace, req = req.split(":", 2)                              # get the namespace (left of the ":") and the requirement (right of the ":")
                assert not(":" in req), "too many \":\" in requirement " + req  # make sure there are no more colons
                
            # if there isn't a ":", the namespace is the same as the Room name
            else:
                namespace = self.__name # set the namespace to be the room's name


            # -------------------------------
            # check if the requirement is met
            # -------------------------------
                
            # if requirement is empty, check if the namespace exits instead
            if req == "":

                # if the first character is "!", requirement is met if namespace doesn't exist
                if namespace[0] == "!":
                    namespace = namespace[1:]   # the namespace is everything but the first "!"

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
            return True # return True as all requirments were met

        return False    # return False as at least one requirment is not met


    def __set(self, namespace=None, argument=""):
        '''
        Set a flag to be stored for later use.

        Parameters:
            namespace (str): A string representing the namespace to set the flag in
            argument (str): A string representing the flag to set
        '''


        # --------------------------
        # set namespace if necessary
        # --------------------------

        namespace = self.__name if namespace == None else namespace     # namespace is room name if not specified
        
        # if the namespace for the new flag doesn't exist yet in the flag dict, create it
        if namespace not in Room.__flags.keys():
            Room.__flags[namespace] = []    # create the namespace in the form of an empty list with the namespace name as the dict key


        # ---------------------
        # set flag if necessary
        # ---------------------

        # if there is no argument, set the namespace rather than an individual flag
        if argument != "":
            assert argument != "!", "The \"set\" command argument cannot be \"!\""  # error if argument is "!"
            Room.__flags[namespace].append(argument)                                # add the argument to the flags list as a flag




    def __unset(self, namespace=None, argument=""):
        '''
        Unset a flag so that it no longer applies to requirements.

        Parameters:
            namespace (str): A string representing the namespace to unset or the namespace where the flag to be unset is
            argument (str): A string representing the flag to unset
        '''

        # --------------------------------------------
        # find the flag in the namespace and delete it
        # --------------------------------------------

        namespace = self.__name if namespace == None else namespace                 # namespace is room name if not specified
        assert argument != "!", "The \"unset\" command argument cannot be \"!\""    # error if argument is "!"
        
        # if the namespace exists in the flag dict, remove all occurences of the argument flag
        if namespace in Room.__flags.keys():

            # if no argument, delete the entire namespace
            if argument == "":
                del Room.__flags[namespace] # delete the namespace

            # if there is an argument, remove occurences of it from the namespace
            else:
                
                # while there are occurences of the argument flag, remove them
                while argument in Room.__flags[namespace]:
                    Room.__flags[namespace].remove(argument)    # remove an occurence of the argument flag

    def __reset(self, argument="game"):
        '''
        End the game in a way specified by the parameter.

        Parameters:
            argument (str): A string that specifies the way the program handles the reset
                "game" will reset the game back to the starting room
                "quit" will end the program
        '''


        # ------------
        # delete flags
        # ------------
        
        flags_to_delete = []        # list of flags to delete

        # check each namespace to remove flags from it
        for namespace in Room.__flags.keys():

            # check each flag in the namespace to see if it should be deleted
            for flag_i in range(len(Room.__flags[namespace])):

                # if the flag starts with "$", it stays between resets
                if Room.__flags[namespace][flag_i][0] != "$":
                    flags_to_delete.append((namespace, flag_i)) # set up the flag to be deleted if it doesnt have the "$"

        # delete non-permanent flags
        for namespace, flag in flags_to_delete:
            del Room.__flags[namespace][flag]   # delete the flag


        # -----------------
        # delete namespaces
        # -----------------
        
        namespaces_to_delete = []   # list of namespaces to delete

        for namespace in Room.__flags.keys():
            
            # if the namespace is empty, delete it
            if Room.__flags[namespace] == []:
                namespaces_to_delete.append(namespace)  # set up the namespace to be deleted

        # delete empty namespaces
        for namespace in namespaces_to_delete:
            del Room.__flags[namespace] # delete the namespace


        # -----------------------
        # reset in different ways
        # -----------------------

        # if the argument is "game", end/restart the game
        if argument == "game" or argument == "":


            # -------------------------------------
            # reset the game back to the first room
            # ask user to continue, reset game
            # -------------------------------------


            # ASK USER
            getting_input = True    # True while user hasn't yet inputted valid input

            # get input from the user regarding whether to replay or quit
            while getting_input:
                slow_type("Continue? (Y/N): ")                                                                              # get input from user
                user_input = input().upper()                                                                                # convert to uppercase
                getting_input = False if isinstance(user_input, str) and (user_input == "Y" or user_input == "N") else True # make sure input is "Y" or "N"
                game_running = False                                                                                        # end all running rooms but keeps program running
                json_text = dumps(Room.__flags)                                                                             # convert the flags to a json string
                data_handle = open("data.json", "w")                                                                        # open "data.json" for writing
                data_handle.write(json_text)                                                                                # write the flags' json string into data.json
                data_handle.close()                                                                                         # close data.json


            # RESET GAME
            # if the user inputted "Y", restart the game by ending all running rooms but keeping the program running
            if user_input == "Y":
                print() # print newline

            # if the user inputted "N", end the program
            else:
                sys.exit()  # end the program

            return False

        # if "quit" is the argument, end the program
        elif argument == "quit":
            sys.exit()  # end the program
            
        # if the argument is invalid raise an error
        else:
            raise AssertionError(argument + " is not a valid argument of reset")    # raise an error due to invalid argument




        def __print(self, argument):
            '''
            Print out the string with the specified label.

            Parameters:
                argument (str): A string which is the key for a string located in the option object in the JSON or in the constants list in the JSON
            '''


            # -----------------------
            # get the string to print
            # -----------------------
            
            assert argument != "", "the \"print\" command requires an argument" # error if there is no argument

            # check if the target text is in the curretn option
            if argument in option:
                text = option[argument] # store the found text

            # check if the target text is in the constants dictionary
            elif argument in self.__constants.keys():
                text = self.__constants[argument]   # store the found text

            # error if argument doesn't match any element in the option object or constants dict
            else:
                raise AssertionError("Cannot print " + argument + " as it does not exist")  # raise error
            
            assert isinstance(text, str), "The argument for \"print\" must be the label of a string, not a " + str(type(text))  # error if argument is not the label of a string


            # ----------------
            # print the string
            # ----------------
            
            slow_type(text + "\n\n")    # print out the target string to the user
            

        def __random(self, argument="", option=None):
            '''
            Choose a random list of commands to run.

            Parameters:
                argument (str):  A string containing the label of the random table object in the JSON
                option (dict[???]): An object that might contain the random table listed by the argument.
            '''


            # ---------------------
            # find the random table
            # ---------------------

            # if option is unset, set it to an empty dict
            option = {} if option == None else option
            
            assert argument != "", "the \"random\" command requires an argument"    # error if no argument for "random" command

            # check if table is in option object
            if argument in option:
                table = option[argument]    # get table from option object

            # check if table is in constants dictionary
            elif argument in self.__constants.keys():
                table = self.__constants[argument]  # get table from constants dictionary
                
            # error if no random table matching argument
            else:
                raise AssertionError("Cannot find random table: \"" + argument + "\"")  # raise error

            assert isinstance(table, list), argument + " must be the label of a list, not a " + str(type(table))    # error if random table is not a list
            bag = []                                                                                                # create list for storing each occurence of lists of commands to be chosen randomly


            # -------------------------------------------------------------------------------------------
            # construct a list of random groups where more likely to happen groups will appear more often
            # calculate weight, check requirements, construct list
            # -------------------------------------------------------------------------------------------

            # add each command list to the random bag taking into accout its weight
            for random_group in table:

                # CALCULATE WEIGHT
                # if weight is an attribute, use it to set the weight | weight is the relative likelihood of a list being chosen
                if "weight" in random_group:

                    
                    assert isinstance(random_group["weight"], int), "weight must be an integer, not a " + str(type(random_group["weight"])) # error if weight is not an integer
                    weight = random_group["weight"]                                                                                         # set weight from the JSON

                # if weight is not specified, set it to 1
                else:
                    weight = 1  # set the weight to 1

                # CHECK REQUIREMENTS
                # if there are requirements tied to this group, verify they are met
                if "req" in random_group:
                    assert isinstance(random_group["req"], list), "\"req\" must be the name of a list, not a " + str(type(random_group["req"])) # error if req is not a list
                    requirements_met = self.__check_requirements(random_group["req"])                                                           # check the requirements of the random group

                # if there are no requiremnts, then requirements are assumed to be met
                else:
                    requirements_met = True # requirements are met

                # if requirements are not met, do not use this random group
                if requirements_met == False:
                    weight = 0  # set weight to 0, effectivly preventing this group from being used

                # CONSTRUCT LIST
                assert "commands" in random_group, "Every object in a random table must have a \"commands\" list"                               # error if no commands list
                assert isinstance(random_group["commands"], list), "\"commands\" must be a list, not a " + str(type(random_group["commands"]))  # error if commands list is not a list

                # add 1 occurence of the command list for every weight point
                for i in range(weight):
                    bag.append(random_group["commands"])    # add an occurence of the command list to the random bag


            # -------------------------
            # get a random command list
            # -------------------------

            assert bag != [], "No choices were found in random table: " + argument  # error if the bag is empty
            chosen_command_list = choice(bag)                                       # get a random command list from the bag
            return chosen_command_list                                              # return the list of commands to be run
