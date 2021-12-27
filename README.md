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
&ensp&ensp;set can be used to set flags to be checked by the req list in the JSON structure.  
    
&ensp;unset  
&ensp;&ensp;The unset command will remove any instances of the argument string that are being stored as a flag to be checked later  
    
