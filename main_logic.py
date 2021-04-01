from flask import Flask,make_response,request,jsonify,render_template,url_for,redirect
from flask_mongoengine import MongoEngine
from config import DB_connection
import requests
from mongoengine import StringField
import pandas as pd
import json
import pymongo
import dns
from comparision import comparision



app = Flask(__name__)

conn = DB_connection()
DB_URI = "mongodb+srv://{}:{}@cluster0.1aksc.mongodb.net/{}?retryWrites=true&w=majority".format(conn.user_name,conn.password,conn.database_name)

client = pymongo.MongoClient(DB_URI)

database_name = client[conn.database_name]
collection_Name = database_name[conn.collection_Name]
collection_Name_2 = database_name[conn.collection_Name_2]
source_comparision = comparision()
history = database_name['History']

@app.route("/api", methods = ['GET','POST'])
def form_data_view():
    return render_template("form.html")

@app.route("/api/history", methods=['GET', 'POST'])
def history1():
    if request.method == 'GET':
        hData = []
        for doc in history.find():
            hData.append(doc)
        return render_template("history.html", hRows=hData)

def save_data(Source_1, Source_2):
    # print(Source_1)
    # print(Source_2)
    history.insert_one({'Source_1': Source_1, 'Source_2': Source_2})

@app.route("/api/config", methods = ['GET','POST'])
def config_form_data_view():
    return render_template("config_form.html")

@app.route("/api/connection_details",methods = ['POST'])
def conn_details():
    conn_1 = {}
    conn_1['UserName'] = request.form['UserName']
    conn_1['Password'] = request.form['Password']
    conn_1['DBName'] = request.form['DBName']
    conn_1['CollectionName'] = request.form['CollectionName']
    print(conn_1)
    return redirect(url_for('form_data_view'))

@app.route("/api/form_data", methods = ['POST'])
def process_form_data():
    Source_1 = {}
    Source_1['Source_1'] = request.form['Source_1']
    Source_1['Company_1'] = request.form['Company_1']
    Source_1['Date_1'] = request.form['Date_1']
    Source_1['Comp_Column_1'] = request.form['Comp_Column_1']
    Source_2 = {}
    Source_2['Source_2'] = request.form['Source_2']
    Source_2['Company_2'] = request.form['Company_2']
    Source_2['Date_2'] = request.form['Date_2']
    Source_2['Comp_Column_2'] = request.form['Comp_Column_2']
    print(Source_1)
    print(Source_2)
    print("RECV DATA")
    save_data(Source_1, Source_2)
    result_list = [Source_1,Source_2]
    json_arg = json.dumps(result_list)
    res = requests.post("http://localhost:5000/api/processed_data",json=json_arg)
    difference_data = res.json()
    json_res = json.loads(difference_data['difference_data'])
    #print(json_res)
    return render_template("index.html", Companies = json_res)
    # return make_response("",200)

@app.route("/api/db_populate", methods = ['GET'])
def db_populate():
    data = pd.read_csv("sec_bhavdata_full_Copy.csv")
    payload = json.loads(data.to_json(orient='records'))
    collection_Name_2.insert_many(payload)
    print("Success")
    return make_response("",200)

@app.route("/api/processed_data", methods = ['GET','POST'])
def process_data():
    if request.method == 'POST':
        sources = json.loads(request.get_json())
        if(sources[0]['Source_1'] == "MongoDB" and sources[1]['Source_2'] == "MongoDB"):
            diff = source_comparision.mongo_mongo_comparision(collection_Name,collection_Name_2)
            print(len(diff))
            json_diff = json.dumps(diff)
            return jsonify({'difference_data': json_diff})
        #return render_template("index.html", Companies = diff[:10])
        #return make_response("",200)
        if(sources[0]['Source_1'] == "MongoDB" and sources[1]['Source_2'] == "Excel Sheet"):
            diff = source_comparision.excel_mongo(collection_Name)
            json_diff = json.dumps(diff)
            return jsonify({'difference_data': json_diff})

if __name__ == "__main__":
    app.run()