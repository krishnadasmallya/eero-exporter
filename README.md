# eero-exporter
eero-exporter is a [Prometheus exporter](https://prometheus.io/docs/instrumenting/exporters/) for your personal [eero](https://eero.com) kit. This is a basic implementation, but far more information can be retrieved using the extended version [krishnadasmallya/eero-client](https://github.com/krishnadasmallya/eero-client) library, a second level fork of the original project [343max/eero-client](https://github.com/343max/eero-client) library.

```shell script
# HELP eero_speed_upload_mbps Current service response upload (Mbps)
# TYPE eero_speed_upload_mbps gauge
eero_speed_upload_mbps{id="1234567"} 10.025496
# HELP eero_speed_download_mbps Current service response download (Mbps)
# TYPE eero_speed_download_mbps gauge
eero_speed_download_mbps{id="1234567"} 113.158512
# HELP eero_health_status Current connection status
# TYPE eero_health_status gauge
eero_health_status{source="internet",id="1234567"} 1.0
eero_health_status{source="eero_network",id="1234567"} 1.0
# HELP eero_clients_count Current count of clients
# TYPE eero_clients_count gauge
eero_clients_count{id="1234567"} 12.0
.................
.................
```

## Installation

Download the source from Github.

Install the necessary libraries in your virtualenv

```shell script
pip install -r requirements.txt
```

Before running the eero exporter, you must first populate the session token. It is currently blank in `session.yml`. Running the initialise script will request eero account information.
###### Note: If your account is setup using the Amazon login and not using email/phone initially this may not work for you. Please signout and register using Phone/Email before you can proceed. You may link your account to amazon account after signing up using Phone/Email. 

```shell script
$ python3 session_init.py
your eero login (email address or phone number): <account information here>
verification key from email or SMS: <one time password here>
Session key stored in session.yml
```

After you enter that, check your email or SMS for the one time password, and enter on the command line.

You can review `session.yml` to verify the token is set.

## Usage
The exporter has one argument, the port. The default port is `9118`.

#### For starting Network breakdown stats
```shell script
python eero_exporter.py
```

#### For starting Speedtest
```shell script
python eero_speedtest_exporter.py
```

## Docker
Please see [acaranta's repo](https://github.com/acaranta/docker-eero-prometheus-exporter) for instructions to run via Docker. Thank you, [acaranta](https://github.com/acaranta)!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Thank you
Thank you to [343max](https://github.com/343max) for providing the excellent eero client library. 

## License
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)