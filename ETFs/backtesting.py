# import libraries
import plot

import os

# Parent directory path
PARENT_DIR = os.getcwd()

# new folder
new_folder = "date"

# Existing Directory
directory = f"Pictures/{new_folder}"

print(PARENT_DIR)

# Path
path = os.path.join(PARENT_DIR, directory)

try:
    os.mkdir(path)
    print(path)
except OSError as error:
    print(error)



