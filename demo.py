import pymongo
import dns
import pprint

client = pymongo.MongoClient("mongodb+srv://Saurabh_Ksagar:Saurabh%40123srk@cluster0.1aksc.mongodb.net/API?retryWrites=true&w=majority")

database_name = client['API']
collection_Name = database_name['book']
for b in collection_Name.find():
    print(b)