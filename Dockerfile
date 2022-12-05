FROM python:3.11-alpine

RUN pip install --no-cache-dir influxdb

WORKDIR /usr/src/app

COPY dockerhub_influx.py ./

CMD [ "python", "/usr/src/app/dockerhub_influx.py" ]
