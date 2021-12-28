# HoP
verbal horror turned coding nightmare

EXAMPLE JSON FILE: example.json-----------------------------------------------------------<br />
{
&ensp;"room_text": "This is where you put the text that is displayed when the player enters this room",<br />
&ensp;"options": [<br />
&ensp;&ensp;{<br />
&ensp;&ensp;&ensp;"option_text": "This is where you put the discription of this choice",<br />
&ensp;&ensp;}<br />
&ensp;]<br />
}<br />  

JSON STRUCTURE----------------------------------------------------------------------------  
|-room_text  
|-options  
&ensp;|-req  
&ensp;| |  
&ensp;|  
&ensp;|-option_text  
&ensp;|-result_text  
&ensp;|-result  
&ensp;&ensp;|  

room_text  
&ensp;room_text contains the text displayed when the user enters the room  

options  
&ensp;options is a list of every option object connected to this room.  

req (OPTIONAL)  
&ensp;req is a list of strings where each string is a flag that must be set for the option to be displayed.  
&ensp;If a flag starts with "!", then that flag must not be set for the option to be displayed.  
&ensp;If a flag is in a different namespace, write the namespace before the flag name and separate with a colon. Example: "namespace:flag_name"  

option_text  
&ensp;contains the text describing its corresponding option  
  
result_text (OPTIONAL)  
&ensp;result_text is a string containing the text displayed when the player chooses the corresponding option  
  
result (OPTIONAL)  
&ensp;result is a list of commands that will be run when the option is chosen.  
&ensp;Commands are strings containing a command and an argument separated by a "-". Example: "command-argument"  
  
&ensp;Arguments can have a namespace (the name of a room usually). The namespace and the argument are separated by a ":". Example: "command-namespace:argument"  
&ensp;If the namespace is not included, it will be set to the name of the current room  
  
&ensp;COMMANDS  
&ensp;set  
&ensp;&ensp;The set command will store the argument as a string to be checked later.  
&ensp;&ensp;set can be used to set flags to be checked by the req list in the JSON structure.  
    
&ensp;unset  
&ensp;&ensp;The unset command will remove any instances of the argument string that are being stored as a flag to be checked later  

&ensp;reset  
&ensp;&ensp;The reset command will reset the game back to the beggining if it has the argument "game" (argument is "game" by default) or end the game if the user doesn't wish to continue

&ensp;quit  
&ensp;&ensp;The quit command will end the program

&ensp;move  
&ensp;&ensp;The move command takes the name of a room as an argument. Example: "move-room_name"
&ensp;&ensp;The move command will cause the current room to stop running and start running the new room.
    
&ensp;print  
&ensp;&ensp;The print command will print out a string (stored in the option object with the label the same as the argument).

&ensp;random  
&ensp;&ensp;The random command will run a randomly selected set of commands. Its argument is the name of a list containing the random choices.
&ensp;&ensp;The list contains objects. Each object has a "weight" integer(OPTIONAL) and a "commands" list.
&ensp;&ensp; The weight integer is the weight of the corresponding commands list being randomly selected.
&ensp;&ensp; The "commands" list is a list of strings containing commands, exactly like the "result" list.
