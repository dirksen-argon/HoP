# HoP
verbal horror turned coding nightmare

EXAMPLE JSON FILE: example.json-----------------------------------------------------------
{
  "room_text": "This is where you put the text that is displayed when the player enters this room",
  "options": [
    {
      "option_text": "This is where you put the discription of this choice",
    }
  ]
}

JSON STRUCTURE----------------------------------------------------------------------------
|-room_text
|-options
  |-req
  | |
  |
  |-option_text
  |-result_text
  |-result
    |

room_text
  room_text contains the text displayed when the user enters the room

options
  options is a list of every option object connected to this room.

req (OPTIONAL)
  req is a list of strings where each string is a flag that must be set for the option to be displayed.
  If a flag starts with "!", then that flag must not be set for the option to be displayed.
  If a flag is in a different namespace, write the namespace before the flag name and separate with a colon. Example: "namespace:flag_name"

option_text
  contains the text describing its corresponding option
  
result_text (OPTIONAL)
  result_text is a string containing the text displayed when the player chooses the corresponding option
  
result (OPTIONAL)
  result is a list of commands that will be run when the option is chosen.
  Commands are strings containing a command and an argument separated by a "-". Example: "command-argument"
  
  Arguments can have a namespace (the name of a room usually). The namespace and the argument are separated by a ":". Example: "command-namespace:argument"
  If the namespace is not included, it will be set to the name of the current room
  
  COMMANDS
  set
    The set command will store the argument as a string to be checked later.
    set can be used to set flags to be checked by the req list in the JSON structure.
    
  unset
    The unset command will remove any instances of the argument string that are being stored as a flag to be checked later
    
