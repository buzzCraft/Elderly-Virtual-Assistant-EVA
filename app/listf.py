import os

# Specify the directory path
directory_path = "../docker"

# List all files in the directory
files = os.listdir(directory_path)

# Filter out only files (exclude directories)
file_list = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]

# Print the list of files
for file in file_list:
    print(file)
