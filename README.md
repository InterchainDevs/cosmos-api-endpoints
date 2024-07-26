# Cosmos-api-endpoints
Cosmos chains endpoints for CMC &amp; Coingecko, etc

## Config
Edit config.py with LCD & DENOM
Customize endpoints if necessary

## Install python deps.
pip3 install flask flask_cors requests

## Run the JSON maker engine
python3 calculated_metrics.py

## Run the API web server
python3 endpoints-server.py

## Optional. Create systemd service files:

### Create the systemd for the Webserver:
```bash
 cd $HOME
 echo "[Unit]
 Description=endpoints-server Script
 After=network-online.target
 [Service]
 User=${USER}
 ExecStart=$(which python3) /home/raul/cosmos-api-endpoints/endpoints-server.py
 Restart=always
 RestartSec=3
 LimitNOFILE=4096
 [Install]
 WantedBy=multi-user.target
 " >endpoints-server.service
 ```

 Enable and activate the `endpoints-server` service.
```bash
sudo mv endpoints-server.service /lib/systemd/system/
sudo systemctl enable endpoints-server.service && sudo systemctl start endpoints-server.service
```
Check the logs to see if everything is working correct:
```bash
sudo journalctl -fu endpoints-server -o cat
```

### Create the systemd for the Calculate Engine:
```bash
 cd $HOME
 echo "[Unit]
 Description=endpoints-calculate Script
 After=network-online.target
 [Service]
 User=${USER}
 ExecStart=$(which python3) /home/raul/cosmos-api-endpoints/calculated_values.py
 Restart=always
 RestartSec=3
 LimitNOFILE=4096
 [Install]
 WantedBy=multi-user.target
 " >endpoints-calculate.service
 ```

 Enable and activate the `endpoints-calculate` service.
```bash
sudo mv endpoints-calculate.service /lib/systemd/system/
sudo systemctl enable endpoints-calculate.service && sudo systemctl start endpoints-calculate.service
```
Check the logs to see if everything is working correct:
```bash
sudo journalctl -fu endpoints-calculate -o cat
```