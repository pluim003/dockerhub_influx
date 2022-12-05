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

Configuration options above can be specified within the environment section of the compose file.

dockerhub-influx.service - A SystemD Unit File for starting dockerhub_influx at boot (and logging) On Centos7, put this file in /lib/systemd/system/.

Run:

systemctl daemon-reload
systemctl enable dockerhub-influx
systemctl start dockerhub-influx

To run dockerhub_influx.py from the command line without the startup script:

/usr/bin/python ./dockerhub_influx.py

I only use the docker-variant.
You could instal this script in /opt/dockerhub_influx. If you put it somewhere else you'll have to update the systemD startup script.

### Troubleshooting

If you get the following error:

Traceback (most recent call last): File "./dockerhub_influx.py", line 11, in <module> from influxdb import InfluxDBClient

You'll need to install the python-influxdb module for python. On a raspberry pi, you can do this with:

sudo apt-get install python-influxdb

Or on CentOS / RHEL:

yum install python-influxdb

If you get this error:

Traceback (most recent call last): File "./dockerhub_influx.py", line 8, in <module> import requests ImportError: No module named requests

You'll need to install the python-requests module.

### Credits

Credits go to https://github.com/chrisbergeron/ for supplying the pihole_influx-script. After some modifications earlier I decided to make it suitable to get Dockerhub-statistics

### Background

I used the docker-hub-exporter for a while which exports data to a Promotheus-database. Created by https://github.com/badsmoke . But didn't like the way stuff was stored and with zero knowledge of golang I couldn't get it the way I wanted it.

### To do

Maybe enter a username instead of image-names to get all images by a specific user.
