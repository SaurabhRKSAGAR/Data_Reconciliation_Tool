import urllib.parse

class DB_connection:

    def __init__(self):
        self.user_name = urllib.parse.quote_plus('Your_Mongo_Username')
        self.password = urllib.parse.quote_plus('Your_Mongo_Password')
        self.database_name = "Mongo_Database_Name"
        self.collection_Name = "Mongo_Collection_Name"