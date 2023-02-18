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

def show_identifiers(data):
    # Create the popup window
    popup = tk.Toplevel()
    popup.title("Identifiers")

    # Add a label to the window
    label = tk.Label(popup, text="These are the identifiers in the file:")
    label.grid(row=0, column=0, columnspan=2)

    # Add a button to close the window
    button_close = tk.Button(popup, text="Close", command=popup.destroy)
    button_close.grid(row=len(data)+3, column=1, columnspan=2)


    # Display the identifiers in rows
    for index, molecule in enumerate(data):
        identifier = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
        label = tk.Label(popup, text=identifier)
        label.grid(row=index+2, column=0)
        button_override = tk.Button(popup, text="Override", command=popup.destroy)
        button_remove = tk.Button(popup, text="Remove", command=popup.destroy)
        button_override.grid(row=index+2, column=1)
        button_remove.grid(row=index+2, column=2)


    # Make the popup window modal
    popup.grab_set()
    popup.geometry("800x600")
    popup.mainloop()


def toggle_color(row_frame):
    bg_color = row_frame.cget("bg")
    if bg_color == "red":
        row_frame.configure(bg="green")
        row_frame.winfo_children()[0].configure(bg="green", fg="white")
        row_frame.winfo_children()[1].configure(bg="green")
    else:
        row_frame.configure(bg="red")
        row_frame.winfo_children()[0].configure(bg="red", fg="white")
        row_frame.winfo_children()[1].configure(bg="red")


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

    # Show the identifiers in a pop-up window
    show_identifiers(data)

    # Check if db has a document with the same identifier
    # If it does, ask the user if they want to override it
    # If they do, update the document

    for molecule in data:
        # Check if the identifier already exists in the database
        doc_id = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
        existing_doc = collection.find_one({"identifier": doc_id})

        if existing_doc:
            # If the document exists, ask the user if they want to keep the original or override
            confirm_override = messagebox.askyesno("Document already exists", f"A document with identifier {doc_id} already exists in the database. Do you want to override it?")

            if confirm_override:
                # If the user confirmed the override, update the existing document with the new information
                collection.update_one({"_id": existing_doc["_id"]}, {"$set": molecule})
                messagebox.showinfo("Success", f"The document with identifier {doc_id} has been updated.")
            else:
                # If the user did not confirm the override, do nothing
                return

        else:
            print(doc_id)
            # If the document does not exist, insert it into the database
            molecule["identifier"] = doc_id
            collection.insert_one(molecule)
            messagebox.showinfo("Success", f"The document with identifier {doc_id} has been added to the database.")

if __name__ == "__main__":
    upload_file()
