from math import log
import os
import re
import sys
from pymongo import MongoClient, errors # type: ignore
from pymongo.server_api import ServerApi
from pyparsing import col
from analysis_types import analysis_type
from analysis_types.Gaussian.Gaussian import Gaussian
from getOrcaData import get_orca_data
from getData import get_data
from molecule import Molecule
import molecule
debug_mode = True

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


if not debug_mode:
    if (len(sys.argv) > 1):
        # if the user passed in a directory, use that directory
        directory = sys.argv[1]
    else:
        # prompt user for directory
        directory = input("Enter the directory of the log files (blank for current directory): ")
else:
    directory = ""

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

def get_desired_suffixes():
    # suffixes as keys and analysis types as values
    suffixes = {}
    for type in analysis_types:
        suffixes[type.suffix] = type

    return suffixes

def get_files_from_directory_with_correct_suffixes(directory, suffixes):

    all_files = get_all_files_from_directory(directory)
    sorted_files = {} # dictionary with suffixes as keys and lists of files as values

    # # get all files that end with .log in the database directory
    # logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]
    # # outfiles are orca output files
    # outfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.out')]

    # make suffix-specific lists
    for suffix in suffixes:
        sorted_files[suffix] = [f for f in all_files if f.endswith(suffix)]

    return sorted_files

def get_analysis_types():
    # names of subdirectories in the analysis_types directory
    # import analysis_type Gaussian from analysis_types/Gaussian/Gaussian.py
    import analysis_types as analysis_types_module

    global analysis_types
    # analysis_types = [f for f in os.listdir("analysis_types") if os.path.isdir(os.path.join("analysis_types", f))]
    # include if the file is a python file, was originally just the directory and getting __pycache__ as well
    analysis_types = [f for f in os.listdir("analysis_types") if os.path.isfile(os.path.join("analysis_types", f, f + ".py"))]

    # change analysis_types to be a list of objects that are the analysis types from the analysis_types directory
    for i in range(len(analysis_types)):
        analysis_types[i] = getattr(getattr(getattr(analysis_types_module, analysis_types[i]), analysis_types[i]), analysis_types[i])()

# # print all the log files
# print("Log files:")
# for logfile in logfiles:
#     print(logfile)

# # print all the out files
# print("Out files:")
# for outfile in outfiles:
#     print(outfile)

# array of molecules to upload
# molecules = get_data(logfiles)

# mol_orca = get_orca_data(outfiles)

# change all molecules.uploader to name_of_user in just one line
# for mol in molecules:
#     mol.uploader = name_of_user

def upload_molecules_to_db(molecules):
    for mol in molecules:
        mol.analysis_type = mol.analysis_type.name # change the analysis type to a string, cannot upload object type to database
        toDB = mol.__dict__
        try:
            collection.insert_one(toDB)
        except errors.PyMongoError as err:
            raise ConnectionError("Failed to upload molecule to the database for molecule: {mol.name} Analysis type: {mol.analysis_type.name}") from err

def get_all_molecule_data(files_dict, name_of_user, suffixes):
    # files_dict is a dictionary with suffixes as keys and lists of files as values
    molecules = []

    for suffix in files_dict:
        for file in files_dict[suffix]:
            # molecule = Molecule(name_of_user, analysis_type=suffixes[suffix]) # custom object from molecule.py

            # molecule.get_data() # implicit call to get_data method of the analysis type
            # molecules.append(molecule)
            molecule = Molecule(name_of_user, suffixes[suffix])
            molecule.get_data(file)
            molecules.append(molecule)

    return molecules

# main function
if __name__ == "__main__":
    check_user_file()
    from user import username, password, name_of_user
    announce_user()

    client = connect_to_db()
    establish_connection() # gets db and collection

    get_analysis_types()

    # suffizes as keys and analysis types as values
    suffixes = get_desired_suffixes() # gets file suffixes for analysis types

    molecule_files = get_files_from_directory_with_correct_suffixes(directory, suffixes)

    # get all the data from the files
    molecules = get_all_molecule_data(molecule_files, name_of_user, suffixes)
    upload_molecules_to_db(molecules)
    pass

