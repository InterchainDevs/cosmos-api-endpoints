from flask import Flask, jsonify
from flask_cors import CORS
from requests import Request, Session
from time import strftime, sleep
import threading
import json

#from richlist import rich

def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(PATH + CSV_LOG_OUTPUT_FILE, "a")
    file_log.write (string_to_log)

app = Flask(__name__)
CORS(app, max_age=404200, resources=r'/api/*', expose_headers='Content-Type: application/json', vary_header=True, methods='GET', origins='*')

from config import HTML_DOC, PATH, HOST, PORT, CSV_LOG_OUTPUT_FILE, SUPPLY_BONDED, SUPPLY_TOTAL_DENOM, SUPPLY_TOTAL_ALL, RICHLIST_FILE



#### Flask endpoints

@app.route("/api/rest/supply/apr")
def get_api_apr():
    data = 'test'
    return data  #return jsonify({currency: value})

@app.route("/api/rest/supply/circulating")
def get_api_circulating():
    data = 'test'
    return data  #return jsonify({currency: value})

@app.route("/api/rest/supply/total")
def get_api_total():
    data = 'test'
    return data

@app.route("/api/rest/supply/total_all")
def get_api_total_all():
    url = SUPPLY_TOTAL_ALL
    parameters = {}
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the TOTAL SUPPLY data ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
    else:
        info = json.loads(response.text)
        # TO-DO: check if pagination.next_key <> null to iterate in results
        return jsonify(info)

@app.route("/api/rest/supply/richlist")
def get_api_total_richlist():
    # read the JSON's richlist 
    with open(RICHLIST_FILE, 'r') as file:
        data = json.load(file)
    
    # Order data by key "balance"
    sorted_data = sorted(data, key=lambda x: x['balance'], reverse=True)
    
    # Seleccionar los 100 primeros registros
    top_100 = sorted_data[:100]
    
    #return json.dumps(top_100, indent=4)
    return jsonify(top_100)

@app.route("/api/rest/supply/bonded")
def get_api_bonded():
    data = 'test'
    return data
        #return jsonify({'value': response})


@app.route("/api") 
def get_api_doc():
    # inject the html file as index/doc page
    with open(PATH + HTML_DOC) as f:
        return f.read()

####### End Flask endpoints

#### Functions: Data for calculations 

def get_total_vested():
    return "test"

def get_richlist():
    return "test"

def get_bonded_not_bonded_data():
    url = SUPPLY_BONDED
    parameters = {} # API parameters { 'ids': 'bitcanna', 'vs_currencies': 'usd' }
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the BONDING data ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
    else:
        info = json.loads(response.text)
        bonded_tokens = info["pool"]["bonded_tokens"]
        not_bonded_tokens = info["pool"]["not_bonded_tokens"]
        return str(int(bonded_tokens) / 1000000), str(int(not_bonded_tokens) / 1000000)

def get_total_supply_data():
    url = SUPPLY_TOTAL_DENOM
    parameters = {}
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the Total Supply data ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
    else:
        info = json.loads(response.text)
        total_denom = info["amount"]["amount"]
        return str(int(total_denom) / 1000000)




def get_calculated_data():
    while True:
        # get richlist and save in richlist.json
        print("test")
        total_supply = get_total_supply_data()
        print(total_supply)
        bonded, not_bonded = get_bonded_not_bonded_data()
        print(bonded, not_bonded)
        #rich()
        # get NOT EXPIRED vested accounts info and save in vested.json
        # total - non-bonded -vested = circulating.json
        sleep(30)

if __name__ == "__main__":
    # Iniciar la ejecución en segundo plano.
    t = threading.Thread(target=get_calculated_data)
    t.start()
    # Init Flask server
    app.run(debug=True, host=HOST, port=PORT, use_reloader=False)


#return jsonify({"error": "Currency not found"}), 404
#return jsonify({currency: value})