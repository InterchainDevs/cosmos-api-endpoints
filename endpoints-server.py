from flask import Flask, jsonify
from flask_cors import CORS
from requests import Request, Session
from time import strftime #, sleep
import json


def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(PATH + CSV_LOG_OUTPUT_FILE, "a")
    file_log.write (string_to_log)

app = Flask(__name__)
CORS(app, max_age=404200, resources=r'/api/*', expose_headers='Content-Type: application/json', vary_header=True, methods='GET', origins='*')

from config import HTML_DOC, PATH, HOST, PORT, CSV_LOG_OUTPUT_FILE, SUPPLY_BONDED

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
    return data  #return jsonify({currency: value})

@app.route("/api/rest/supply/total_all")
def get_api_total_all():
    data = 'test'
    return data  #return jsonify({currency: value})

@app.route("/api/rest/supply/richlist")
def get_api_total_richlist():
    data = 'test'
    return data  #return jsonify({currency: value})

@app.route("/api/rest/supply/bonded")
def get_api_bonded():
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
        return str(int(bonded_tokens) / 1000000)
        #return jsonify({'value': response})


@app.route("/api") 
def get_api_doc():
    # inject the hmtl file as index/doc page
    f = open(PATH + HTML_DOC)
    return f

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)


#return jsonify({"error": "Currency not found"}), 404
#return jsonify({currency: value})