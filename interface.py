if __name__ != "__main__":
    import pygame, sys
    from editor import Editor
    from room import Room

    class Interface:

        def __init__(self):
            pygame.init()

            self.start = "start_room_fight"

            self.__size = self.__width, self.__height = 640, 480

            self.__screen = pygame.display.set_mode(self.__size)

            self.__editor = Editor(self.__screen)

            Room.set_editor(self.__editor)

            self.__current_room = Room(self.start)

            self.__reset_game = False
            self.__reset_room = False

        def run(self):

            self.__screen.fill((0, 0, 0))
            self.__editor.type()
            #self.__current_room.run()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif self.__editor.get_buffer() != []:
                        continue
                    elif self.__reset_game or self.__reset_room:
                        if self.__editor.get_buffer() == [] and chr(event.key).upper() in ["Y", "N"] and (self.__reset_game or self.__reset_room):
                            if chr(event.key).upper() == "Y" and self.__reset_game:
                                self.__editor.clear()
                                self.__reset_game = False
                                self.__current_room = Room(self.start)
                            elif chr(event.key).upper() == "Y" and self.__reset_room:
                                self.__editor.clear()
                                self.__reset_room = False
                                self.__current_room = Room(self.__current_room.get_name())
                            else:
                                pygame.quit()
                                sys.exit()
                    elif event.key < 123 and event.key > 64 and chr(event.key).upper() in [chr(i) for i in range(65, 65 + len(self.__current_room.shown_options))]:
                        self.__current_room.choose_option(event.key)
                            
                        
                elif event.type == pygame.MOUSEWHEEL:
                    self.__editor.scroll += event.y
                elif event.type == Room.PALAI_EXIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == Room.GAME_RESET:
                    self.__editor.type("GAME OVER\nRESTART? (Y/N)")
                    self.__reset_game = True
                    Editor.delay = 65
                    
                elif event.type == Room.ROOM_RESET:
                    self.__editor.type("GAME OVER\nCONTINUE? (Y/N)")
                    self.__reset_room = True
                    Editor.delay = 65

                elif event.type == Room.ROOM_CHANGE:
                    #self.__editor.clear()
                    self.__current_room = Room(Room.next_room)
                    Room.next_room = ""
                    
            pygame.display.flip()

        def type(self, text):
            new_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(new_text, (0, 0))
