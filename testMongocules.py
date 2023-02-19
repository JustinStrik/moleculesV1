from mongocules import *

# Connect to the database
cluster = MongoClient("mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority")
db = cluster["moleculesTesting1"]
collection = db["molecules"]

def test_sum():
    assert sum([1, 2, 3]) == 6, "Expected: 6"

# test if upload works
def test_upload():
    # clear database first
    # print whether the delete was acknowledged

    assert deleteEverything().acknowledged, "Delete was not acknowledged"

    with open("testData2.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Selected file is not a valid JSON file.")
            return

    statuses = upload_file(data)
    show_identifiers(statuses)

    for status in statuses:
        print(status)
    
    # check if the statuses are correct
    assert statuses[0][1] == Status.SUCCESS, "Case 1 was: {}. Expected: SUCCESS because the basis set is the different".format(statuses[0][1])
    assert statuses[1][1] == Status.WARNING, "Case 2: {}. Expected: WARNING because the basis set is the same but the functional is different".format(statuses[1][1])
    assert statuses[2][1] == Status.EXISTS, "Case 3: {}. Expected: EXISTS because the identifier and properties are the same".format(statuses[2][1])
    assert statuses[3][1] == Status.CONFLICT, "Case 4: {}. Expected: CONFLICT because the identifier is the same but the properties are different".format(statuses[3][1])


def test_sum_tuple():
    assert sum((1, 2, 2)) == 6, "Expected: 6"

if __name__ == "__main__":
    
    test_sum()
    test_upload()
    print("Everything passed")