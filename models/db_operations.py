from pymongo import MongoClient

connection_string = f"mongodb+srv://dwalkman:dwalkman@cluster0.ctofdja.mongodb.net/"

# listing database
client = MongoClient(connection_string)
db = client["test"]


def get_all_listings():
    return db.get_collection("Listing")

coll = get_all_listings()

def get_listing_by_title(value, coll=coll):
    return coll.find({"Title": {value}})



