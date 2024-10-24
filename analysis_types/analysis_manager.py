import analysis_type
import os

class Analysis_Manager:
    def get_all_analysis_types():
        # names of subdirectories in the analysis_types directory
        # each folder in the current directory is a different analysis type
        # under each folder is a python file with the same name as the folder
        # the python file contains the analysis type class
        # for each folder in the analysis_types directory
        for folder in os.listdir("analysis_types"):
            # import all those classes
            import_statement = "from analysis_types.{folder}.{folder} import {folder}".format(folder=folder)
            exec(import_statement)
            # get the class from the module
            analysis_type = getattr(getattr(getattr(analysis_types_module, folder), folder), folder)
            print(analysis_type)
            # instantiate the class