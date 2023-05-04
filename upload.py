import pymongo
import os
import sys
import certifi
from getData import get_data
from user import username, password
import json

def create_user_file():
    # create the file
    username = input("Enter username: ")
    password = input("Enter password: ")
    name_of_user = input("Enter name of user: ")
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

if not os.path.exists("user.py"):
    create_user_file()
    
from user import username, password, name_of_user


client = pymongo.MongoClient("mongodb+srv://{username}:{password}@cluster0.tk9aheu.mongodb.net/test".format(username=username, password=password), tlsCAFile=certifi.where())
db = client.Main
collection = db.molecules
# allow user to choose from one of the following collections
# DGQD
# FeXGQD
# Graphyne
# LIG
print("Choose a collection to upload to:")
print("1. DGQD")
print("2. FeXGQD")
print("3. Graphyne")
print("4. LIG")
print("5. molecules")
choice = input("Enter a number: ")
if choice == "1":
    collection = db.DGQD
elif choice == "2":
    collection = db.FeXGQD
elif choice == "3":
    collection = db.Graphyne
elif choice == "4":
    collection = db.LIG

logfiles = []
path = os.getcwd()

# get files from all subdirectories
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".log"):
            logfiles.append(os.path.join(root, file))        

# change logfiles to paths to the files
logfiles = [os.path.join(path, f) for f in logfiles]

molecules = get_data(logfiles)

for mol in molecules:
    mol = mol.__dict__
    if mol['status'] != 'Error':
        mol['identifier'] = f'{mol["name"]}.{mol["basis_sets"]}.{mol["functional"]}'

    ret_val = collection.insert_one(mol)
    if ret_val.acknowledged:
        print("Successfully inserted molecule: {name}".format(name=mol['name']))

