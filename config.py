import urllib.parse

class DB_connection:

    def __init__(self):
        self.user_name = urllib.parse.quote_plus('UserName_for_your_mongo')
        self.password = urllib.parse.quote_plus('Password_for_your_mongo')
        self.database_name = "Your_Database_name"
        self.collection_Name = "Your_Collection_name"