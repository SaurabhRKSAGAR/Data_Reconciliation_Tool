import pandas as pd
class comparision:

    def mongo_mongo_comparision(self,collection_Name_1,collection_Name_2):
        Data_1 = []
        for doc in collection_Name_1.find({},{"_id":0,"Series":0}).sort("Symbol",1):
            Data_1.append(doc)
        Data_2 = []
        for doc in collection_Name_2.find({},{"_id":0,"Series":0}).sort("Symbol",1):
            Data_2.append(doc)
        final_result = []

        for i in range(len(Data_1)):
            if(Data_1[i] == Data_2[i]):
                continue
            else:
                final_result.append(Data_1[i])
                final_result.append(Data_2[i])
        return final_result[:10]

    def excel_mongo(self,collection_Name):
        data1 = pd.read_csv("sec_bhavdata_diff.csv").values.tolist()
        data2 = []
        col = collection_Name.find()
        for i in col:
            temp = [v for k,v in i.items()]
            temp = temp[1:]
            data2.append(temp)
        data3 = []

        for i in range(len(data1)):
            if(data1[i]!=data2[i]):
                data3.append(data1[i])
                data3.append(data2[i])    
        #print(data3)
        return data3






        

