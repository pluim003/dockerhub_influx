#! /usr/bin/python

# Script originally created by JON HAYWARD: https://fattylewis.com/Graphing-pi-hole-stats/
# Adapted to work with InfluxDB by /u/tollsjo in December 2016
# Updated by Cludch December 2016
# Updated and dockerised by rarosalion in September 2019
# Updated by Dick Pluim December 2022 and modified to use with Dockerhub 

# To install and run the script as a service under SystemD. See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux

import requests
import time
import json
import os
import logging
from influxdb import InfluxDBClient

# Modify these values if running as a standalone script
_DEFAULTS = {
    'INFLUXDB_SERVER': "127.0.0.1",  # IP or hostname to InfluxDB server
    'INFLUXDB_PORT': 8086,  # Port on InfluxDB server
    'INFLUXDB_USERNAME': "username",
    'INFLUXDB_PASSWORD': "password",
    'INFLUXDB_DATABASE': "piholestats",
    'DELAY': 600,  # seconds
    'DOCKERHUB_IMAGES': ["pluim003/dockerhub_influx"],  # Dockerhub images 
}


def get_config():
    """ Combines config options from config.json file and environment variables """

    # Read a config file (json dictionary) if it exists in the script folder
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(script_dir, 'config.json')
    if os.path.exists(config_file):
        config = json.load(open(config_file))
    else:
        config = _DEFAULTS

    # Overwrite config with environment variables (set via Docker)
    for var_name in _DEFAULTS.keys():
        config[var_name] = os.getenv(var_name, _DEFAULTS[var_name])
        if var_name == 'DOCKERHUB_IMAGES' and ',' in config[var_name]:
            config[var_name] = config[var_name].split(',')

    # Make sure DOCKERHUB_IMAGES is a list (even if it's just one entry)
    if not isinstance(config['DOCKERHUB_IMAGES'], list):
        config['DOCKERHUB_IMAGES'] = [config['DOCKERHUB_IMAGES']]

    return config


def check_db_status(config, logger):
    """ Check the required DB exists, and create it if necessary """

    logger.debug("Connecting to {}".format(config['INFLUXDB_SERVER']))
    client = InfluxDBClient(
        config['INFLUXDB_SERVER'],
        config['INFLUXDB_PORT'],
        config['INFLUXDB_USERNAME'],
        config['INFLUXDB_PASSWORD']
    )

    if {"name": config['INFLUXDB_DATABASE']} not in client.get_list_database():
        logger.info('Database {} not found. Will attempt to create it.'.format(config['INFLUXDB_DATABASE']))
        client.create_database(config['INFLUXDB_DATABASE'])
        return True
    else:       
        logger.info('Found existing database {}.'.format(config['INFLUXDB_DATABASE']))
        return True


def send_msg(config, logger, image, user, name, pull_count, star_count, last_updated, status):
    """ Sends message to InfluxDB server defined in config """
    json_body = [
        {
            "measurement": "dockerhubstats." + image.replace(".", "_"),
            "tags": {
                "image": image 
            },
            "fields": {
                "user": user,
                "name": name,
                "pull_count": int(pull_count),
                "star_count": int(star_count),
                "last_updated": last_updated,
                "status": status
            }
        }
    ]
    logger.debug(json_body)

    # InfluxDB host, InfluxDB port, Username, Password, database
    client = InfluxDBClient(
        config['INFLUXDB_SERVER'],
        config['INFLUXDB_PORT'],
        config['INFLUXDB_USERNAME'],
        config['INFLUXDB_PASSWORD'],
        config['INFLUXDB_DATABASE']
    )

    client.write_points(json_body)
    print(json_body)


if __name__ == '__main__':

    # Setup logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

    # Get configuration details
    config = get_config()
    number_of_images = len(config['DOCKERHUB_IMAGES'])
    logger.info("Querying {} dockerhub images: {}".format(len(config['DOCKERHUB_IMAGES']), config['DOCKERHUB_IMAGES']))
    logger.info("Logging to InfluxDB server {}:{}".format(
        config['INFLUXDB_SERVER'], config['INFLUXDB_PORT']
    ))

    # Create database if it doesn't exist
    check_db_status(config, logger)
    
    # Loop pulling stats from dockerhub, and pushing to influxdb
    while True:
        i = 0
        for i in range(number_of_images): 
            image = config['DOCKERHUB_IMAGES'][i]
            # Get Dockerhub Stats
            dockerhub_api = "https://hub.docker.com/v2/repositories/{}".format(image)
            logger.info("Attempting to contact {} with URL {}".format(image, dockerhub_api))
            api = requests.get(dockerhub_api)  # URI to dockerhub server api
            print (api)
            API_out = api.json()
            user = (API_out['user'])
            name = (API_out['name'])
            pull_count = (API_out['pull_count'])
            star_count = (API_out['star_count'])
            last_updated = (API_out['last_updated'])
            status = (API_out['status'])

            # Update DB
            send_msg(config, logger, image, user, name, pull_count, star_count, last_updated, status)
            i = i + 1

        # Wait...
        logger.info("Waiting {}".format(config['DELAY']))
        time.sleep(int(config['DELAY']))
