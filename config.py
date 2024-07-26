# -*- coding: utf-8 -*-

# Server config
PATH = './' # Production: '/var/www/endpoints/'
CSV_LOG_OUTPUT_FILE = PATH + 'log.csv'
RICHLIST_FILE = PATH + 'richlist.json'
VESTING_FILE = PATH + 'vesting.json'
CHAIN_FILE = PATH + 'chain_metrics.json'
HTML_DOC = PATH + 'index.html'
HOST= '0.0.0.0'
PORT= 3030
TIME_TO_SLEEP = 60 * 60 # 1 hour

# Chain config
LCD = 'https://lcd.bitcanna.io'
DENOM = 'ubcna'
LOGO = 'https://raw.githubusercontent.com/cosmos/chain-registry/master/bitcanna/images/bcna.svg'


# Endpoints v0.47
INFLATION = LCD + '/cosmos/mint/v1beta1/inflation'
SUPPLY_BONDED = LCD + '/cosmos/staking/v1beta1/pool'
SUPPLY_TOTAL_DENOM = LCD + '/cosmos/bank/v1beta1/supply/by_denom?denom=' + DENOM
SUPPLY_TOTAL_ALL = LCD + '/cosmos/bank/v1beta1/supply?pagination.limit=3000&pagination.count_total=true'
SUPPLY_CIRCULATING = '' # Total_Denom - Bonded - VESTED_ACCOUNTS_BALANCE
SUPPLY_RICHLIST = LCD + '/cosmos/bank/v1beta1/balances/' # addr/bcna1khyrv2kcx5qsqx46pt78dk3wp8naqnygke0zcl + '/by_denom?denom=' + DENOM
SUPPLY_ACCOUNTS = LCD + '/cosmos/auth/v1beta1/accounts?pagination.limit=5000&pagination.count_total=true'
