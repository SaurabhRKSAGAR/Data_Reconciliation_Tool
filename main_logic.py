from flask import Flask,make_response,request,jsonify,render_template,url_for,redirect
from flask_mongoengine import MongoEngine
from config import DB_connection
import requests
from mongoengine import StringField
import pandas as pd
import json
import pymongo
import dns


app = Flask(__name__)

conn = DB_connection()
DB_URI = "mongodb+srv://{}:{}@cluster0.1aksc.mongodb.net/{}?retryWrites=true&w=majority".format(conn.user_name,conn.password,conn.database_name)
# app.config["MONGODB_HOST"] = DB_URI
# print(DB_URI)

# db = MongoEngine()
# db.init_app(app)
client = pymongo.MongoClient(DB_URI)

database_name = client[conn.database_name]
collection_Name = database_name[conn.collection_Name]

@app.route("/api", methods = ['GET','POST'])
def form_data_view():
    return render_template("form.html")

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
    return redirect(url_for('process_data'))

@app.route("/api/db_populate", methods = ['GET'])
def db_populate():
    data = pd.read_csv("sec_bhavdata_full.csv")
    payload = json.loads(data.to_json(orient='records'))
    collection_Name.insert_many(payload)
    print("Success")
    return make_response("",200)

@app.route("/api/processed_data", methods = ['GET','POST'])
def process_data():
    if request.method == 'GET':
        Data = []
        for doc in collection_Name.find():
            Data.append(doc)
        return render_template("index.html", Companies = Data[:10])

if __name__ == "__main__":
    app.run()