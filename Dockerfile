FROM debian

RUN yum update && yum install -y git python3-pip jq
RUN mkdir /app
WORKDIR /app
RUN git clone git@github.com:krishnadasmallya/eero-exporter.git /app
RUN pip3 install -r requirements.txt
RUN pip3 install yq
WORKDIR /data

CMD ["/app/startapp.sh"]