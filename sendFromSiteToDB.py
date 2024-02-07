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

# rewrite the above with teh following string mongodb+srv://<username>:<password>@cluster0.tk9aheu.mongodb.net/, fill in variables in the same way
cluster = MongoClient("mongodb+srv://{username}:{password}@cluster0.tk9aheu.mongodb.net/?retryWrites=true&w=majority".format(username=username, password=password),
tls=True,
tlsAllowInvalidCertificates=True)


db = cluster["Main"]
collection = db["XYZfromSite"]

# make var of type dict
molecules = []

# open all files that end in xyz in the current directory
xyzfiles = [f for f in os.listdir() if f.endswith(".xyz")]
# make dicts out of each file and store in an array
for xyzfile in xyzfiles:
    # open the file
    with open(xyzfile, "r") as file:
        molecule = {}
        # store the file in a dict
        molecule["name"] = xyzfile
        molecule["xyz"] = file.read()
        # add the dict to the array
        molecules.append(molecule)
        # insert the dict into the database

collection.insert_many(molecules)