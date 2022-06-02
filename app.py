from asyncio.log import logger
# from crypt import methods
from unittest import result
from flask import Flask, request, url_for, render_template
import pickle
import numpy as np
import json
from db.conn import database
from db.dbmodels import HouseData, SignIn

app = Flask(__name__)

app.config.update(
    dict(SECRET_KEY="powerful secretkey", WTF_CSRF_SECRET_KEY="a csrf secret key")
)

__locations = None
__data_columns = None
model = pickle.load(open("bangalore_home_prices_model.pickle","rb"))

def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(244)
    x[0] = input_json['sqft']
    x[1] = input_json['bath']
    x[2] = input_json['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    x = round(model.predict([x])[0],2)
    if x<50:
        result = x-10
    elif 50<x<100:
        result = x-20
    elif x>100:
        result = x-30
    return result

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading the saved artifacts...start !")
    global __data_columns
    global __locations
    global model

    with open("columns.json") as f:
        __data_columns = json.loads(f.read())["data_columns"]
        __locations = __data_columns[3:]

@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/users")
# def signin(req_json: SignIn):
#     try:
#         result = database().sign_log(req_json)
#         return result
#     except Exception as e:
#         logger.error("Exception in signing or logging in {e}")
#         return "Error"



@app.route("/prediction", methods=["POST"])
def prediction():
    
    if request.method == 'POST':
        input_json = {
            "location": request.form['sLocation'],
            "sqft": request.form['Squareft'],
            "bhk": request.form['uiBHK'],
            "bath": request.form['uiBathrooms']
        }
        result = get_estimated_price(input_json)

        if result > 100:
            result = round(result/100, 2)
            result = str(result) + ' Crore'
        else:
            result = str(result) + ' Lakhs'

    return render_template('prediction.html', result=result)

@app.route("/add", methods=['GET','POST'])
def insert_data():
    if request.method == 'POST':
        input_json = {
            "name": request.form['iName'],
            "phone": request.form['iNum'],
            "area": request.form['iSqft'],
            "bhk": request.form['iBHK'],
            "bath": request.form['iBathrooms'],
            "location": request.form['sLocation'],
            "price": request.form['Price']
        }
        result = database().insert_house_data(input_json)
        return render_template('data.html', result = result)

@app.route("/houses", methods=['GET', 'POST'])
def display_house_data():
    if request.method == 'POST':
        input_json = {
            "location": request.form['nLocation']
        }
    final_data = database().fetch_house_data(input_json)
    return render_template('houses.html', result = final_data)
    
@app.route("/remove", methods=['GET', 'POST'])
def remove_house_data():
    if request.method == 'POST':
        input_json = {
            "number": request.form['iNumber']
        }
    result = database().archive_house_data(input_json)
    return render_template('data.html', result=result)

if __name__ == "__main__":
    print("Starting Python Flask Server")
    load_saved_artifacts()
    app.run(debug=True)



