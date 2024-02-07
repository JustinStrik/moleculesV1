import os
import sys
from pymongo import MongoClient
from getData import get_data

def create_user_file(username, password, name_of_user):
    # create the file
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

# if the user.py file does not exist, create it
if not os.path.exists("user.py"):
    print("Please enter your username, password, and name of user")
    username = input("Username: ")
    password = input("Password: ")
    name_of_user = input("Name of user: ")
    create_user_file(username, password, name_of_user)

from user import username, password, name_of_user

print("Username: {username}".format(username=username))
print("Password: {password}".format(password=password))
print("Name of user: {name_of_user}".format(name_of_user=name_of_user))

# connect to the database
cluster = MongoClient("mongodb+srv://{username}:{password}@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority".format(username=username, password=password),     
tls=True,
tlsAllowInvalidCertificates=True)
                             
                             # ?)
db = cluster["moleculesTestV1"]
collection = db["moleculesTesting1"]

if (len(sys.argv) > 1):
    # if the user passed in a directory, use that directory
    directory = sys.argv[1]
else:
    # prompt user for directory
    directory = input("Enter the directory of the log files: ")

# reformat directory to be compatible with os.path.join
directory = directory.replace('\\', '/')
print("Directory: {directory}".format(directory=directory))

# get all files that end with .log in the database directory
logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]

# print all the log files
print("Log files:")
for logfile in logfiles:
    print(logfile)

# array of molecules to upload
molecules = get_data(logfiles)

for mol in molecules:
    toDB = mol.__dict__
    collection.insert_one(toDB)