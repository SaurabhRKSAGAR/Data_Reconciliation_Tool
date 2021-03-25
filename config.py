import urllib.parse

class DB_connection:

    def __init__(self):
        self.user_name = urllib.parse.quote_plus('Saurabh_Ksagar')
        self.password = urllib.parse.quote_plus('Saurabh@123srk')
        self.database_name = "Stock_Data"
        self.collection_Name = "Companies"