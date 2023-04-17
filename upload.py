import pymongo
import os
import sys
import certifi
from getData import get_data
from user import username, password
import json

# # test to see if a simply function from pymongo works
# client = MongoClient('localhost', 27017)

def create_user_file():
    # create the file
    username = input("Enter username: ")
    password = input("Enter password: ")
    name_of_user = input("Enter name of user: ")
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

if not os.path.exists("user.py"):
    create_user_file()
# from user import username, password, name_of_user

# mongodb+srv://jstrik:strik@cluster0.tk9aheu.mongodb.net/?retryWrites=true&w=majority
# mongodb+srv://jstrik:strik@cluster0.tk9aheu.mongodb.net/test

client = pymongo.MongoClient("mongodb+srv://{username}:{password}@cluster0.tk9aheu.mongodb.net/test".format(username=username, password=password), tlsCAFile=certifi.where())
db = client.Main
collection = db.molecules


#  client = pymongo.MongoClient("mongodb+srv://jstrik:strik@cluster0.tk9aheu.mongodb.net/?retryWrites=true&w=majority")
# db = client.Main
# collection = db.molecules


logfiles = []
path = ''
if (len(sys.argv) > 1):
    # see if directory or file or if it exists
    path = sys.argv[1]
else:
    print("No path given")
    path = input("Enter path (or . for current directory): ")

if path == '.': 
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".log"):
            logfiles.append(file)
elif os.path.isdir(path):
    for file in os.listdir(path):
        if file.endswith(".log"):
            logfiles.append(file)
elif os.path.isfile(path):
    logfiles.append(path)
else:  
    # not a file or directory
    print("Not a file or directory")
    sys.exit()

# change logfiles to paths to the files
logfiles = [os.path.join(path, f) for f in logfiles]

molecules = get_data(logfiles)

# insert the data into the database

# debug output to json
# with open("testData6.json", "w") as f:
#     for mol in molecules:
#         mol = mol.__dict__
#         if mol['status'] != 'Error':
#             mol['identifier'] = f'{mol["name"]}_{mol["basis_sets"]}_{mol["functional"]}'
#         f.write(json.dumps(mol))


for mol in molecules:
    mol = mol.__dict__
    if mol['status'] != 'Error':
        mol['identifier'] = f'{mol["name"]}_{mol["basis_sets"]}_{mol["functional"]}'

    ret_val = collection.insert_one(mol)
    if ret_val.acknowledged:
        print("Successfully inserted molecule: {name}".format(name=mol['name']))

