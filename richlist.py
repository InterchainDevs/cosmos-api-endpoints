from requests import Request, Session
from time import strftime, sleep
import json

from config import SUPPLY_RICHLIST, SUPPLY_ACCOUNTS, PATH, CSV_LOG_OUTPUT_FILE, DENOM, RICHLIST_FILE, VESTING_FILE



def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(PATH + CSV_LOG_OUTPUT_FILE, "a")
    file_log.write (string_to_log)

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
    print('rich list\n=========')
    addresses = []
    vesting = []
    info = get_accounts('')
    pagination = info["pagination"]["next_key"]
    if pagination != None:
        print(pagination)
        for reg in info["accounts"]:
            if reg["@type"] == "/cosmos.auth.v1beta1.BaseAccount":
                address = reg["address"]
                addresses.append(address)
                print(address)
                print(str(len(addresses)))
            if reg["@type"] == "/cosmos.vesting.v1beta1.DelayedVestingAccount":
                address = reg["base_vesting_account"]["base_account"]["address"]
                addresses.append(address)
                print(address)
                print(str(len(addresses)))
                #reg_replace = reg.replace("'", "0")
                vesting.append(reg) # makes a JSON with vesting account info
        print(pagination)
        sleep(3)
        while pagination != None:
            info = get_accounts(pagination)
            for reg in info["accounts"]:
                if reg["@type"] == "/cosmos.auth.v1beta1.BaseAccount":
                    address = reg["address"]
                    addresses.append(address)
                    print(address)
                    print(str(len(addresses)))
                if reg["@type"] == "/cosmos.vesting.v1beta1.DelayedVestingAccount":
                    address = reg["base_vesting_account"]["base_account"]["address"]
                    addresses.append(address)
                    print(address)
                    print(str(len(addresses)))
                    #reg_replace = reg.replace("'", "0")
                    vesting.append(reg) # makes a JSON with vesting account info
            print(pagination)
            sleep(3)
            pagination = info["pagination"]["next_key"]
    else:
        for reg in info["accounts"]:
            if reg["@type"] == "/cosmos.auth.v1beta1.BaseAccount":
                address = reg["address"]
                addresses.append(address)
                print(address)
                print(str(len(addresses)))
            if reg["@type"] == "/cosmos.vesting.v1beta1.DelayedVestingAccount":
                address = reg["base_vesting_account"]["base_account"]["address"]
                addresses.append(address)
                print(address)
                print(str(len(addresses)))
                vesting.append(reg) # makes a JSON with vesting account info
    return addresses, vesting

addresses, vested = get_all_accounts()

# Process the vesting accounts
print(vested)
json_vesting_data = json.dumps(vested, indent=4)
with open(VESTING_FILE, "w") as vesting_json_file:
    vesting_json_file.write(json_vesting_data)

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
         # entry = {
        # "address": address,
        # "balance": {
        #     "amount": int(amount),
        #     "denom": DENOM
        #     }
        # }
        json_list.append(entry)
# Convertir la lista a una cadena JSON
json_data = json.dumps(json_list, indent=4)

with open(RICHLIST_FILE, "w") as json_file:
    json_file.write(json_data)


    # {
    #   "@type": "/cosmos.vesting.v1beta1.DelayedVestingAccount",
    #   "base_vesting_account": {
    #     "base_account": {
    #       "address": "bcna17s8qdu02hwep7lafla4kwkdlnqw3m29zdug0ag",
    #       "pub_key": {
    #         "@type": "/cosmos.crypto.secp256k1.PubKey",
    #         "key": "Ah6vl/8Ebq0dycm0Zy4Ob6nNoX8aRiSiJ5DvO4GJVMmR"
    #       },
    #       "account_number": "555",
    #       "sequence": "1"
    #     },
    #     "original_vesting": [
    #       {
    #         "denom": "ubcna",
    #         "amount": "33519123320000"
    #       }
    #     ],
    #     "delegated_free": [],
    #     "delegated_vesting": [],
    #     "end_time": "1666962000"
    #   }
    # },
    # {
    #   "@type": "/cosmos.auth.v1beta1.BaseAccount",
    #   "address": "bcna17sgwwu39jhgg7nd5ws0498gmgqqevfxju6gw6d",
    #   "pub_key": {
    #     "@type": "/cosmos.crypto.secp256k1.PubKey",
    #     "key": "Au0kk/6P8UabvbQbcqMcDnwlToyfSSJESJjED4kCLxs+"
    #   },
    #   "account_number": "1689",
    #   "sequence": "5"
    # },