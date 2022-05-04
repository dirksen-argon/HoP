if __name__ != "__main__":
    import pygame
    import time
    
    class Editor:

        command_list = ["w", "d", "m", "@"]

        def __init__(self, box):
            pygame.init()

            self.__box = box

            self.__text = ""
            self.__text_buffer = []

            self.__font = pygame.font.Font(pygame.font.match_font("georgia"), 16)

            self.__max_width = 0
            self.__dy = 0

            self.__w_start_time = None
            self.__w_timer_i = 0

            self.__d_timer = time.time()
            self.__d_index = 0

            self.__delay = 65

            self.__mode = 0

            self.scroll = 0

            self.__wait_time = time.time()  # time when wait command is over and typing can resume

            for i in range(32, 127):
                surface = self.__font.render(ascii(i), False, (255, 255, 255))
                if surface.get_rect().width > self.__max_width:
                    self.__max_width = surface.get_rect().width
                if surface.get_rect().height > self.__dy:
                    self.__dy = surface.get_rect().height

        def type(self, new_text=None, *args):

            # if new text is given
            if new_text != None:
                # ensure text is a string
                assert isinstance(new_text, str), "text displayed to the screen must be a string, not " + str(type(new_text))

                new_text = self.word_wrap(new_text) # add newlines into the text for word wrapping
                
                # if we have text onscreen or in buffer put space between old text and the new text
                if (self.__text != "" or self.__text_buffer != []) and "no newline" not in args:
                    new_text = "\n\n" + new_text    # put newlines before new text


                # put new text in buffer
                for char in new_text:
                    self.__text_buffer.append(char) # put char from new_text in buffer

            # if we are in slow_type mode and the buffer isn't empty add in characters with a delay
            if self.__mode == 0 and len(self.__text_buffer) != 0:
                # if delay timer over and not waiting, display character
                if time.time() - self.__d_timer >= self.__delay / 1000 and time.time() - self.__wait_time >= 0:
                    next_char = self.__text_buffer.pop(0)   # get next character to be displayed

                    # if character is command, run command
                    if next_char == "@":
                        self.run_command()  # run a command
                        self.display()      # display text on screen
                        
                    # display next character
                    else:
                        self.display(next_char)         # display text on screen with a new character
                        self.__d_timer = time.time()    # reset type delay timer

                # if not time to display new character, display old text on screen
                else:
                    self.display()  # display text on screen

            # if we are not in slow type mode and buffer isn't empty add in characters with no delay
            elif self.__mode == 1 and self.__text_buffer != "":

                # if we aren't waiting print characters
                if time.time() - self.__wait_time >= 0:
                    new_text = ""   # stores text to be printed at once

                    # while values still in buffer, pop them and display them
                    while True:

                        try:
                            char = self.__text_buffer.pop(0)    # get next character

                        # if can't pop because buffer empty, stop iterating
                        except AttributeError:
                            break   # stop iterating

                        # if we run into a command, run it
                        if char == "@":
                            self.run_command()  # run command
                            break               # print what we have so far, save rest for next frame

                        # if we aren't in a command, store the character
                        else:
                            new_text += char    # store the character

                    # print out the stored text all at once
                    self.display(new_text)

                # print old text if waiting
                else:
                    self.display()  # print text on screen

            # if nothing to print, print old text on screen
            else:
                self.display()  # print text on screen
                

        def display(self, new_text=None):
            self.__d_timer = time.time() if self.__d_timer == None else self.__d_timer
            new_text = "" if new_text == None else new_text
            self.__text += new_text
            

            x = 10
            y = 2 + self.scroll * 10

            if y > 2:
                y = 2
                self.scroll = 0
            elif self.__box.get_rect().height > (self.__text.count("\n") + 1) * self.__dy:
                self.scroll = 0
                y = 2
            elif y < 2 + -(self.__text.count("\n") + 4) * self.__dy + self.__box.get_rect().height:
                y = self.__box.get_rect().height - 2 - (self.__text.count("\n") + 4) * self.__dy
                self.scroll = (y - 2)/10

            i = 0
            while i < len(self.__text):
                if self.__text[i] == "\n":
                    y += self.__dy
                    x = 10
                    self.__d_index += 1

                else:

                    text_surface = self.__font.render(self.__text[i], True, (255, 255, 255))
                    self.__box.blit(text_surface, (x, y))
                    x += text_surface.get_rect().width

                i += 1   


        def run_command(self):
            arg = ""    # used to store argument of command

            reading_command = True  # true when reading command from text buffer

            # loop through characters in command to get argument and run command
            while reading_command:
                char = self.__text_buffer.pop(0)    # get the next character

                # if w, wait for specified amoutn of time
                if char == "w":
                    assert arg != "" and arg.isnumeric(), "Usage: @XXXXw where X is integer and there are at least 1 X" # error if invalid argument
                    arg = int(arg)                                          # get integer
                    self.__wait_time = time.time() + arg / 1000             # get time to continue displaying
                    reading_command = False                                 # stop reading the command

                # if d, change delay time
                elif char == "d":
                    assert arg != "" and arg.isnumeric(), "Usage: @XXXXd where X is integer and there are at least 1 X" # error if invalid argument 
                    arg = int(arg)          # get command argument as int
                    self.__delay = arg      # set delay
                    reading_command = False # stop reading the command

                # if m, change slow type mode
                elif char == "m":

                    # if argument is 0 enable slow type
                    if arg == "0":
                        self.__mode = 0     # enable slow type

                    # if argument is 1 disable slow type
                    elif arg == "1":
                        self.__mode = 1     # disable slow type

                    # invalid argument, raise error
                    else:
                        print(arg)
                        raise AssertionError("Usage: @Xm where X is 0 for enable slow type or 1 for disable slow type") # error if invalid argument

                    reading_command = False # stop reading the command

                # if @, print @
                elif char == "@":
                    assert arg == "", "Usage: @@"   # error if argument exists
                    self.display("@")               # display @

                    # set delay timer if slow typing
                    if self.__mode == 0:
                        self.__d_timer = time.time()    # set delay timer

                    reading_command = False # stop reading the command
                
                # store argument for command
                else:
                    arg += char     # append character to command argument


        def word_wrap(self, text):

            x = 0                               # measures distance between current character and left side of screen
            i = 0                               # index for getting characters from text
            currently_parsing_command = False   # flag for if we are currently iterating through an in-text command

            # loop through every character in input and find where to put newlines
            while i + 1 < len(text):

                # add to x if current characer is counted as having width (not a command)

                # id we are in a command and the current character is the last char in the command, we are no longer in a command
                if currently_parsing_command and text[i] in Editor.command_list:

                    # if it is @ command, @ is printed so count its width
                    if text[i] == "@":
                        x += self.__font.render("@", False, (255, 255, 255)).get_rect().width   # add width to x
                    currently_parsing_command = False   # no longer in a command

                # if we are in a command, do not check if x should increase
                elif currently_parsing_command:
                    pass    # stop checking

                # if the current character is "@", we are now in a command
                elif text[i] == "@":
                    currently_parsing_command = True    # we are now in a command

                # if the current character has width in the final display, store its width
                else:
                    # store the width of the current character
                    x += self.__font.render(text[i], False, (255, 255, 255)).get_rect().width

                # if the current character is a space, we are between words and will check if we should go to a new line
                if text[i] == " ":
                    next_space = text[i + 1:].find(" ")         # get the location of the next space
                    next_word = text[i + 1:next_space + i + 1]  # the next word will be between the current char (which is space) and the next space

                    word_width = 0          # counts width of the word
                    command_running = False # flag for if we iterate through command while getting width

                    # get the width of the word by adding together the width of its characters
                    for char in next_word:

                        # if @@ command is running, ignore it since it puts down @
                        if command_running and char == "@":
                            command_running = False # stop running command

                        # if we are iterating through a command, ignore the width for now
                        if command_running:

                            # if we have reached the end of the command, stop ignoring width
                            if char in Editor.command_list:
                                command_running = False # we are no longer in a command
                                continue                # get next char to measure width

                        # if we have "@" we are now in a command
                        elif char == "@":
                            command_running = True  # we are now in a command

                        # add width of character to total
                        else:
                            # add width of character to total
                            word_width += self.__font.render(char, False, (255, 255, 255)).get_rect().width

                    # if we are near the right edge of screen add a newline
                    if x + word_width + self.__max_width > self.__box.get_rect().right and text[i + 1] != "\n":
                        text = text[:i + 1] + "\n" + text[i + 1:]   # add a newline

                # if we hit a newline, reset x since we are now at left of screen
                elif text[i] == "\n":
                    x = 0   # reset x

                i += 1  # increment iterator

            return text     # return text with newlines inserted

        def clear(self):
            self.__text = ""
            self.__buffer = []

        def get_buffer(self):
            return self.__text_buffer
