import pymongo
from pymongo import MongoClient
import mongoengine
import os
import sys
from getData import get_data

# # test to see if a simply function from pymongo works
# client = MongoClient('localhost', 27017)

def create_user_file(username, password, name_of_user):
    # create the file
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

if not os.path.exists("user.py"):
    create_user_file()
from user import username, password, name_of_user


client = pymongo.MongoClient()
db = client.LiuDB
collection = db.molecules

#print('mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority')

# print connection string
#print("mongodb+srv://{username}:{password}@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority".format(username=username, password=password))
# Connect to the database
#client = pymongo.MongoClient('mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority')
#db = client.moleculesTesting1

# db = cluster['moleculesTesting1']
#collection = db['molecules']

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

# change logfiles to paths to the files
logfiles = [os.path.join(path, f) for f in logfiles]

molecules = get_data(logfiles)

# insert the data into the database
for mol in molecules:
    mol = mol.__dict__
    mol['user'] = name_of_user
    collection.insert_one(mol)
