import unittest
from comparision import comparision
import pymongo
import csv

client = pymongo.MongoClient("mongodb+srv://ABC:42403287@comparison.ydtcv.mongodb.net/DB1?retryWrites=true&w=majority")
database_name = client['DB1']
collection_Name_1 = database_name['Stocks']
collection_Name_2 = database_name['Stocks2']
file1 = "sec_bhavdata_full.csv"
file2 = "sec_bhavdata_diff.csv"

source_comparision = comparision()

source = [{'Date_1': '22/03/2021', 'Comp_Column_1': 'Prev_Close'}, {'Date_2': '22/03/2021', 'Comp_Column_2': 'Prev_Close'}]

#class nullComparision(unittest.TestCase):


#manually calculating the results after comparision
#the results after this process will be compared with the results of the original functions during the testing process

def date_conversion(Date):
    month_dict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
    Date_str = Date.split("/")
    month = month_dict[int(Date_str[1])]
    Updated_Date = " " + Date_str[0] + "-" + month + "-" + Date_str[2]
    return Updated_Date

def find_difference(Data_1, Data_2,Col_1,Col_2):
    diff = round(abs(float(Data_1[Col_1]) - float(Data_2[Col_2])),2)
    percentage_diff = round(((float(Data_1[Col_1]) - float(Data_2[Col_2]))/float(Data_1[Col_1]))*100,2)
    dictionary = {'Symbol':Data_1['Symbol'], "Col_1":Data_1[Col_1], "Col_2":Data_2[Col_2],"Diff": diff, "percentage": percentage_diff}
    return dictionary

def mongo_mongo(): # for calculating mongo_mongo_answer

    source = [{'Date_1': '22/03/2021', 'Comp_Column_1': 'Prev_Close'}, {'Date_2': '22/03/2021', 'Comp_Column_2': 'Prev_Close'}]

    Col_1 = source[0]['Comp_Column_1']
    Col_2 = source[1]['Comp_Column_2']
    Date_1 = date_conversion(source[0]['Date_1'])
    Date_2 = date_conversion(source[1]['Date_2'])

    Data_1 = []
    for doc in collection_Name_1.find({"Date":Date_1},{"_id":0, Col_1:1, "Symbol": 1}).sort([("Symbol",1),("Series",1)]):
        Data_1.append(doc)
    Data_2 = []
    for doc in collection_Name_2.find({"Date": Date_2},{"_id":0,Col_2:1,"Symbol": 1}).sort([("Symbol",1),("Series",1)]):
        Data_2.append(doc)
    mongo_mongo_answer = []
    for i in range(len(Data_1)):
        if(Data_1[i] == Data_2[i]):
            continue
        else:
            dictionary = find_difference(Data_1[i],Data_2[i],Col_1,Col_2)
            mongo_mongo_answer.append(dictionary)
    return mongo_mongo_answer

def excel_mongo(): #for calculating excel_mongo_answer

    source = [{'Date_1': '22/03/2021', 'Comp_Column_1': 'Prev_Close'}, {'Date_2': '22/03/2021', 'Comp_Column_2': 'Prev_Close'}]

    Col_1 = source[0]['Comp_Column_1']
    Col_2 = source[1]['Comp_Column_2']
    Date_1 = date_conversion(source[0]['Date_1'])
    Date_2 = date_conversion(source[1]['Date_2'])

    Data_1 = []
    for doc in collection_Name_1.find({"Date":Date_1},{"_id":0, Col_1:1, "Symbol": 1}).sort([("Symbol",1),("Series",1)]):
        Data_1.append(doc)
    for dict in Data_1:
        dict[Col_1] = float(dict[Col_1])

    Data_2 = []

    with open(file1, "r") as f:
        reader = csv.DictReader(f)
        collection_Name_2 = list(reader)

    for dict in collection_Name_2:
        temp = {key: value for key, value in dict.items() if (key==Col_2 or key=='Symbol') and dict['Date']==Date_2}
        if(temp):
            Data_2.append(temp)
    for dict in Data_2:
        dict[Col_2] = float(dict[Col_2])

    excel_mongo_answer = []
    for i in range(len(Data_1)):
        if(Data_1[i] == Data_2[i]):
            continue
        else:
            dictionary = find_difference(Data_1[i],Data_2[i],Col_1,Col_2)
            excel_mongo_answer.append(dictionary)
    return excel_mongo_answer

def excel_excel(): #for calculating excel_excel_answer

    source = [{'Date_1': '22/03/2021', 'Comp_Column_1': 'Prev_Close'}, {'Date_2': '22/03/2021', 'Comp_Column_2': 'Prev_Close'}]

    Col_1 = source[0]['Comp_Column_1']
    Col_2 = source[1]['Comp_Column_2']
    Date_1 = date_conversion(source[0]['Date_1'])
    Date_2 = date_conversion(source[1]['Date_2'])

    Data_1 = []
    with open(file1, "r") as f:
        reader = csv.DictReader(f)
        collection_Name_1 = list(reader)

    for dict in collection_Name_1:
        temp = {key: value for key, value in dict.items() if (key==Col_1 or key=='Symbol') and dict['Date']==Date_1}
        if(temp):
            Data_1.append(temp)

    Data_2 = []
    with open(file2, "r") as f:
        reader = csv.DictReader(f)
        collection_Name_2 = list(reader)

    for dict in collection_Name_2:
        temp = {key: value for key, value in dict.items() if (key==Col_2 or key=='Symbol') and dict['Date']==Date_2}
        if(temp):
            Data_2.append(temp)


    excel_excel_answer = []
    for i in range(len(Data_1)):
        if(Data_1[i] == Data_2[i]):
            continue
        else:
            dictionary = find_difference(Data_1[i],Data_2[i],Col_1,Col_2)
            excel_excel_answer.append(dictionary)
    return excel_excel_answer


class testComparision(unittest.TestCase):

    def test_mongo_null_comparision(self):
        result = source_comparision.mongo_mongo_comparision(collection_Name_1, collection_Name_1, source)
        self.assertEqual([], result)

    def test_excel_null_comparision(self):
        result = source_comparision.excel_excel(file1, file1, source)
        self.assertEqual([], result)

    def test_mongo_mongo(self):
        result = source_comparision.mongo_mongo_comparision(collection_Name_1, collection_Name_2, source)
        mongo_mongo_answer = mongo_mongo()
        self.assertEqual(result, mongo_mongo_answer)

    def test_excel_mongo(self):
        result = source_comparision.excel_mongo(collection_Name_1, file1, source)
        excel_mongo_answer = excel_mongo()
        self.assertEqual(result, excel_mongo_answer)

    def test_excel_excel(self):
        result = source_comparision.excel_excel(file1, file2, source)
        excel_excel_answer = excel_excel()
        self.assertEqual(result, excel_excel_answer)