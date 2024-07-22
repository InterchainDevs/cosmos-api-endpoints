# -*- coding: utf-8 -*-

# Server config
PATH = './' # Production: '/var/www/endpoints/'
CSV_LOG_OUTPUT_FILE = 'log.csv'
RICHLIST_FILE = 'richlist.json'
VESTING_FILE = 'vesting.json'
HTML_DOC = 'index.html'
HOST= '0.0.0.0'
PORT= 40420

# Chain config
LCD = 'https://lcd.bitcanna.io'
DENOM = 'ubcna'
LOGO = 'https://raw.githubusercontent.com/cosmos/chain-registry/master/bitcanna/images/bcna.svg'


# Endpoints v0.47
SUPPLY_BONDED = LCD + '/cosmos/staking/v1beta1/pool'
SUPPLY_TOTAL_DENOM = LCD + '/cosmos/bank/v1beta1/supply/by_denom?denom=' + DENOM
SUPPLY_TOTAL_ALL = LCD + '/cosmos/bank/v1beta1/supply?pagination.limit=3000&pagination.count_total=true'
SUPPLY_CIRCULATING = '' # Total_Denom - Bonded - VESTED_ACCOUNTS_BALANCE
SUPPLY_RICHLIST = LCD + '/cosmos/bank/v1beta1/balances/' # addr/bcna1khyrv2kcx5qsqx46pt78dk3wp8naqnygke0zcl + '/by_denom?denom=' + DENOM
SUPPLY_ACCOUNTS = LCD + '/cosmos/auth/v1beta1/accounts?pagination.limit=3000&pagination.count_total=true'
# APR = ''



# https://api2.bitcanna.io/api/rest/supply/apr
# https://api2.bitcanna.io/api/rest/supply/circulating
# https://api2.bitcanna.io/api/rest/supply/bonded
# https://api2.bitcanna.io/api/rest/supply/total
# https://api2.bitcanna.io/api/rest/supply/total_all
# https://api2.bitcanna.io/api/rest/supply/richlist