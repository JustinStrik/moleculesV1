import tkinter as tk
from tkinter import filedialog
import json
import pymongo
from pymongo import MongoClient
from tkinter import messagebox

# Connect to the MongoDB, change the connection string per your MongoDB environment
cluster = MongoClient("mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority")

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

    print(data[0]["name"])

    # Check if the identifier already exists in the database
    doc_id = f'{data[0]["name"]}_{data[0]["basis_sets"]}_{data[0]["functional"]}'
    existing_doc = collection.find_one({"identifier": doc_id})

    if existing_doc:
        # If the document exists, ask the user if they want to keep the original or override
        confirm_override = messagebox.askyesno("Document already exists", f"A document with identifier {doc_id} already exists in the database. Do you want to override it?")

        if confirm_override:
            # If the user confirmed the override, update the existing document with the new information
            collection.update_one({"_id": existing_doc["_id"]}, {"$set": data})
            messagebox.showinfo("Success", f"The document with identifier {doc_id} has been updated.")
        else:
            # If the user did not confirm the override, do nothing
            return

    else:
        print(doc_id)
        # If the document does not exist, insert it into the database
        data["identifier"] = doc_id
        collection.insert_one(data)
        messagebox.showinfo("Success", f"The document with identifier {doc_id} has been added to the database.")


if __name__ == "__main__":
    upload_file()
