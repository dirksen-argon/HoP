

if __name__ != "__main__":

    from editor import Editor
    from json import loads, dumps       # for converting json to dict and vice versa
    from os.path import dirname, exists # for finding files
    from random import choice           # for running the random command
    import pygame
    from pygame.locals import *

    class Room:

        __editor = None
        __flags = {}

        PALAI_EXIT = USEREVENT + 1
        quit_event = pygame.event.Event(PALAI_EXIT)

        GAME_RESET = USEREVENT + 2
        game_reset_event = pygame.event.Event(GAME_RESET)

        ROOM_RESET = USEREVENT + 3
        room_reset_event = pygame.event.Event(ROOM_RESET)

        ROOM_CHANGE = USEREVENT + 4
        room_change_event = pygame.event.Event(ROOM_CHANGE)

        next_room = ""

        def __init__(self, name):

            assert Room.__editor != None, "the editor must be set with Room.set_editor() before a Room can be created"

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

            # -------------------------------------------------------------
            # asign values from json where needed
            # name, text, flags, options, constants, changes, text settings
            # -------------------------------------------------------------

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

            # CHANGES
            self.__changes = []  # initialize list for storing changes made during room

            # TEXT SETTINGS
            self.__text_settings = room_dict["text_settings"] if "text_settings" in room_dict else ""   # get text settings if they are set in the JSON

            self.__result = ""

            self.__resetting = False
            
            
            # --------------------
            # run startup commands
            # --------------------

            # if there are commands to run on startup, run them
            if "commands" in room_dict.keys():
                assert isinstance(room_dict["commands"], list), "\"commands\" must be a list"                   # error if "commands" is not a list
                command_result = self.__run_commands(room_dict["commands"][:])                                   # run the startup commands

##            # ---------------------
##            # display the room text
##            # ---------------------
##
##            self.option_count = 0
##
            # print out the room's introduction text
            if self.__text:
                Room.__editor.type(self.__text + "\n\n")

            self.shown_options = self.__display_options()

##
##        
##            shown_options = self.__display_options()
            
        
        # choose option text
        # room text
        # options

        # flags

        def __display_options(self):
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
                
                Room.__editor.type(self.__text_settings + chr(letter_ascii) + ": " + option["option_text"] + "\n", "no newline")   # print the corresponding letter of the option to its left
                letter_ascii += 1                                               # increment the letter by 1 up the alphabet
                #self.option_count += 1

            # RETURN OPTIONS
            return shown_options    # return the list of options shown to the user
        

        def __check_requirements(self, requirements):
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


        def choose_option(self, key):
            key = ord(chr(key).upper())

            option = self.shown_options[key - ord('A')]
            
            result = ""

            if self.__result != "":
                result = self.result
                self.__result = ""
                
            elif "result_text" in option:
                result = option["result_text"]

            Room.__editor.clear()

            try:            
                self.__run_commands(option["result"][:])
                
            except KeyError:
                pass

            if (Room.next_room != ""):
                Room.__editor.clear()
                Room.__editor.type(result, "no newline")
                return
            
            Room.__editor.type(result + "\n\n")

            if self.__resetting == False:
                self.shown_options = self.__display_options()

            self.__resetting = False


        def __run_commands(self, commands, option={}, mode=""):
            
            # ----------------
            # run each command
            # ----------------
            
            game_running = True # keep track of whether a result would end the game
                
            # iterate through each command in the list
            for result in commands:


                # ------------------------------
                # get the namespace and argument
                # ------------------------------
                
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


                # --------------------------------
                # determine the command and run it
                # --------------------------------
                
                # if the command is "set", add the argument to the flags list as a flag to keep track of it
                if command == "set":
                    self.__set(namespace, argument, mode=mode)  # set the flag/namespace
                    continue                                    # continue to the next command
                
                # if the command is "unset", remove a flag from the flags list if it exists
                elif command == "unset":
                    self.__unset(namespace, argument, mode=mode)    # unset the flag/namespace
                    continue                                        # continue to the next command
                
                # if the command is "reset", end the game
                elif command == "reset":
                    game_running = self.__reset(argument)   # end the game in some way determined by the argument
                    continue

                # if the command is "move", stop running the current room and run a new room
                elif command == "move":
                    assert argument != "", "argument for \"move\" cannot be empty"  # error if argument is empty
                    pygame.event.post(Room.room_change_event)
                    Room.next_room = argument
                    #next_room = Room(argument)                                      # create a new room with argument being the room's name
                    #next_room.run()                                                 # run the new room
                    #game_running = False                                            # stop running the current room

                # if the command is "print", print out a string with the argument as its name
                elif command == "print":
                    self.__print(argument, option)  # print out a string with the label matching the argument
                    continue                # continue to the next command

                # if the command is "random", choose a random set of commands and run them
                elif command == "random":
                    self.__run_commands(self.__random(argument, option), option) # get a random list of commands and run them
                    continue                                                    # continue to the next command

                # if the command is "if", run a list of commands if requirements are met
                elif command == "if":
                    self.__if(argument, option) # run commands if requirements are met
                    continue                    # continue to the next command

                # if the command is "delay", change the type speed globally for text
##                    elif command == "delay":
##                        self.__delay(argument)  # change the global delay for slow typing
##                        continue                # continue to the next command

                # if the command is not a valid command raise an error
                else:
                    raise AssertionError(command + " is not a valid command")   # raise an error due to an invalid command

            if game_running == False:
                
                pygame.event.post(Room.quit_event)

        def __set(self, namespace=None, argument="", mode=""):
            '''
            Set a flag to be stored for later use.

            Parameters:
                namespace (str): A string representing the namespace to set the flag in
                argument (str): A string representing the flag to set
                mode (str): used to convey specific instructions to the method
                    "reset" will prevent the method from recording its changes
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

                # if there is not a reset happening, record the change for later
                if mode != "reset" and argument[0] != "$":
                    self.__changes.append("unset-" + namespace + ":" + argument)    # record the change so it can be undone on a reset




        def __unset(self, namespace=None, argument="", mode=""):
            '''
            Unset a flag so that it no longer applies to requirements.

            Parameters:
                namespace (str): A string representing the namespace to unset or the namespace where the flag to be unset is
                argument (str): A string representing the flag to unset
                mode (str): used to convey specific instructions to the method
                    "reset" will prevent the method from recording its changes
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

                        # if there is not a reset happening, record the change for later
                        if mode != "reset":
                            self.__changes.append("set-" + namespace + ":" + argument)    # record the change so it can be undone on a reset




        def __reset(self, argument="game"):
            '''
            End the game in a way specified by the parameter.

            Parameters:
                argument (str): A string that specifies the way the program handles the reset
                    "game" will reset the game back to the starting room
                    "quit" will end the program
                    "reset" will reset the current room
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

                pygame.event.post(Room.game_reset_event)
                self.__resetting = True

                json_text = dumps(Room.__flags)                                                                             # convert the flags to a json string
                data_handle = open("data.json", "w")                                                                        # open "data.json" for writing
                data_handle.write(json_text)                                                                                # write the flags' json string into data.json
                data_handle.close()                                                                                         # close data.json


##                # RESET GAME
##                # if the user inputted "Y", restart the game by ending all running rooms but keeping the program running
##                if user_input == "Y":
##                    print() # print newline
##
##                # if the user inputted "N", end the program
##                else:
##                    sys.exit()  # end the program
##
##                return False

            # if "quit" is the argument, end the program
            elif argument == "quit":
                self.__resetting = True
                json_text = dumps(Room.__flags)                                                                             # convert the flags to a json string
                data_handle = open("data.json", "w")                                                                        # open "data.json" for writing
                data_handle.write(json_text)                                                                                # write the flags' json string into data.json
                data_handle.close()                                                                                         # close data.json
                pygame.quit()
                sys.exit()  # end the program

            # if "room" is the argument, restart the room
            elif argument == "room":
                self.__resetting = True
                self.__changes.reverse()                            # reverse the list of changes so we can undo them in the correct order
                self.__run_commands(self.__changes, mode="reset")    # undo every change made
                self.__changes = []                                 # reset changes list
                
                # get input from the user regarding whether to replay or quit

                json_text = dumps(Room.__flags)                                                                             # convert the flags to a json string
                data_handle = open("data.json", "w")                                                                        # open "data.json" for writing
                data_handle.write(json_text)                                                                                # write the flags' json string into data.json
                data_handle.close()


                pygame.event.post(Room.room_reset_event)
                
            # if the argument is invalid raise an error
            else:
                raise AssertionError(argument + " is not a valid argument of reset")    # raise an error due to invalid argument




        def __print(self, argument, option=None):
            '''
            Print out the string with the specified label.

            Parameters:
                argument (str): A string which is the key for a string located in the option object in the JSON or in the constants list in the JSON
            '''

            option = {} if option == None else option
            

            # -----------------------
            # get the string to print
            # -----------------------
            
            assert argument != "", "the \"print\" command requires an argument" # error if there is no argument

            # check if the target text is in the curretn option
            if argument in option:
                text = option[argument] # store the found text

            # check if the target text is in the constants dictionary
            elif argument in self.__constants.keys():
                text = self.__constants[argument]   # store the found text0


            # error if argument doesn't match any element in the option object or constants dict
            else:
                raise AssertionError("Cannot print " + argument + " as it does not exist")  # raise error
            
            assert isinstance(text, str), "The argument for \"print\" must be the label of a string, not a " + str(type(text))  # error if argument is not the label of a string


            # ----------------
            # print the string
            # ----------------
            
            Room.__editor.type(text, "no newline")    # print out the target string to the user
            



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




        def __if(self, argument, option=None):
            '''
            Run a list of commands if specific requirements are met.

            Parameters:
                argument (str): label for JSON object containing requirements and commands
                option (str): an option which might have the JSON object referenced by the argument
            '''
            

            # ---------------------------------
            # get the requirements and commands
            # ---------------------------------

            option = {} if option == None else option                                                       # if option not set, keep it as an empty dict
            assert isinstance(option, dict), "the option used in the \"if\" command must be a dictionary"   # error if option isn't a dictionary
            assert isinstance(argument, str), "the argument for the \"if\" command must be a string"        # error if argument isn't a string

            # if the requirements and commands are in the option, get them
            if argument in option:
                if_commands = option[argument]  # store the JSON object with the requirements and commands

            # if the requirements and commands are in constants, get them
            elif argument in self.__constants:
                if_commands = self.__constants[argument]    # store the JSON object with the requirements and commands

            # error if cannot find JSON with requirements and commands
            else:
                raise AssertionError("could not find \"" + argument + "\"") # no requirements or commands so error

            assert isinstance(if_commands, dict), "\"" + argument + "\" must be a dictionary"                                   # error if not a dictionary
            assert "req" in if_commands, "\"req\" list not found in \"" + argument + "\""                                       # error if no requirements
            assert isinstance(if_commands["req"], list), "\"req\" in \"" + argument + "\" must be a list"                       # error if requirements not a list
            assert "commands" in if_commands, "\"" + argument + "\" must have a \"commands\" list"                              # error if no commands
            assert isinstance(if_commands["commands"], list), "the \"commands\" list in \"" + argument + "\" must be a list"    # error if commands not a lsit
            commands = if_commands["commands"]                                                                                  # get commands list


            # -----------------------------------
            # check requirements and run commands
            # -----------------------------------

            # if requirements are met, run the commands
            if self.__check_requirements(if_commands["req"]):
                self.__run_commands(commands, option)    # run the commands
                return True                             # return True as requirements were met

            return False    # return False as requirements weren't met




        def __delay(self, argument):
            '''

            '''
            
            assert isinstance(argument, str), "the argument for the \"delay\" command must be a string, not a " + str(type(argument))

            assert len(argument) > 0, "the argument cannot be empty for the \"delay\" command"

            if argument[0] == "~":
                positive = False
                assert len(argument) > 1, "the argument must be a number for the \"delay\" command"
                argument = argument[1:]
            else:
                positive = True

            assert argument.isnumeric(), "the argument for \"delay\" must be an integer"
            
            delay_modifier = int(argument)

            delay_modifier = delay_modifier if positive else delay_modifier * -1

            self.__delay_modifier = delay_modifier


        @classmethod
        def set_editor(self, editor):
            Room.__editor = editor
            

        def get_name(self):
            return self.__name
