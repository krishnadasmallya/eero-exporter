#!/usr/bin/env python
from argparse import ArgumentParser
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import eero
import time
import cookie_store
from pytz.reference import LocalTimezone
from dateutil.parser import *

class JsonCollector(object):
    def collect(self):
        account = eero.account()
        for network in account['networks']['data']:
            id = network['url'].split('/')[3]
            network_name = network['name']
            eero.start_speed_test(id)
            time.sleep(1 * 60) # sleep for a min for speedtest to complete
            speeds = eero.get_speed_test(id)
            latest_speed = speeds[0]
            up_mbps = latest_speed['up_mbps']
            down_mbps = latest_speed['down_mbps']
            datestring = latest_speed['date']
            dt = parse(datestring)
            datetime=dt.astimezone(LocalTimezone()).isoformat()
            metric1 = GaugeMetricFamily('eero_network_speedtest_upload',
                                        'Latest upload speed for the network',
                                        labels=['network','date'])
            metric1.add_metric([network_name, datetime], up_mbps)
            yield metric1
            metric2 = GaugeMetricFamily('eero_network_speedtest_download',
                                        'Latest download speed for the network ',
                                        labels=['network','date'])
            metric2.add_metric([network_name, datetime], down_mbps)
            yield metric2


session = cookie_store.CookieStore('session.yml')
eero = eero.Eero(session)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-port", help="port to run the exporter on")
    args = parser.parse_args()

    if args.port:
        port = int(args.port)
    else:
        port = 9119
    REGISTRY.register(JsonCollector())
    start_http_server(port)
    print("Server is up and running..")

    coll = JsonCollector()
    while True:
        coll.collect()
        time.sleep(1)
