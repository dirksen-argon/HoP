import json
from time import sleep
from random import choice, sample

import sys
import os
sys.path.insert(1, "/Users/fischerrecordingstudio/Documents/Test HoP/Test Folder")

from functions import slow_type, pick_box, pick_door
from room import Room

 # "backpack" is the player's inventory.
backpack = []

running = True
while running:
    start_room = Room("start_room")

    start_room.run()
