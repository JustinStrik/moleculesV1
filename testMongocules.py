from mongocules import *

# Connect to the database
cluster = MongoClient("mongodb+srv://jstrik:strik@moleculev1.w7biaat.mongodb.net/?retryWrites=true&w=majority")
db = cluster["moleculesTesting1"]
collection = db["molecules"]

def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

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

    for status in statuses:
        print(status)
    
    # check if the statuses are correct
    assert statuses[0][1] == Status.SUCCESS, "Was: " + statuses[0][1] + ". 1 should be SUCCESS because the basis set is the different" 
    assert statuses[1][1] == Status.WARNING, "Was: " + statuses[1][1] + ". 2 should be WARNING because the basis set is the same but the functional is different"
    assert statuses[2][1] == Status.EXISTS, "Was: " + statuses[2][1] + ". 3 should be EXISTS because the identifier and properties are the same"
    assert statuses[3][1] == Status.CONFLICT, "Was: " + statuses[3][1] + ". 4 should be CONFLICT because the identifier is the same but the properties are different"


def test_sum_tuple():
    assert sum((1, 2, 2)) == 6, "Should be 6"

if __name__ == "__main__":
    
    test_sum()
    test_upload()
    print("Everything passed")