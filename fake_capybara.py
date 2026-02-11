import os
import time


# Checks if a file exists in the current repository
def check_file(filename):
    current_directory = os.getcwd()  # Get the current working directory
    file_path = os.path.join(current_directory, filename)  # Construct the file path

    return os.path.exists(file_path) and os.path.isfile(file_path)



def wait_for_file(filename):
    directory = os.getcwd()
    while not os.path.exists(os.path.join(directory, filename)):
        time.sleep(1)  # Wait for 1 second before checking again
        print("waiting on fake")

print("Fake initiated")
# Program waits for the go file
wait_for_file("fake_capybara.go")
print('Fake found the go file!')

# Program starts after the go file has been detected

if check_file("end_game"):
    pass
else:
    with open('move_file', 'r') as file:
        # ignored opponent move
        opponent_move = file.read()

    with open('move_file', 'w') as file:
        # overwrite with my own move
        file.write("fake_capybara 3,3 3,4")

# python3 referee.py capybara fake_capybara --time_limit 20 & python3 capybara.py & python3 fake_capybara.py
