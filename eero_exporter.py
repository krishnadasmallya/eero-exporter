#!/usr/bin/env python
from argparse import ArgumentParser
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import eero
import time
import cookie_store

class JsonCollector(object):
    def collect(self):
        account = eero.account()
        for network in account['networks']['data']:
            network_details = eero.networks(network['url'])
            network_speed = network_details['speed']

            id = network['url'].split('/')[3]
            network_name = network['name']
            metric1 = GaugeMetricFamily('eero_speed_upload_mbps', 'Current service response upload (Mbps)', labels=['network'])
            metric1.add_metric([network_name], value=network_speed['up']['value'])
            yield metric1
            metric2 = GaugeMetricFamily('eero_speed_download_mbps', 'Current service response download (Mbps)', labels=['network'])
            metric2.add_metric([network_name], value=network_speed['down']['value'])
            yield metric2

            network_health = network_details['health']
            metric3 = GaugeMetricFamily('eero_health_status', 'Current connection status', labels=['network', 'source'])
            metric3.add_metric([network_name, 'internet'], 1 if network_health['internet']['status'] == 'connected' else 0)
            metric3.add_metric([network_name, 'eero_network'], 1 if network_health['eero_network']['status'] == 'connected' else 0)
            yield metric3

            network_clients = network_details['clients']
            metric4 = GaugeMetricFamily('eero_clients_count', 'Current count of clients', labels=['network'])
            metric4.add_metric([network_name], network_clients['count'])
            yield metric4

            network_data_usages = eero.data_usage_last_5_min_breakdown(id)
            # starttime = network_data_usages['start']
            # endtime = network_data_usages['end']

            upload_speed = network_data_usages['upload']
            metric5 = GaugeMetricFamily('eero_network_usage_upload', 'Current upload speed for the eero device', labels=['network'])
            metric5.add_metric([network_name], upload_speed)
            yield metric5

            download_speed = network_data_usages['download']
            metric6 = GaugeMetricFamily('eero_network_usage_download', 'Current download speed for the eero device', labels=['network'])
            metric6.add_metric([network_name], download_speed)
            yield metric6

            # print(starttime, endtime, upload_speed, download_speed)
            for eeros in network_data_usages['eeros']:
                label = eeros['location']
                upload = eeros['upload']
                download = eeros['download']
                metric1 = GaugeMetricFamily('eero_network_usage_eeros_upload', 'Current upload speed for the eero device',
                                            labels=['network', 'eero'])
                metric1.add_metric([network_name, label], upload)
                yield metric1

                metric2 = GaugeMetricFamily('eero_network_usage_eeros_download', 'Current download speed for the eero device',
                                            labels=['network', 'eero'])
                metric2.add_metric([network_name, label], download)
                yield metric2

            for devices in network_data_usages['devices']:
                label = devices['hostname']
                upload = devices['upload']
                download = devices['download']
                metric1 = GaugeMetricFamily('eero_network_usage_devices_upload',
                                            'Current upload speed for the connected device',
                                            labels=['network', 'device'])
                metric1.add_metric([network_name, label], upload)
                yield metric1

                metric2 = GaugeMetricFamily('eero_network_usage_devices_download',
                                            'Current download speed for the connected device',
                                            labels=['network', 'device'])
                metric2.add_metric([network_name, label], download)
                yield metric2

            for profiles in network_data_usages['profiles']:
                label = profiles['profile_name']
                upload = profiles['upload']
                download = profiles['download']
                metric1 = GaugeMetricFamily('eero_network_usage_profiles_upload',
                                            'Current upload speed for the eero profile',
                                            labels=['network', 'eero'])
                metric1.add_metric([network_name, label], upload)
                yield metric1

                metric2 = GaugeMetricFamily('eero_network_usage_profiles_download',
                                            'Current download speed for the eero profile',
                                            labels=['network', 'eero'])
                metric2.add_metric([network_name, label], download)
                yield metric2

            for unprofiled in network_data_usages['unprofiled']:
                label = unprofiled['name']
                upload = unprofiled['upload']
                download = unprofiled['download']
                metric1 = GaugeMetricFamily('eero_network_usage_unprofiled_upload',
                                            'Current upload speed for the eero unprofiled',
                                            labels=['network', 'eero'])
                metric1.add_metric([network_name, label], upload)
                yield metric1

                metric2 = GaugeMetricFamily('eero_network_usage_unprofiled_download',
                                            'Current download speed for the eero unprofiled',
                                            labels=['network', 'eero'])
                metric2.add_metric([network_name, label], download)
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
        port = 9118
    REGISTRY.register(JsonCollector())
    start_http_server(port)
    print("Server is up and running..")
    coll = JsonCollector()
    while True:
        coll.collect()
        time.sleep(1)
