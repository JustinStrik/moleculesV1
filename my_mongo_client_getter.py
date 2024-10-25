import os

# if my_mongo_client.py does not exist in the current directory, copy it from the above directory
def get_my_mongo_client():
    file_absolutepath = os.path.abspath(__file__)
    file_directory = os.path.dirname(file_absolutepath)

    # check if my_mongo_client.py exists in the current directory
    if not os.path.exists(os.path.join(file_directory, "my_mongo_client.py")):
        # if it does not exist, copy it from the above directory
        import shutil
        shutil.copyfile(os.path.join(file_directory, "..", "my_mongo_client.py"), os.path.join(file_directory, "my_mongo_client.py"))
        print("Copied my_mongo_client.py from above directory")