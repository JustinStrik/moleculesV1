from pymongo import MongoClient
import os
import sys
from getData import get_data

def create_user_file(username, password, name_of_user):
    # create the file
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

if not os.path.exists("user.py"):
    create_user_file()
from user import username, password, name_of_user

# Connect to the database
cluster = MongoClient("mongodb+srv://{username}:{password}@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority".format(username=username, password=password))
db = cluster["moleculesTesting1"]
collection = db["molecules"]

logfiles = []
path = ''
if (len(sys.argv) > 1):
    # see if directory or file or if it exists
    path = sys.argv[1]
else:
    print("No path given")
    path = input("Enter path: ")

if os.path.isdir(path):
    for file in os.listdir(path):
        if file.endswith(".log"):
            logfiles.append(file)
elif os.path.isfile(path):
    logfiles.append(path)
else:  
    # not a file or directory
    print("Not a file or directory")
    sys.exit()

molecules = get_data(logfiles)

# insert the data into the database
collection.insert_many(molecules)
