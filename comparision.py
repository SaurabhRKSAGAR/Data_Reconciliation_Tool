import pandas as pd
import csv
class comparision:

    def date_conversion(self,Date):
        month_dict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        Date_str = Date.split("/")
        month = month_dict[int(Date_str[1])]
        Updated_Date = " " + Date_str[0] + "-" + month + "-" + Date_str[2]
        return Updated_Date

    def find_difference(self, Data_1, Data_2,Col_1,Col_2):
        diff = round(abs(float(Data_1[Col_1]) - float(Data_2[Col_2])),2)
        percentage_diff = round(((float(Data_1[Col_1]) - float(Data_2[Col_2]))/float(Data_1[Col_1]))*100,2)
        dictionary = {'Symbol':Data_1['Symbol'], "Col_1":Data_1[Col_1], "Col_2":Data_2[Col_2],"Diff": diff, "percentage": percentage_diff}
        return dictionary


    def mongo_mongo_comparision(self,collection_Name_1,collection_Name_2,sources):
        Col_1 = sources[0]['Comp_Column_1']
        Col_2 = sources[1]['Comp_Column_2']
        Date_1 = self.date_conversion(sources[0]['Date_1'])
        Date_2 = self.date_conversion(sources[1]['Date_2'])
        Data_1 = []
        for doc in collection_Name_1.find({"Date":Date_1},{"_id":0, Col_1:1, "Symbol": 1}).sort([("Symbol",1),("Series",1)]):
            Data_1.append(doc)
        Data_2 = []
        for doc in collection_Name_2.find({"Date": Date_2},{"_id":0,Col_2:1,"Symbol": 1}).sort([("Symbol",1),("Series",1)]):
            Data_2.append(doc)
        final_result = []
        for i in range(len(Data_1)):
            if(Data_1[i] == Data_2[i]):
                continue
            else:
                dictionary = self.find_difference(Data_1[i],Data_2[i],Col_1,Col_2)
                final_result.append(dictionary)
        return final_result

    def excel_mongo(self, collection_Name_1, file_name_1,sources):
        Col_1 = sources[0]['Comp_Column_1']
        Col_2 = sources[1]['Comp_Column_2']
        Date_1 = self.date_conversion(sources[0]['Date_1'])
        Date_2 = self.date_conversion(sources[1]['Date_2'])

        Data_1 = []
        for doc in collection_Name_1.find({"Date":Date_1},{"_id":0, Col_1:1, "Symbol": 1}).sort([("Symbol",1),("Series",1)]):
            Data_1.append(doc)
        for dict in Data_1:
            dict[Col_1] = float(dict[Col_1])

        Data_2 = []

        with open(file_name_1, "r") as f:
            reader = csv.DictReader(f)
            collection_Name_2 = list(reader)

        for dict in collection_Name_2:
            temp = {key: value for key, value in dict.items() if (key==Col_2 or key=='Symbol') and dict['Date']==Date_2}
            if(temp):
                Data_2.append(temp)
        for dict in Data_2:
            dict[Col_2] = float(dict[Col_2])

        final_result = []
        for i in range(len(Data_1)):
            if(Data_1[i] == Data_2[i]):
                continue
            else:
                dictionary = self.find_difference(Data_1[i],Data_2[i],Col_1,Col_2)
                final_result.append(dictionary)
        return final_result

    def excel_excel(self,file_name_1,file_name_2,sources):
        Col_1 = sources[0]['Comp_Column_1']
        Col_2 = sources[1]['Comp_Column_2']
        Date_1 = self.date_conversion(sources[0]['Date_1'])
        Date_2 = self.date_conversion(sources[1]['Date_2'])


        Data_1 = []
        with open(file_name_1, "r") as f:
            reader = csv.DictReader(f)
            collection_Name_1 = list(reader)

        for dict in collection_Name_1:
            temp = {key: value for key, value in dict.items() if (key==Col_1 or key=='Symbol') and dict['Date']==Date_1}
            if(temp):
                Data_1.append(temp)

        Data_2 = []
        with open(file_name_2, "r") as f:
            reader = csv.DictReader(f)
            collection_Name_2 = list(reader)

        for dict in collection_Name_2:
            temp = {key: value for key, value in dict.items() if (key==Col_2 or key=='Symbol') and dict['Date']==Date_2}
            if(temp):
                Data_2.append(temp)


        final_result = []
        for i in range(len(Data_1)):
            if(Data_1[i] == Data_2[i]):
                continue
            else:
                dictionary = self.find_difference(Data_1[i],Data_2[i],Col_1,Col_2)
                final_result.append(dictionary)
        return final_result





        

