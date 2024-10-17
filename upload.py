import glob
import os
import sys
from pymongo import MongoClient, errors # type: ignore
from pymongo.server_api import ServerApi
from pyparsing import col
from scipy import cluster
from getOrcaData import get_orca_data
from getData import get_data

def create_user_file(username, password, name_of_user):
    # create the file
    with open("user.py", "w") as file:
        file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

def check_user_file():
    # if the user.py file does not exist, create it
    if not os.path.exists("user.py"):
        print("Please enter your username, password, and name of user")
        username = input("Username: ")
        password = input("Password: ")
        name_of_user = input("Name of user: ")
        create_user_file(username, password, name_of_user)   

def announce_user():
    from user import username, password, name_of_user
    print("Username: {username}".format(username=username))
    print("Password: {password}".format(password=password))
    print("Name of user: {name_of_user}".format(name_of_user=name_of_user)) 

def connect_to_db():
    # connect to the database
    # try, if doesnt work, throw error
    global client
    try:
        # Set a timeout for the connection (in milliseconds)
        client = MongoClient("mongodb+srv://{username}:{password}@cluster0.tk9aheu.mongodb.net/test".format(username=username, password=password),     
            tls=True,
            tlsAllowInvalidCertificates=True)
        
        # Attempt to connect to the server
        client.server_info()  # Will throw an exception if unable to connect
        
        print("Connected to the database successfully")
        return client
    except errors.ServerSelectionTimeoutError as err:
        raise ConnectionError("Failed to connect to the database: Timeout") from err
    except errors.ConnectionError as err:
        raise ConnectionError("Failed to connect to the database: Connection error") from err
    except Exception as err:
        raise ConnectionError("Failed to connect to the database: An unexpected error occurred") from err

    
def establish_connection():
    # connect to the database
    global db, collection
    db = client["Main"]
    collection = db["molecules"]


if (len(sys.argv) > 1):
    # if the user passed in a directory, use that directory
    directory = sys.argv[1]
else:
    # prompt user for directory
    directory = input("Enter the directory of the log files (blank for current directory): ")

# reformat directory to be compatible with os.path.join
directory = directory.replace('\\', '/')
if directory != "":
    print("Directory: {directory}".format(directory=directory))
else:
    print("Directory: current directory")
    directory = "." # current directory notation to be used in os.path.join

def get_all_files_from_directory(directory):
    # get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    return files

def get_files_from_directory_with_correct_suffixes(directory):
    global logfiles, outfiles # temporary, hopefully better method soon

    all_files = get_all_files_from_directory(directory)

    # get all files that end with .log in the database directory
    logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]
    # outfiles are orca output files
    outfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.out')]

def get_analysis_types():
    # names of subdirectories in the analysis_types directory
    global analysis_types
    analysis_types = [f for f in os.listdir("analysis_types") if os.path.isdir(os.path.join("analysis_types", f))]

# print all the log files
print("Log files:")
for logfile in logfiles:
    print(logfile)

# print all the out files
print("Out files:")
for outfile in outfiles:
    print(outfile)

# array of molecules to upload
molecules = get_data(logfiles)

mol_orca = get_orca_data(outfiles)

# change all molecules.uploader to name_of_user in just one line
for mol in molecules:
    mol.uploader = name_of_user

for mol in molecules:
    toDB = mol.__dict__
    collection.insert_one(toDB)

def get_all_molecule_data(arrs):
    pass

# main function
if __name__ == "__main__":
    check_user_file()
    from user import username, password, name_of_user
    announce_user()

    client = connect_to_db()
    establish_connection() # gets db and collection

    get_analysis_types()
    get_files_from_directory_with_correct_suffixes(directory)

    pass

