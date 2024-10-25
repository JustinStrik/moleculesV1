import os
import sys
# take in input for name of analysis type
new_analysis_type = input("Enter the name of the new analysis type: ")

# line to create folder
current_file_path = os.path.abspath(__file__)

# line to create folder
# add to current path the new folder name
new_folder_path = os.path.join(os.path.dirname(current_file_path), f"{new_analysis_type}")

# line to create folder
os.makedirs(new_folder_path)

# # line to create file, which is a copy of the template Type_Example.py from Type_Example/Type_Example.py
# # replace Type_Example with new_analysis_type in the file
# with open(f"Type_Example/Type_Example.py", "r") as f:
# with open({current_file_path}/Type_Example/Type_Example.py, "r") as f
with open(f"{os.path.dirname(current_file_path)}/Type_Example/Type_Example.py", "r") as f:
    data = f.read()
    data = data.replace("Type_Example", new_analysis_type)

    # line to create file of the new analysis type
    with open(f"{new_folder_path}/{new_analysis_type}.py", "w") as f:
        f.write(data)

