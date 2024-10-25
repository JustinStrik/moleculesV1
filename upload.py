from math import log
import os
import re
import sys
from pymongo import MongoClient, errors # type: ignore
# from my_mongo_client import connect_to_database

# write code for if no my_mongo_client.py file exists get one from above directory
# if to see if my_mongo_client.py exists, if not, read it from above directory
file_absolutepath = os.path.abspath(__file__)
file_directory = os.path.dirname(file_absolutepath)

# check if my_mongo_client.py exists in the current directory
if not os.path.exists(os.path.join(file_directory, "my_mongo_client.py")):
    # if it does not exist, copy it from the above directory
    import shutil
    shutil.copyfile(os.path.join(file_directory, "..", "my_mongo_client.py"), os.path.join(file_directory, "my_mongo_client.py"))
    print("Copied my_mongo_client.py from above directory")

from my_mongo_client import connect_to_database
from molecule import Molecule
debug_mode = True

# def create_user_file(username, password, name_of_user):
#     # create the file
#     with open("user.py", "w") as file:
#         file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

# def check_user_file():
#     # if the user.py file does not exist, create it
#     if not os.path.exists("user.py"):
def get_user():
    if not debug_mode:
        print("Please enter your username, password, and name of user")
        username = input("Username: ")
        password = input("Password: ")
        name_of_user = input("Name of user: ")
    # in debug mode, use the user.py file
    else:
        if not os.path.exists("user.py"):
            username = input("Username: ")
            password = input("Password: ")
            name_of_user = input("Name of user: ")
        else:        
            from user import username, password, name_of_user
    return username, password, name_of_user

# create_user_file(username, password, name_of_user)   

def announce_user():
    print("Username: {username}".format(username=username))
    print("Password: {password}".format(password=password))
    print("Name of user: {name_of_user}".format(name_of_user=name_of_user)) 

def connect_to_db(username, password):
    # connect to the database
    # try, if doesnt work, throw error
    global client
    try:
        # Set a timeout for the connection (in milliseconds)
        client = connect_to_database(username, password)
        
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


def get_directory():
    if not debug_mode:
        if (len(sys.argv) > 1):
            # if the user passed in a directory, use that directory
            directory = sys.argv[1]
        else:
            # prompt user for directory
            directory = input("Enter the FULL PATH directory of the desired files (LEAVE BLANK for current directory): ")
    else:
        if (len(sys.argv) > 1):
            # if the user passed in a directory, use that directory
            directory = sys.argv[1]
        else:
            directory = ""

    # reformat directory to be compatible with os.path.join
    directory = directory.replace('\\', '/')
    if directory != "":
        print("Directory: {directory}".format(directory=directory))
    else:
        print("Directory: current directory")
        directory = "." # current directory notation to be used in os.path.join
    return directory

def get_all_files_from_directory(directory):
    # get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    # change to absolute path
    files = [os.path.abspath(f) for f in files]
    return files

# returns map of suffixes to an array of analysis types
def get_desired_suffixes():
    # suffixes as keys and analysis types as values
    suffixes = {}
    for type in analysis_types:
        if type.name == "Type_Example":
            continue
        # get type with that name, can be more than one type with the same suffix
        if type.suffix not in suffixes:
            suffixes[type.suffix] = []
        
        suffixes[type.suffix].append(type)

    # returns map of suffixes to an array of analysis types
    return suffixes

def split_suffixes_into_analysis_types(suffixes):
    # analysis type has function called     def check_if_correct_file_type(self, lines):
        # TODO change to the test that only the correct file type would pass

        # to ensure the file is the correct type, have it check to see if the file
        # passes a test that only the correct file type would pass
        # for example, Gaussian files start with 'Entering Gaussian System'
        # print(f"check_if_correct_file_type not implemeneted yet in {self.mol.name}")
        # pass

        # # example for Gaussian"
        # # check first line for 'Entering Gaussian System'
        # return 'Entering Gaussian System' in lines[0]

    # for each suffix, check if it is the correct file type
    pass


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

    # change to relative to the current running directory
    current_directory = os.path.dirname(os.path.realpath(__file__))
    analysis_types = [f for f in os.listdir(os.path.join(current_directory, "analysis_types")) if os.path.isfile(os.path.join(current_directory, "analysis_types", f, f + ".py")) and f != "Type_Example"]
    # change analysis_types to be a list of objects that are the analysis types from the analysis_types directory
    # to do that, import the module and get the class from the module
    for i in range(len(analysis_types)):
        import_statement = "from analysis_types.{analysis_type}.{analysis_type} import {analysis_type}".format(analysis_type=analysis_types[i])
        exec(import_statement)

    # replace the string with the object
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

# checks to see if mol.identifier is already in the database
def check_for_duplicates(molecules):
    conflict_molecules = []
    for mol in molecules:
        # doc_id = f'{mol.name}_{mol.basis_sets}_{mol.functional}'
        if mol.status == "Error":
            if mol.identifier == "":
                mol.identifier = f'{mol.name}_{mol.basis_sets}_{mol.functional}'

        existing_doc = collection.find_one({"identifier": mol.identifier})
        if existing_doc:
            # if the document exists, ask the user if they want to keep the original or override
            if set(mol.__dict__.keys()).intersection(set(existing_doc.keys())):
                # if the keys are the same, check if the values are the same
                if mol.__dict__ != existing_doc:
                    # if the values are the same, do nothing
                    print(f"Conflict: molecule with identifier {mol.identifier} already exists in the database. Upload cancelled.")
                    conflict_molecules.append(mol)
                    # molecules.remove(mol) # can't remove from list while iterating
                else:
                    print("Exists")

    # remove the molecules that are in conflict
    molecules = [mol for mol in molecules if mol not in conflict_molecules]

    return conflict_molecules, molecules

def duplicate_error_messages(duplicates):
    for mol in duplicates:
        # with f strings, the curly braces need to be doubled
        print(f"Duplicate molecule found: {mol.name} with basis set {mol.basis_sets} and functional {mol.functional}")

def upload_molecules_to_db(molecules):
    failed_molecules = []
    for mol in molecules:
        mol.analysis_type = mol.analysis_type.name # change the analysis type to a string, cannot upload object type to database
        toDB = mol.__dict__
        try:
            collection.insert_one(toDB)
            print(f"Uploaded molecule to the database for molecule: {mol.name} Analysis type: {mol.analysis_type}")
            print(f"Identifier: {mol.identifier}")
        except errors.PyMongoError as err:
            # raise ConnectionError("Failed to upload molecule to the database for molecule: {name} Analysis type: {analysis_type.name}") from err
            # print instead
            failed_molecules.append(mol)
            print(f"Failed to upload molecule with identifier {mol.identifier} to the database for molecule: {mol.name} Analysis type: {mol.analysis_type}")
            print("The error was:" + err)

    print("Total successful uploads: {num}".format(num=len(molecules) - len(failed_molecules))) 
    print("Total failed uploads: {num}".format(num=len(failed_molecules)))

def get_all_molecule_data(files_dict, name_of_user, suffixes):
    # files_dict is a dictionary with suffixes as keys and lists of files as values
    molecules = []

    for suffix in files_dict:
        # file must be absolute path
        for file in files_dict[suffix]:

            # molecule = Molecule(name_of_user, analysis_type=suffixes[suffix]) # custom object from molecule.py

            # molecule.get_data() # implicit call to get_data method of the analysis type
            # molecules.append(molecule)

            # if suffix size is >1, check to see which analysis type it is
            if len(suffixes[suffix]) > 1:
                for analysis_type in suffixes[suffix]:
                    if analysis_type.check_if_correct_file_type(file):
                        molecule = Molecule(name_of_user, analysis_type, file)
                        molecules.append(molecule)
                        break
            else:
                molecule = Molecule(name_of_user, suffixes[suffix][0], file) # for first element in the list, only one element
                molecules.append(molecule)

    return molecules

# main function
if __name__ == "__main__":
    # check_user_file() # now asks for input every time
    username, password, name_of_user = get_user()
    # announce_user()

    client = connect_to_db(username, password)
    establish_connection() # gets db and collection

    get_analysis_types()

    # suffizes as keys and analysis types as values
    suffixes = get_desired_suffixes() # gets file suffixes for analysis types (file types in directory that can be parsed)

    directory = get_directory()
    molecule_files = get_files_from_directory_with_correct_suffixes(directory, suffixes)

    # get all the data from the files
    molecules = get_all_molecule_data(molecule_files, name_of_user, suffixes)
    duplicates, molecules = check_for_duplicates(molecules)
    duplicate_error_messages(duplicates)

    upload_molecules_to_db(molecules)
    pass


# class Analysis_Manager:
#     def get_all_analysis_types():
#         # names of subdirectories in the analysis_types directory
#         # each folder in the current directory is a different analysis type
#         # under each folder is a python file with the same name as the folder
#         # the python file contains the analysis type class
#         # for each folder in the analysis_types directory
#         for folder in os.listdir("analysis_types"):
#             # import all those classes
#             import_statement = "from analysis_types.{folder}.{folder} import {folder}".format(folder=folder)
#             exec(import_statement)
#             # get the class from the module
#             analysis_type = getattr(getattr(getattr(analysis_types_module, folder), folder), folder)
#             print(analysis_type)
#             # instantiate the class