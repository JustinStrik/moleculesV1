# import datetime
# import os
# import tkinter as tk
# from tkinter import filedialog
# import json
# import csv
# from enum import Enum
# import pymongo
# # from pymongo import MongoClient
# from tkinter import messagebox
# import functools

# # to override, pull from db and update data by adding properties

# # if the user file does not exist (they have never logged in before), create it
# # file should just contain variables username and password
# # create a gui to ask for the username and password
# def get_user_info():
#     create_user_window = tk.Tk()
#     create_user_window.title("Create user file")
#     create_user_window.geometry("300x200")

#     # create a label and entry for the username
#     username_label = tk.Label(create_user_window, text="Username")
#     username_label.pack()
#     username_entry = tk.Entry(create_user_window)
#     username_entry.pack()

#     # create a label and entry for the password
#     password_label = tk.Label(create_user_window, text="Password")
#     password_label.pack()
#     password_entry = tk.Entry(create_user_window)
#     password_entry.pack()

#     name_of_user_label = tk.Label(create_user_window, text="Name of user")
#     name_of_user_label.pack()
#     name_of_user_entry = tk.Entry(create_user_window)
#     name_of_user_entry.pack()

#     # create a button to create the file
#     create_button = tk.Button(create_user_window, text="Create file", command=lambda: create_user_file(username_entry.get(), password_entry.get(), name_of_user_entry.get()))
#     create_button.pack()

#     # create a button to close the window
#     close_button = tk.Button(create_user_window, text="Close", command=create_user_window.destroy)
#     close_button.pack()

#     create_user_window.mainloop()

# def create_user_file(username, password, name_of_user):
#     # create the file
#     with open("user.py", "w") as file:
#         file.write("# this file stores usernames and passwords for the database\nusername=\"{username}\"\npassword=\"{password}\"\nname_of_user=\"{name_of_user}\"".format(username=username, password=password, name_of_user=name_of_user))

# # if the user.py file does not exist, create it
# if not os.path.exists("user.py"):
#     get_user_info()
# from user import username, password, name_of_user

# print("REMOVED")
# cluster = REMOVED

# class Status(Enum):
#     CONFLICT = 'conflict' # item is already in the database, but with the same properties (requires override)
#     WARNING = 'warning' # item is already in the database, but with different properties
#     SUCCESS = 'success' # item was successfully added to the database
#     ABORTED = 'aborted' # user aborted the upload
#     EXISTS = 'exists' # exact item is already in the database

# # Connect to the database
# db = cluster["moleculesTestV1"]
# collection = db["moleculesTesting1"]

# # Create a list of labels for the identPopup window
# labels = []
# statuses = []

# # query to find  documents in the database and make it accessible to the rest of the program
# query = {}
# query_entry = ''
# query_response = ''
# response_text_widget = '' # will be initialized later as a widget

# def deleteEverything():
#     # clear the database
#     return collection.delete_many({})

# # needed to make this so that the function ran with the parameters from when the button was instantiated
# def make_override_callback(molecule, statuses, row):
#     return lambda: push_to_db(molecule, statuses, row)

# def push_to_db(molecule, statuses, row):
#     collection.insert_one(molecule[0])
#     index = statuses.index(molecule)  # get the index of the molecule in the statuses list
#     new_molecule = (molecule[0], Status.SUCCESS)  # create a new tuple with the updated status
#     statuses[index] = new_molecule  # replace the old tuple with the new one
#     labels[row].config(bg='green')

# def make_abort_callback(molecule, statuses):
#     return lambda: abort_upload(molecule, statuses)

# def abort_upload(molecule, statuses):
#     index = statuses.index(molecule)  # get the index of the molecule in the statuses list
#     labels[index].config(bg='light grey')
#     new_molecule = (molecule[0], Status.ABORTED)  # create a new tuple with the updated status
#     statuses[index] = new_molecule  # replace the old tuple with the new one

# def query_db(query_entry) -> dict:
#     # convert the query string into a dictionary

#     # query string format: key1:value1,key2:value2,key3:value3
#     query = {}
#     for item in query_entry.split(","):
#         key, value = item.split(":")
#         query[key] = value

#     # return the query from the mongo database
#     query_response = collection.find(query)
#     for x in query_response:
#         print(x)
#     update_response_text_widget()

# def on_retrieve():
#     # create a new window to show the retrieved content
#     retrieve_window = tk.Tk()
#     retrieve_window.title("Retrieved Content")
    
#     # insert the content into a text widget
#     query_response = "Some content that was retrieved from the database."

#     # for the response from the database
#     response_text_widget = tk.Text(retrieve_window)
#     response_text_widget.insert(tk.END, query_response)
#     response_text_widget.pack()

#     # add an entry for the user to enter a query
#     query_entry = tk.Entry(retrieve_window)
#     query_entry.pack()

#     # add a button to retrieve the content
#     retrieve_button = tk.Button(retrieve_window, text="Retrieve", command=lambda:query_db(query_entry.get()))
#     retrieve_button.pack()

#     # once query is entered, disyplay the content in the text widget
#     # text_widget.insert(tk.END, content)

#     retrieve_window.mainloop()


# def update_response_text_widget():
#     # update the response text widget with the query response
#     response_text_widget.delete(1.0, tk.END)
#     response_text_widget.insert(tk.END, query_response)

# def on_close():
#     # close the popup window
#     actionPopup.destroy()

# def show_identifiers(statuses):
#     # Create the identPopup window
#     identPopup = tk.Tk()

#     # what follows is a line of code that will hide the window that says tk
#     identPopup.title("Identifiers")

#     # Add a label to the window
#     label = tk.Label(identPopup, text="These are the identifiers in the file:")
#     label.grid(row=0, column=0, columnspan=2)

#     # Add a button to close the window
#     button_close = tk.Button(identPopup, text="Close", command=identPopup.destroy)
#     button_close.grid(row=len(statuses)+3, column=1, columnspan=2)

#     # Display the identifiers in rows
#     for row, molecule in enumerate(statuses):
#         # Create a Label widget for each column in the row
#         label = tk.Label(identPopup, text=molecule[0]["identifier"])
#         labels.append(label) # add the label to the list of labels for ease of color changing
#         label.grid(row=row+2, column=0)

#         if molecule[1] == Status.CONFLICT: # if the status is conflict, add an override button which will remove the document from the database and add the new one
#             button_override = tk.Button(identPopup, text="Override", command=make_override_callback(molecule, statuses, row))
#             button_abort = tk.Button(identPopup, text="Abort", command=make_abort_callback(molecule, statuses))
#             button_override.grid(row=row+2, column=1)
#             button_abort.grid(row=row+2, column=2)
#         elif molecule[1] == Status.WARNING: # if the status is warning, add an abort button which will not add the document to the database
#             button_abort = tk.Button(identPopup, text="Abort", command=make_abort_callback(molecule, statuses))
#             button_remove = tk.Button(identPopup, text="Remove", command=identPopup.destroy)
#             button_abort.grid(row=row+2, column=1)
#             button_remove.grid(row=row+2, column=2)
#         # elif molecule[1] == Status.SUCCESS: # if the status is success, no buttons are needed


#         # Set the background color based on the status
#         if molecule[1] == Status.CONFLICT:
#             label.config(bg='red')
#         elif molecule[1] == Status.WARNING:
#             label.config(bg='yellow')
#         elif molecule[1] == Status.SUCCESS:
#             label.config(bg='light green')
#         elif molecule[1] == Status.EXISTS:
#             label.config(bg='light blue')


#     # Make the identPopup window modal
#     identPopup.geometry("800x600")
#     identPopup.mainloop()

# def choose_file():
#     # Open a GUI window to browse for a file

#     file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

#     # If the user canceled the file selection, do nothing
#     if not file_path:
#         return

#     with open(file_path, "r") as f:
#         try:
#             data = json.load(f)
#         except json.JSONDecodeError:
#             messagebox.showerror("Error", "Selected file is not a valid JSON or CSV file.")
#             return
        
#     upload_file(data)    

# def upload_file(data):

#     # Check if db has a document with the same identifier
#     # If it does, ask the user if they want to override it
#     # If they do, update the document

#     for molecule in data:
#         # Check if the identifier already exists in the database
#         doc_id = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
#         existing_doc = collection.find_one({"identifier": doc_id})

#         if existing_doc:
#             # If the document exists, ask the user if they want to keep the original or override
#             # if the document exists, check if any of the keys are the same, if even one is, there is a conflict
#             if set(molecule.keys()).intersection(set(existing_doc.keys())):
#                 # If the keys are the same, check if the values are the same
#                 if molecule != existing_doc:
#                     # If the values are the same, do nothing
#                     statuses.insert(0, (molecule, Status.CONFLICT)) # push front
#                     continue
#                 else:
#                     statuses.append((molecule, Status.EXISTS))
#             else:
#                 statuses.append((molecule, Status.WARNING))
#         else:
#             # If the document does not exist, insert it into the database
#             molecule["identifier"] = doc_id
#             molecule["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             molecule["uploaded_by"] = name_of_user
#             collection.insert_one(molecule)
#             statuses.append((molecule, Status.SUCCESS))

#     show_identifiers(statuses)
#     return statuses

# if __name__ == "__main__":

#     # Define the actionPopup window
#     actionPopup = tk.Tk() 
#     actionPopup.title("Choose an action")

#     # Create the buttons
#     upload_button = tk.Button(actionPopup, text="Upload", command=choose_file) # upload_file(choose_file())
#     retrieve_button = tk.Button(actionPopup, text="Retrieve", command=on_retrieve)
#     close_button = tk.Button(actionPopup, text="Close", command=actionPopup.destroy)

#     # Add the buttons to the actionPopup window
#     upload_button.pack(pady=5)
#     retrieve_button.pack(pady=5)
#     close_button.pack(pady=5)

#     # Run the main window
#     actionPopup.grab_set()
#     actionPopup.geometry("800x600")
#     actionPopup.mainloop()