import tkinter as tk
from tkinter import filedialog
import json
from enum import Enum
import pymongo
from pymongo import MongoClient
from tkinter import messagebox

# Connect to the MongoDB, change the connection string per your MongoDB environment
cluster = MongoClient("mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority")

class Status(Enum):
    CONFLICT = 'conflict'
    WARNING = 'warning'
    SUCCESS = 'success'
    ABORTED = 'aborted'

# Connect to the database
db = cluster["moleculesTestV1"]
collection = db["molecules"]
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

def show_identifiers(statuses):
    # Create the popup window
    popup = tk.Toplevel()
    popup.title("Identifiers")

    # Add a label to the window
    label = tk.Label(popup, text="These are the identifiers in the file:")
    label.grid(row=0, column=0, columnspan=2)

    # Add a button to close the window
    button_close = tk.Button(popup, text="Close", command=popup.destroy)
    button_close.grid(row=len(statuses)+3, column=1, columnspan=2)

    # Display the identifiers in rows
    for row, molecule in enumerate(statuses):
        # Create a Label widget for each column in the row
        label = tk.Label(popup, text=molecule[0]["identifier"])
        labels.append(label) # add the label to the list of labels for ease of color changing
        label.grid(row=row+2, column=0)

        if molecule[1] == Status.CONFLICT: # if the status is conflict, add an override button which will remove the document from the database and add the new one
            button_override = tk.Button(popup, text="Override", command=push_to_db(molecule, statuses, row))
            button_remove = tk.Button(popup, text="Remove", command=popup.destroy)
        if molecule[1] == Status.WARNING: # if the status is warning, add an abort button which will not add the document to the database
            button_override = tk.Button(popup, text="Abort", command=abort_upload(molecule, statuses))
            button_remove = tk.Button(popup, text="Remove", command=popup.destroy)

        button_override.grid(row=row+2, column=1)
        button_remove.grid(row=row+2, column=2)

        # Set the background color based on the status
        if molecule[1] == Status.CONFLICT:
            label.config(bg='red')
        elif molecule[1] == Status.WARNING:
            label.config(bg='yellow')
        elif molecule[1] == Status.SUCCESS:
            label.config(bg='green')


    # Make the popup window modal
    popup.grab_set()
    popup.geometry("800x600")
    popup.mainloop()

def upload_file():
    # Open a GUI window to browse for a file
    root = tk.Tk()
    root.withdraw()
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

    # instantiate statuses array, will be stored as array of pairs (index, status)
    statuses = []

    # Check if db has a document with the same identifier
    # If it does, ask the user if they want to override it
    # If they do, update the document

    for molecule in data:
        # Check if the identifier already exists in the database
        doc_id = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
        existing_doc = collection.find_one({"identifier": doc_id})

        if existing_doc:
            # If the document exists, ask the user if they want to keep the original or override
            if set(molecule.keys()) == set(existing_doc.keys()):
                # If the keys are the same, check if the values are the same
                if molecule == existing_doc:
                    # If the values are the same, do nothing
                    statuses.insert(0, (molecule, Status.CONFLICT)) # push front
                    continue
            else:
                statuses.append((molecule, Status.WARNING))
        else:
            # If the document does not exist, insert it into the database
            molecule["identifier"] = doc_id
            collection.insert_one(molecule)
            statuses.append((molecule, Status.SUCCESS))

        
    # Show the identifiers in a pop-up window
    show_identifiers(statuses)

if __name__ == "__main__":
    upload_file()
