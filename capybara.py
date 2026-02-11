import os
import time
import re
import math


# Running the program and ref
# MAC:
# python3 referee.py capybara fake_capybara --time_limit 20 & python3 capybara.py & python3 fake_capybara.py

# Windows (open 3 terminals):
# python capybara.py
# python fake_capybara.py
# python referee.py capybara fake_capybara --time_limit 20


#TODO: Charlie: Capy will read the file when the opponent moves twice, but will send out a message or a signal that capy will not be taking his turn and passes to the Ref.
#TODO: Charlie: Capy will read every move the opponent does.
#TODO: Squares are captured by the color-team who completes the square.
#TODO: capybara needs to build his own board as he visualizes as a tree
#These are global variables which function like capy's memory.
capy_remembers_occupied_coordinates = [] #all just an array of single tuples which are occupied regardless of side
capy_remembers_friendly_edges = [] #for friendly, all edges which friendly has drawn, tuples of coordinates)
capy_remembers_enemy_edges = [] #for opponent, all edges which opponent has drawn
latest_friendly_move = () #for friend, this is what the algorithm will write to after it has made its own move
latest_enemy_move = () #for enemy, this is what the algorithm will have after it has parsed an enemy move.
latest_general_move = () #TODO: a function that might utilize this decides which side had the latest move and who had it
has_enemy_gone_multiple_times_in_a_row = False #TODO: this is for the case that capy knows the enemy has gone more than once in a row
capy_remembers_friendly_square_count = 0 #81 possible squares can exist from the scenario of 180 edges on the 10x10 dot board,
capy_remembers_enemy_square_count = 0 #if 41 squares are captured by the enemy during a match, there is no way for capy to win.


#TODO: a main portion of the program which is always run when it is our turn in order.
#TODO: This main portion should first read, upkeep (including the various checks he performs), if we should not move, pass, if we should move: minimax/heuristic, write (and sub-upkeep)

# Checks if a file exists in the current repository
def check_file(filename):
    current_directory = os.getcwd()  # Get the current working directory
    file_path = os.path.join(current_directory, filename)  # Construct the file path

    return os.path.exists(file_path) and os.path.isfile(file_path)


# Waits for a respective go file to appear in the directory
def wait_for_file(filename):
    directory = os.getcwd()
    while not os.path.exists(os.path.join(directory, filename)):
        time.sleep(1)  # Wait for 1 second before checking again
        print("waiting on capybara go")


#capybara checks to see if he actually would already win
def capy_checks_to_claim_victory():
    if capy_remembers_friendly_square_count >= 41:
        print("capybara knows he has already won")
        return True
    else:
        return False

#capybara_checking_to_currender, returns true if he cannot win
def capy_checks_to_surrender():
    if capy_remembers_enemy_square_count >= 41:
        print("capybara knows he cannot win\n")
        return True
    else:
        return False

# store_last_coordinate, we must take the new string of the opponent_move and parse the string and store the tuples.
# an opponent move will look like: "enemy 3,4 3,5"
#TODO: Provide the case for when capy goes again.
#all domains are 0-9, and all ranges are 0-9
def parse_last_enemy_move():
    enemyreadline = file.read()
    splitstring = enemyreadline.split(" ") #separates it out into an array with three places the name of the player, the first coord, and the second coord. a delimiter here is a space

    #getting coordinates
    stringed_raw_firstcoord = splitstring[1]
    stringed_firstcoord = stringed_raw_firstcoord.replace(",", "")
    stringed_raw_secondcoord = splitstring[2]
    stringed_secondcoord = stringed_raw_secondcoord.replace(",", "")

    integered_firstcoord_x = int(stringed_firstcoord[0])
    integered_firstcoord_y = int(stringed_firstcoord[1])
    integered_secondcoord_x = int(stringed_secondcoord[0])
    integered_secondcoord_y = int(stringed_secondcoord[1])

    #The actual coordinates are here changed the stringed coordinats into tuples, tuples do not have the numbers as integers
    tupled_firstcoord = (integered_firstcoord_x, integered_firstcoord_y)
    tupled_secondcoord = (integered_secondcoord_x, integered_secondcoord_y)
    tupled_edge = (tupled_firstcoord, tupled_secondcoord)

    # TODO: in this function, it should be decided whether or not a pass file is present, if a pass file is present, that player cannot play on their reading turn.
    #TODO: start capy upkeep, this needs to account for the case if capy goes again. It checks if there is it's respective pass file present.
    # Reminder that capy reads every move that is played
    if check_file("capybara.pass"):
        capy_enemy_upkeep(tupled_firstcoord, tupled_secondcoord, tupled_edge, splitstring[0])
    else:
        capy_enemy_upkeep(tupled_firstcoord, tupled_secondcoord, tupled_edge, splitstring[0])
        capy_friendly_upkeep(tupled_firstcoord, tupled_secondcoord, tupled_edge, splitstring[0])


#upkeep function for what capy remembers, before he makes his own moves, if the enemy
def capy_enemy_upkeep(arg_tupled_firstcoord, arg_tupled_secondcord, arg_tupled_edge, playername):
    if(playername != "capybara"):
        latest_enemy_move = arg_tupled_edge
        capy_remembers_occupied_coordinates.append(arg_tupled_firstcoord)
        capy_remembers_occupied_coordinates.append(arg_tupled_secondcord)
        capy_remembers_enemy_edges.append(arg_tupled_edge)

def capy_friendly_upkeep(arg_tupled_firstcoord, arg_tupled_secondcoord, arg_tupled_edge, playername):
    if (playername == "capybara"):
        print("Capy's move")
    #TODO: initiate capy actually moving again on his turn.

#Charlie needs to implement the writer funciton whuch takes it's input form the algorithm, and writes it out to the move_file.txt
#input parameters are two tuples, which need to be written to string
# an friendly move will look like: "capybara 3,4 3,5"
#TODO: After everytime the algorithm was used run this function
def write_next_move(coord1, coord2):
    #upkeep capy's current move, this upkeep is implicit in here
    tupled_capys_latest_edge = (coord1, coord2)
    latest_friendly_move = tupled_capys_latest_edge
    capy_remembers_occupied_coordinates.append(coord1)
    capy_remembers_occupied_coordinates.append(coord2)
    capy_remembers_friendly_edges.append(latest_friendly_move)

    #the writing process itself
    strcoord1 = str(','.join(str(x) for x in coord1))
    strcoord2 = str(','.join(str(x) for x in coord2))

    file.write("capybara " + strcoord1 + " " + strcoord2)



#TODO: Aidan/Eli needs study the algorithm that inputs tuples of tuples and outputs them as well to the writer.
#TODO: We need to design a heuristic to decide which next move is the best move. We could use minimax in combination with Monte Carlo Tree Search,
#TODO: we would also need it to use Progressive Deepening as long as real world time allows
#TODO: because of the insanity of having a large search space, exploring every option is not feasible.
#TODO: Minimax with AlphaBeta pruning with helping heuristics (Iterative Deepening with explicit recording of real world time)


def capy_algorithm(state):
    pass


# TODO: main function should be written at the very end of the script.

# Program waits for the go file
print("Capybara initiated")
wait_for_file("capybara.go")
print('Capybara found the go file!')

# Program starts after the go file has been detected
if check_file("end_game"):
    pass
else:
    with open('move_file', 'r') as file:
        # ignored opponent move
        opponent_move = file.read()

    with open('move_file', 'w') as file:
        # overwrite with my own move
        file.write("capybara 2,3 2,4")