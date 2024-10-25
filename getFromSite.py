import os
from datetime import datetime
from my_mongo_client_getter import get_my_mongo_client
get_my_mongo_client() # this will copy my_mongo_client.py from the above directory if it does not exist in the current directory
from my_mongo_client import connect_to_database

# def create_user_file(username, password, name_of_user):
#     # create the file
#     with open("user.py", "w") as file:
#         file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

# if the user.py file does not exist, create it
print("Please enter your username, password, and name of user")
username = input("Username: ")
password = input("Password: ")
name_of_user = input("Name of user: ")
# create_user_file(username, password, name_of_user)

from user import username, password, name_of_user

print("Username: {username}".format(username=username))
print("Password: {password}".format(password=password))
print("Name of user: {name_of_user}".format(name_of_user=name_of_user))

# connect to the database
cluster = connect_to_database(username, password)

db = cluster["Main"]
collection = db["XYZfromSite"]

# pull data from the specified folder to a local file
now = datetime.now()
folder_name = now.strftime("%m-%d-%y_%H-%M-%S")
os.mkdir(folder_name)

# find where uploader = name of user
mols_to_pull = collection.find({"uploader": name_of_user})

# write each object to a file in the fromDB folder
for molecule in mols_to_pull:
    open(os.path.join(folder_name, molecule["name"]), "w").write(molecule["xyz"])

# delete everything from the database collection
collection.delete_many({'uploader': name_of_user})
