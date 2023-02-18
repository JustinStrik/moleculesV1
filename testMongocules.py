from mongocules import *

# Connect to the database
db = cluster["moleculesTesting1"]
collection = db["molecules"]

def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

# test if upload works
def test_upload():
    # clear database first
    # print whether the delete was acknowledged
    assert collection.delete_many({}).acknowledged, "Delete was not acknowledged"
    print(upload_file("testData1.json"))

def test_sum_tuple():
    assert sum((1, 2, 2)) == 6, "Should be 6"

if __name__ == "__main__":
    
    test_sum()
    test_upload()
    print("Everything passed")