#!/usr/bin/python
from requests import Request, Session
from time import strftime, sleep
from datetime import datetime
import json

from config import SUPPLY_RICHLIST, SUPPLY_ACCOUNTS, CSV_LOG_OUTPUT_FILE, DENOM, RICHLIST_FILE, VESTING_FILE, TIME_TO_SLEEP, SUPPLY_BONDED, CHAIN_FILE, SUPPLY_TOTAL_DENOM, INFLATION



def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(CSV_LOG_OUTPUT_FILE, "a")
    file_log.write (string_to_log)

def get_richlist():
    print('Richlist\n========')
    json_list = []
    for address in addresses:
        url = SUPPLY_RICHLIST + address + '/by_denom?denom=' + DENOM
        parameters = {}
        headers = {
            'Accepts': 'application/json'
        }
        print(f'Procesing: {url}')
        try:
            session = Session()
            session.headers.update(headers)
            response2 = session.get(url, params=parameters)
        except:
            conn_error = 'An error occurred getting the Accounts data ' +  url
            print("\n"+conn_error)
            log_this(conn_error)
        else:
            info2 = json.loads(response2.text)
            amount = int(info2["balance"]["amount"]) / 1000000
            entry = {
            "address": address,
            "balance": amount
            }
            json_list.append(entry)
    # Convertir la lista a una cadena JSON
    json_data = json.dumps(json_list, indent=4)

    with open(RICHLIST_FILE, "w") as json_file:
        json_file.write(json_data)

# Gets all accounts (normal & vested excluding module's accounts)
def get_accounts(next_key):
    url =  SUPPLY_ACCOUNTS + '&pagination.key=' + next_key
    parameters = {}
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the Accounts data ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
    else:
        addresses = []
        info = json.loads(response.text)
        return info

def get_all_accounts():
    print('All accounts\n============')
    addresses = []
    vesting = []
    total_vesting = 0
    info = get_accounts('')
    pagination = info["pagination"]["next_key"]
    if pagination != None:
        # print(pagination)
        for reg in info["accounts"]:
            if reg["@type"] == "/cosmos.auth.v1beta1.BaseAccount":
                address = reg["address"]
                addresses.append(address)
                print(str(len(addresses)) + ' ' + address)
            if reg["@type"] == "/cosmos.vesting.v1beta1.DelayedVestingAccount":
                address = reg["base_vesting_account"]["base_account"]["address"]
                addresses.append(address)
                vesting.append(reg) # makes a JSON with vesting account info
                time_vesting = reg["base_vesting_account"]["end_time"]
                end_time = datetime.fromtimestamp(int(time_vesting))
                current_time = datetime.now()
                if end_time > current_time:
                    total_vesting = int(total_vesting) + int(reg["base_vesting_account"]["original_vesting"][0]["amount"])
                    msg = str(len(addresses)) + ' ' + address + ' Vesting active'
                    log_this(msg)
                    # log_this(str(total_vesting))
                else:
                    msg = str(len(addresses)) + ' ' + address + ' Vesting finished'
                    # log_this(msg)
        # print(pagination)
        sleep(3)
        while pagination != None:
            info = get_accounts(pagination)
            for reg in info["accounts"]:
                if reg["@type"] == "/cosmos.auth.v1beta1.BaseAccount":
                    address = reg["address"]
                    addresses.append(address)
                    print(str(len(addresses)) + ' ' + address)
                if reg["@type"] == "/cosmos.vesting.v1beta1.DelayedVestingAccount":
                    address = reg["base_vesting_account"]["base_account"]["address"]
                    addresses.append(address)
                    vesting.append(reg) # makes a JSON with vesting account info
                    time_vesting = reg["base_vesting_account"]["end_time"]
                    end_time = datetime.fromtimestamp(int(time_vesting))
                    current_time = datetime.now()
                    if end_time > current_time:
                        total_vesting = int(total_vesting) + int(reg["base_vesting_account"]["original_vesting"][0]["amount"])
                        msg = str(len(addresses)) + ' ' + address + ' Vesting active'
                        log_this(msg)
                        # log_this(str(total_vesting))
                    else:
                        msg = str(len(addresses)) + ' ' + address + ' Vesting finished'
                        # log_this(msg)
            # print(pagination)
            sleep(3)
            pagination = info["pagination"]["next_key"]
    else:
        for reg in info["accounts"]:
            if reg["@type"] == "/cosmos.auth.v1beta1.BaseAccount":
                address = reg["address"]
                addresses.append(address)
                print(str(len(addresses)) + ' ' + address)
            if reg["@type"] == "/cosmos.vesting.v1beta1.DelayedVestingAccount":
                address = reg["base_vesting_account"]["base_account"]["address"]
                addresses.append(address)
                vesting.append(reg) # makes a JSON with vesting account info
                time_vesting = reg["base_vesting_account"]["end_time"]
                end_time = datetime.fromtimestamp(int(time_vesting))
                current_time = datetime.now()
                if end_time > current_time:
                    total_vesting = int(total_vesting) + int(reg["base_vesting_account"]["original_vesting"][0]["amount"])
                    msg = str(len(addresses)) + ' ' + address + ' Vesting active'
                    log_this(msg)
                    # log_this(str(total_vesting))
                else:
                    msg = str(len(addresses)) + ' ' + address + ' Vesting finished'
                    # log_this(msg)
    return addresses, vesting, (total_vesting / 1000000)

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

def get_inflation():
    url = INFLATION
    parameters = {}
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the Inflation data ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
    else:
        info = json.loads(response.text)
        inflation = info["inflation"]
        return float(inflation)

if __name__ == "__main__":
    while True:
        total_vesting = 0
        chain_params = []
        # Process the vesting accounts
        try:
            addresses, vested, total_vesting = get_all_accounts()
            json_vesting_data = json.dumps(vested, indent=4)
        except:
            error = 'Account or vesting dump failed'
            print(error)
            log_this(error)
        else:
            with open(VESTING_FILE, "w") as vesting_json_file:
                vesting_json_file.write(json_vesting_data)
        # Process the other chain params
        try:
            bonded, not_bonded = get_bonded_not_bonded_data()
            total_supply = get_total_supply_data()
            inflation = get_inflation()
        except:
            conn_error = 'Error getting Params from chain'
            print("\n"+conn_error)
            log_this(conn_error)
        else:
            apr = ((float(total_supply) * inflation ) / float(bonded) ) * 100
            apr_str = f"{apr:.2f}"
            vested_str = f"{total_vesting:.6f}"
            inflation_srt = f"{inflation:.2f}"
            entry = {
            "total_supply": total_supply,
            "inflation": inflation_srt,
            "total_bonded": bonded,
            "apr": apr_str,
            "not_bonded": not_bonded,
            "total_vested": vested_str
            }
            # Convertir la lista a una cadena JSON
        json_data = json.dumps(entry, indent=4)
        with open(CHAIN_FILE, "w") as json_file:
            json_file.write(json_data)
        print('Chain data saved to JSON')
        # calculate the richlist
        get_richlist()
        sleep(TIME_TO_SLEEP)
