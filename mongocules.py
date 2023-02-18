import tkinter as tk
from tkinter import filedialog
import json
from enum import Enum
import pymongo
from pymongo import MongoClient
from tkinter import messagebox
import dbFunctions

# Connect to the MongoDB, change the connection string per your MongoDB environment
cluster = MongoClient("mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority")

class Status(Enum):
    CONFLICT = 'conflict' # item is already in the database, but with the same properties (requires override)
    WARNING = 'warning' # item is already in the database, but with different properties
    SUCCESS = 'success' # item was successfully added to the database
    ABORTED = 'aborted' # user aborted the upload
    EXISTS = 'exists' # exact item is already in the database

# Connect to the database
db = cluster["moleculesTestV1"]
collection = db["moleculesTesting1"]

# Create a list of labels for the identPopup window
labels = []

def push_to_db(molecule, statuses, row):
    collection.insert_one(molecule[0])
    index = statuses.index(molecule)  # get the index of the molecule in the statuses list
    new_molecule = (molecule[0], Status.SUCCESS)  # create a new tuple with the updated status
    statuses[index] = new_molecule  # replace the old tuple with the new one
    labels[row].config(bg='green')

def abort_upload(molecule, statuses):
    index = statuses.index(molecule)  # get the index of the molecule in the statuses list
    new_molecule = (molecule[0], Status.ABORTED)  # create a new tuple with the updated status
    statuses[index] = new_molecule  # replace the old tuple with the new one

# BOTH FUNCTIONS BELOW ARE NOT USED IN THE CURRENT VERSION OF THE PROGRAM
def on_retrieve():
    # create a new window to show the retrieved content
    retrieve_window = tk.Toplevel(root)
    retrieve_window.title("Retrieved Content")
    
    # insert the content into a text widget
    content = "Some content that was retrieved from the database."
    text_widget = tk.Text(retrieve_window)
    text_widget.insert(tk.END, content)
    text_widget.pack()

def on_close():
    # close the popup window
    actionPopup.destroy()

def show_identifiers(statuses):
    # Create the identPopup window
    identPopupRoot = tk.Tk()
    identPopupRoot.withdraw()
    identPopup = tk.Toplevel(identPopupRoot)

    # what follows is a line of code that will hide the window that says tk
    identPopup.title("Identifiers")

    # Add a label to the window
    label = tk.Label(identPopup, text="These are the identifiers in the file:")
    label.grid(row=0, column=0, columnspan=2)

    # Add a button to close the window
    button_close = tk.Button(identPopup, text="Close", command=identPopupRoot.destroy)
    button_close.grid(row=len(statuses)+3, column=1, columnspan=2)

    # Display the identifiers in rows
    for row, molecule in enumerate(statuses):
        # Create a Label widget for each column in the row
        label = tk.Label(identPopup, text=molecule[0]["identifier"])
        labels.append(label) # add the label to the list of labels for ease of color changing
        label.grid(row=row+2, column=0)

        if molecule[1] == Status.CONFLICT: # if the status is conflict, add an override button which will remove the document from the database and add the new one
            button_override = tk.Button(identPopup, text="Override", command=push_to_db(molecule, statuses, row))
            button_remove = tk.Button(identPopup, text="Remove", command=identPopup.destroy)
            button_override.grid(row=row+2, column=1)
            button_remove.grid(row=row+2, column=2)
        elif molecule[1] == Status.WARNING: # if the status is warning, add an abort button which will not add the document to the database
            button_override = tk.Button(identPopup, text="Abort", command=abort_upload(molecule, statuses))
            button_remove = tk.Button(identPopup, text="Remove", command=identPopup.destroy)
            button_override.grid(row=row+2, column=1)
            button_remove.grid(row=row+2, column=2)
        # elif molecule[1] == Status.SUCCESS: # if the status is success, no buttons are needed


        # Set the background color based on the status
        if molecule[1] == Status.CONFLICT:
            label.config(bg='red')
        elif molecule[1] == Status.WARNING:
            label.config(bg='yellow')
        elif molecule[1] == Status.SUCCESS:
            label.config(bg='light green')
        elif molecule[1] == Status.EXISTS:
            label.config(bg='light blue')


    # Make the identPopup window modal
    identPopup.grab_set()
    identPopup.geometry("800x600")
    identPopup.mainloop()

def choose_file():
    # Open a GUI window to browse for a file
    chooseRoot = tk.Tk()
    chooseRoot.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

    # If the user canceled the file selection, do nothing
    if not file_path:
        return

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Selected file is not a valid JSON file.")
            return
        
    upload_file(data)
    chooseRoot.destroy()
    print("Choose File finished")
    

def upload_file(data):

    # Check if db has a document with the same identifier
    # If it does, ask the user if they want to override it
    # If they do, update the document

    for molecule in data:
        # Check if the identifier already exists in the database
        doc_id = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
        existing_doc = collection.find_one({"identifier": doc_id})

        if existing_doc:
            # If the document exists, ask the user if they want to keep the original or override
            # if the document exists, check if any of the keys are the same, if even one is, there is a conflict
            if set(molecule.keys()).intersection(set(existing_doc.keys())):
                # If the keys are the same, check if the values are the same
                if molecule != existing_doc:
                    # If the values are the same, do nothing
                    statuses.insert(0, (molecule, Status.CONFLICT)) # push front
                    continue
                else:
                    statuses.append((molecule, Status.EXISTS))
            else:
                statuses.append((molecule, Status.WARNING))
        else:
            # If the document does not exist, insert it into the database
            molecule["identifier"] = doc_id
            collection.insert_one(molecule)
            statuses.append((molecule, Status.SUCCESS))

    # return statuses

if __name__ == "__main__":
    statuses = []
    
    # Create the main window
    root = tk.Tk()
    root.withdraw()

    # Define the actionPopup window
    actionPopup = tk.Toplevel(root)
    actionPopup.title("Choose an action")

    # Create the buttons
    upload_button = tk.Button(actionPopup, text="Upload", command=choose_file) # upload_file(choose_file())
    retrieve_button = tk.Button(actionPopup, text="Retrieve", command=on_retrieve)
    close_button = tk.Button(actionPopup, text="Close", command=root.destroy)

    # Add the buttons to the actionPopup window
    upload_button.pack(pady=5)
    retrieve_button.pack(pady=5)
    close_button.pack(pady=5)

    # Run the main window
    actionPopup.grab_set()
    actionPopup.geometry("800x600")
    actionPopup.mainloop()

    # instantiate statuses array, will be stored as array of pairs (molecule, status)
    # statuses = upload_file()

    # Show the identifiers in a pop-up window
    show_identifiers(statuses)