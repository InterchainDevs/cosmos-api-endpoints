#!/usr/bin/python
from flask import Flask, jsonify
from flask_cors import CORS
from requests import Session
from time import strftime, sleep
import json


def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(PATH + CSV_LOG_OUTPUT_FILE, "a")
    file_log.write (string_to_log)

app = Flask(__name__)
CORS(app, max_age=404200, resources=r'/api/*', expose_headers='Content-Type: application/json', vary_header=True, methods='GET', origins='*')

from config import HTML_DOC, PATH, HOST, PORT, CSV_LOG_OUTPUT_FILE, SUPPLY_TOTAL_ALL, RICHLIST_FILE, CHAIN_FILE, VESTING_FILE



#### Flask endpoints

@app.route("/api/rest/supply/apr")
def get_api_apr():
    # read the JSON's chain_metrics 
    with open(CHAIN_FILE, 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route("/api/rest/supply/circulating")
def get_api_circulating():
    # read the JSON's chain_metrics 
    with open(CHAIN_FILE, 'r') as file:
        data = json.load(file)
        circulating = float(data["total_supply"]) - float(data["total_bonded"]) - float(data["total_vested"])
        circulating_str = f"{circulating:.6f}"
    return circulating_str

@app.route("/api/rest/supply/total")
def get_api_total():
    # read the JSON's chain_metrics 
    with open(CHAIN_FILE, 'r') as file:
        data = json.load(file)
    return data["total_supply"]

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
    
    # Select the first 100 registries
    top_100 = sorted_data[:100]
    
    #return json.dumps(top_100, indent=4)
    return jsonify(top_100)

@app.route("/api/rest/supply/bonded")
def get_api_bonded():
    # read the JSON's chain_metrics 
    with open(CHAIN_FILE, 'r') as file:
        data = json.load(file)
    return data["total_bonded"]

@app.route("/api/rest/supply/not_bonded")
def get_api_bonded():
    # read the JSON's chain_metrics 
    with open(CHAIN_FILE, 'r') as file:
        data = json.load(file)
    return data["not_bonded"]

# TO-DO /api/rest/supply/vested
#
# show all active accounts vested with amount and end_date(both unix stamp & human) & total_count

@app.route("/api") 
def get_api_doc():
    # inject the html file as index/doc page
    with open(PATH + HTML_DOC) as f:
        return f.read()

####### End Flask endpoints

if __name__ == "__main__":
    # Init Flask server
    app.run(debug=True, host=HOST, port=PORT, use_reloader=False)