
from pymongo import MongoClient as mdb
# from pymongo.server_api import ServerApi



uri = "mongodb://appuser:appuser123@prmnlmdp1si11.amer.dell.com:27100/udid_us_st1"

#uri = "mongodb://appuser:@ppUser@12#@prmnlmdp1de11.amer.dell.com:27100/udid_us_dv"

myclient = mdb(uri)


try:
    myclient.admin.command('ping')
    db = myclient["udid_us_st1"]
    print(db.list_collection_names()[:5])
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print(myclient.list_database_names())

    collection = db["students100"]
    print("Collection 'students' created successfully")
    print(collection.find_one())

    doc = {"name": "John", "age": 30, "city": "New York"}
    collection.insert_one(doc)


    # Read operation
    for doc in collection.find():
        print(doc)

    print(collection.find_one())


except Exception as e:
    print(e)