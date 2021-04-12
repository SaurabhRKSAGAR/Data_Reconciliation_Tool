from flask import Flask,make_response,request,jsonify,render_template,url_for,redirect,flash
from flask_mongoengine import MongoEngine
from config import DB_connection
import requests
from mongoengine import StringField
import pandas as pd
import json
import pymongo
import dns
import sys
from comparision import comparision



app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'    

source_comparision = comparision()

history = []

database_name = ""
collection_Name = ""
database_name_2 = ""
collection_Name_2 = ""
excel_path_1 = ""
excel_path_2 = ""
Source_1 = {}
Source_2 = {}

@app.route("/api", methods = ['GET','POST'])
def form_data_view():
    return render_template("form.html")

@app.route("/api/history", methods=['GET', 'POST'])
def history1():
    if request.method == 'GET':
        print(history)
        return render_template("history.html", hRows=history)

def save_data(Source_1, Source_2):
    tmp_dict = {'Source_1': Source_1, 'Source_2': Source_2} 
    if(tmp_dict not in history):
        history.append(tmp_dict)


@app.route("/api/config", methods = ['GET','POST'])
def config_form_data_view():
    return render_template("config_form.html")

@app.route("/api/config_form_data", methods=['POST'])
def process_config_form_data():
    info = {}
    error = "Invalid"
    global excel_path_1, excel_path_2, database_name, database_name_2, collection_Name, collection_Name_2
    excel_path_1 = ""
    excel_path_2 = ""
    database_name = ""
    database_name_2 = ""
    collection_Name = ""
    collection_Name_2 = ""

    info['Source_1'] = request.form['Source_1']
    Source_1['Source_1'] = info['Source_1']
    info['Source_2'] = request.form['Source_2']
    Source_2['Source_2'] = info['Source_2']
    source1_path = request.form['Path_1']
    source2_path = request.form['Path_2']
    print(str(info) + " " + source1_path + " " + source2_path)
    #if mongo db then check uri
    if info['Source_1'] == "MongoDB":
        #check this client for active connection
        try:
            client1 = pymongo.MongoClient(source1_path)
            print(client1.server_info())
            print("CONNECTED")
            uri1 = pymongo.uri_parser.parse_uri(source1_path)
            db_name = uri1['database']  
            database_name = client1[db_name]
            print(database_name)
            collect_1_Name = request.form['Collection_1']
            collection_Name = database_name[collect_1_Name]
            print(type(collection_Name))

        except:
            error = error + " :Source 1 MongoDB URI"
            e = sys.exc_info()[0]
            print(e)
            print("ERROR")
    else:
        try:
            my_file = open(source1_path)
            excel_path_1 = source1_path
        except IOError:
            # file does not exist
            error = error + " :Excel File for Source 1"

    if info['Source_2'] == "MongoDB":
        #check this client for active connection
        try:
            client2 = pymongo.MongoClient(source2_path)
            print(client2.server_info())
            print("CONNECTED")
            uri2 = pymongo.uri_parser.parse_uri(source2_path)
            db_name_2 = uri2['database']
            database_name_2 = client2[db_name_2]
            #collection_Name_2 = uri2['collection']
            collect_Name_2 = request.form['Collection_2']
            collection_Name_2 = database_name_2[collect_Name_2]
        except:
            error = error + " :Source 2 MongoDB URI"
            e = sys.exc_info()[0]
            print(e)
            print("ERROR")
    else:
        try:
            my_file = open(source2_path)
            excel_path_2 = source2_path
        except IOError:
            # file does not exist
            error = error + " :Excel File for Source 2"

    print("Excel: 1: " + str(excel_path_1) + " 2: " + str(excel_path_2))
    print("MongoDB: 1: " + str(database_name) + " " + str(collection_Name) + " 2: " + str(database_name_2) + " " + str(collection_Name_2))

    if error != "Invalid":
        return render_template('config_form.html',error=error)
    else:
        flash("Configuration Details Successfully Stored")  
        return redirect(url_for('form_data_view'))  

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
    Source_1['Date_1'] = request.form['Date_1']
    Source_1['Comp_Column_1'] = request.form['Comp_Column_1']
    Source_2['Date_2'] = request.form['Date_2']
    Source_2['Comp_Column_2'] = request.form['Comp_Column_2']
    print(Source_1)
    print(Source_2)
    #print("RECV DATA")
    print("------------------")
    print(history)
    save_data(Source_1.copy(), Source_2.copy())
    result_list = [Source_1,Source_2]
    json_arg = json.dumps(result_list)
    res = requests.post("http://localhost:5000/api/processed_data",json=json_arg)
    difference_data = res.json()
    json_res = json.loads(difference_data['difference_data'])
    #print(json_res)
    return render_template("index.html", Companies = json_res, Col_1 = Source_1['Comp_Column_1'], Col_2 = Source_2['Comp_Column_2'], Date_1=Source_1['Date_1'], Date_2 = Source_2['Date_2'])
    # return make_response("",200)

@app.route("/api/db_populate", methods = ['GET'])
def db_populate():
    data = pd.read_csv("INSERT_PATH_TO_EXCEL_FILE_HERE")
    payload = json.loads(data.to_json(orient='records'))
    collection_Name_2.insert_many(payload)
    print("Success")
    return make_response("",200)

@app.route("/api/processed_data", methods = ['GET','POST'])
def process_data():
    if request.method == 'POST':
        sources = json.loads(request.get_json())
        if(sources[0]['Source_1'] == "MongoDB" and sources[1]['Source_2'] == "MongoDB"):
            diff = source_comparision.mongo_mongo_comparision(collection_Name,collection_Name_2,sources)
            print(len(diff))
            json_diff = json.dumps(diff)
            return jsonify({'difference_data': json_diff})
        if(sources[0]['Source_1'] == "MongoDB" and sources[1]['Source_2'] == "Excel Sheet"):
            diff = source_comparision.excel_mongo(collection_Name,excel_path_2,sources)
            json_diff = json.dumps(diff)
            return jsonify({'difference_data': json_diff})

        if(sources[0]['Source_1'] == "Excel Sheet" and sources[1]['Source_2'] == "Excel Sheet"):
            diff = source_comparision.excel_excel(excel_path_1,excel_path_2,sources)
            json_diff = json.dumps(diff)
            return jsonify({'difference_data': json_diff})


if __name__ == "__main__":
    app.run()