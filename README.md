## Dockerhub_Influx

A basic script for inserting dockerhub data into influxdb for graphing.

*dockerhub_influx.py* - A python script for inserting records into influxdb.

Configuration options:
``` bash
INFLUXDB_SERVER = "127.0.0.1" # IP or hostname to InfluxDB server
INFLUXDB_PORT = 8086 # Port on InfluxDB server
INFLUXDB_USERNAME = "username"
INFLUXDB_PASSWORD = "password"
INFLUXDB_DATABASE = "piholestats"
DELAY = 600 # seconds
DOCKERHUB_IMAGES = "pluim003/dockerhub_influx" # Dockerhub image(s) to report in InfluxDB for each measurement. Comma separated list.
```
*docker-compose.yml* - An example Docker setup to run this script

Configuration options above can be specified within the environment section of the compose file.

Run:

Make a subdirectory for your installation
Create and edit docker-compose.yml to your needs

``` bash
docker-compose up -d
```

