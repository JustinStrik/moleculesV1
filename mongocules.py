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
    Conflicts = 'conflicts'
    Warning = 'warning'
    Success = 'success'

# Connect to the database
db = cluster["moleculesTestV1"]
collection = db["molecules"]


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

    conflicts = []
    warnings = []
    safe = []

    # Check if db has a document with the same identifier
    # If it does, ask the user if they want to override it
    # If they do, update the document

    for molecule in data:
        # Check if the identifier already exists in the database
        doc_id = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
        existing_doc = collection.find_one({"identifier": doc_id})

        if existing_doc:
            # If the document exists, add it to the conflicts list
            conflicts.append((doc_id, molecule))
        elif collection.find_one({"name": molecule["name"], "basis_sets": molecule["basis_sets"], "functional": molecule["functional"]}):
            # If there is a molecule with the same name, basis_sets, and functional in the database, add it to the warnings list
            warnings.append((doc_id, molecule))
        else:
            # If the document does not exist, insert it into the database and add it to the safe list
            molecule["identifier"] = doc_id
            collection.insert_one(molecule)
            safe.append((doc_id, molecule))

    # Show the results in message boxes
    if conflicts:
        conflict_message = "\n".join([f"{molecule[0]} - {Status.Conflicts.value}" for molecule in conflicts])
        messagebox.showwarning("Conflicts", f"The following molecules already exist in the database:\n{conflict_message}")

    if warnings:
        warning_message = "\n".join([f"{molecule[0]} - {Status.Warning.value}" for molecule in warnings])
        messagebox.showwarning("Warnings", f"The following molecules have the same name, basis sets, and functional as molecules in the database:\n{warning_message}")

    if safe:
        safe_message = "\n".join([f"{molecule[0]} - {Status.Success.value}" for molecule in safe])
        messagebox.showinfo("Success", f"The following molecules have been added to the database:\n{safe_message}")


if __name__ == "__main__":
    upload_file()
