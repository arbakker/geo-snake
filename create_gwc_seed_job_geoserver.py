#!/usr/local/bin/python3
"""create_gwc_seed_job_geoserver.py: create tilecache seed job in GeoServer"""
from urllib3.exceptions import ProtocolError
import argparse
import requests
from sys import exit
import xml.etree.ElementTree as ET
import http.client
from util import *

def parse_args(args):
    parser = argparse.ArgumentParser(description='Create a GeoWebCache seed job.')
    parser.add_argument('--baseurl', type=str)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--minx', type=str)
    parser.add_argument('--maxx', type=str)
    parser.add_argument('--miny', type=str)
    parser.add_argument('--maxy', type=str)
    parser.add_argument('--gridsetid', type=str)
    parser.add_argument('--minzoom', type=str)
    parser.add_argument('--maxzoom', type=str)
    parser.add_argument('--layername', type=str)
    parser.add_argument('--style', type=str)
    # see, reseed or operation
    parser.add_argument('--operation', type=str)
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    baseurl = args.baseurl
    username = args.username
    password = args.password
    minx = args.minx
    miny = args.miny
    maxx = args.maxx
    maxy = args.maxy
    gridsetid = args.gridsetid
    minzoom = args.minzoom
    maxzoom = args.maxzoom
    layername = args.layername
    style = args.style
    operation = args.operation
    layer_url = "{0}/gwc/rest/layers/{1}.xml".format(baseurl, layername)
    seed_url = "{0}/gwc/rest/seed/{1}.xml".format(baseurl, layername)

    if not ResourceExists(layer_url, username, password):
        print("Error: geowebcache layer {0} does not exist".format(layername))
        exit(1)
    with open('xml/seed_job.xml', 'r') as myfile:
        job_template = myfile.read().replace('\n', '')
        job = job_template.format(layername, minx, miny, maxx, maxy, gridsetid, minzoom, maxzoom, operation, style)

        if not CreateResource(seed_url, username, password, job):
            print("Error: failed to create geowebcache seed job for layer {0} at {1}".format(layername, seed_url))
            exit(1)
    print("Succes: created geowebcache seed job for layer {0} at {1}".format(layername, seed_url))
    exit(0)

# ./create_gwc_seed_job_geoserver --baseurl http://localhost:8000/geoserver --username admin --password geoserver --gridsetid EPSG:900913 --minzoom 14 --maxzoom 18 --layername rws_enc --style '' --operation seed --minx 438766.88770604855 --miny 6783066.093828267 --maxx 457234.06219725823 --maxy 6800945.2382005295
if __name__ == "__main__":
    main(sys.argv[1:])
    








