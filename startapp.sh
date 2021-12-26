#!/bin/bash
if [ ! -f /data/session.yml ]; then
	echo "No /data/session.yml  file found, copying default"
	cp /app/session.yml /data
fi
if [ $(yq -r .session /data/session.yml) == "null" ]; then
	echo "/data/session.yml is not configured, please run this container manually : 'docker run --rm -ti -v [datamount]:/data acaranta/docker-eero-prometheus-exporter python3 /app/session_init.py'"
	exit 1
fi

echo "Starting eero Exporter & sppedtest exporter on default ports, 9118 & 9119 respectively"
/usr/bin/python3 /app/eero_exporter.py
/usr/bin/python3 /app/eero_speedtest_exporter.py