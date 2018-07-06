#!/usr/local/bin/python3
"""create_gwc_wms_layer_geoserver.py: create GWC tile layer in GeoServer based on WMS source"""
from urllib3.exceptions import ProtocolError
import argparse
import requests
from sys import exit
import xml.etree.ElementTree as ET
import http.client
from util import *

def parse_args(args):
    parser = argparse.ArgumentParser(description='Create GWC tile layer in GeoServer based on WMS source')
    parser.add_argument('--baseurl', type=str)
    parser.add_argument('--wmsurl',  type=str)
    parser.add_argument('--wmslayers', type=str)
    parser.add_argument('--wmsworkspace', type=str)
    parser.add_argument('--newlayername', type=str)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    baseurl = args.baseurl
    wmsurl = args.wmsurl
    wmslayers = args.wmslayers
    newlayername = args.newlayername
    username = args.username
    password = args.password

    newlayer_url = "{0}/gwc/rest/layers/{1}.xml".format(baseurl, newlayername)
    # Check if gwc does not already exist
    if ResourceExists(newlayer_url, username, password):
        print("Error: geowebcache layer {0} already exists".format(newlayername))
        exit(1)
    with open('xml/gwc_wms_layer.xml', 'r') as myfile:
        gwc_template = myfile.read().replace('\n', '')
        gwc = gwc_template.format(newlayername, wmsurl, wmslayers)
        if not CreatePutResource(newlayer_url, username, password, gwc):
            print("Error: failed to create geowebcache layer {0}".format(newlayername))
            exit(1)
    print("Succes: created geowebcache layer {0} at {1}".format(newlayername, newlayer_url))
    exit(0)


# ./create_gwc_wms_layer_geoserver.py --baseurl http://localhost:8000/geoserver --wmsurl "http://somehost/wms?" --wmslayers 2 --newlayername rws_2 --username admin --password geoserver
if __name__ == "__main__":
    main(sys.argv[1:])


