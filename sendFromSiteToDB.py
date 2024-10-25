import os
import sys

from pyparsing import col
from sympy import use
from my_mongo_client import connect_to_database

def create_user_file(username, password, name_of_user):
    # create the file
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

# NO LONGER USE USER FILE, INPUT DIRECTLY EACH TIME
# if the user.py file does not exist, create it
# if not os.path.exists("user.py"):
#     print("Please enter your username, password, and name of user")
#     username = input("Username: ")
#     password = input("Password: ")
#     name_of_user = input("Name of user: ")
#     create_user_file(username, password, name_of_user)

# from user import username, password, name_of_user


def get_user():
    print("Please enter your username, password, and name of user")
    username = input("Username: ")
    password = input("Password: ")
    name_of_user = input("Name of user: ")
    return username, password, name_of_user

def make_xyz_files_molecules():
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

    return molecules

if __name__ == "__main__":
    username, password, name_of_user = get_user()

    cluster = connect_to_database(username, password)
    db = cluster["Main"]
    collection = db["XYZfromSite"]

    molecules = make_xyz_files_molecules()
    collection.insert_many(molecules)
