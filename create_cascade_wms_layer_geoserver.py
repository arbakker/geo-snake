#!/usr/local/bin/python3
"""create_cascade_wms_layer_geoserver.py: create cascading wms layer in GeoServer"""
from urllib3.exceptions import ProtocolError
import argparse
import requests
from sys import exit
import xml.etree.ElementTree as ET
import http.client
from util import *

def parse_args(args):
    parser = argparse.ArgumentParser(description='Create a cascaded WMS datastore (if not exists) and publish layer from that datastore.')
    parser.add_argument('--datastore', type=str)
    parser.add_argument('--workspace', type=str)
    parser.add_argument('--baseurl', type=str)
    parser.add_argument('--capabilitiesurl', type=str)
    parser.add_argument('--layername', type=str)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    workspace = args.workspace
    datastore = args.datastore
    baseurl = args.baseurl
    capabilitiesurl = args.capabilitiesurl
    layername = args.layername
    username = args.username
    password = args.password
    gs_client = GeoserverClient(username, password, baseurl)
    workspace_url = gs_client.get_workspace_url(workspace)

    if not ResourceExists(workspace_url):
        print("Error: workspace {0} does not exist".format(workspace))
        exit(1)

    # check if datastore exists
    datastore_url = "{0}/rest/workspaces/{1}/wmsstores/{2}.xml".format(baseurl, workspace, datastore)
    if (not ResourceExists(datastore_url)):
        print("Datastore {0} does not exist".format(datastore))
        with open('wms_cascade.xml', 'r') as myfile:
            ds_template = myfile.read().replace('\n', '')
            ds = ds_template.format(datastore, workspace, baseurl, capabilitiesurl)
            new_ds_url = "{0}/rest/workspaces/{1}/wmsstores.xml".format(baseurl, workspace)
            if not CreateResource(new_ds_url, ds):
                print("Error: failed to create datastore {0}:{1}".format(workspace, datastore))
                exit(1)


    print("Datastore {0} exists".format(datastore_url))


    layers_url = "{0}/rest/workspaces/{1}/wmsstores/{2}/wmslayers.xml?list=available".format(baseurl, workspace, datastore)
    print(layers_url)
    layers_xml = GetResource(layers_url)

    print(layers_xml)

    root = ET.fromstring(layers_xml)
    available_layers=[]
    for child in root:
        available_layers.append(child.text)

    if not layername in available_layers:
        print("Layer {0} not available in datastore {2}".format(layername, datastore_url))

    new_wmslayer_url = "{0}/rest/workspaces/{1}/wmsstores/{2}/wmslayers.xml".format(baseurl, workspace, datastore)

    with open('wmslayer.xml', 'r') as myfile:
        lyr_template = myfile.read().replace('\n', '')
        lyr = lyr_template.format(layername,workspace, datastore, baseurl)
        if not CreateResource(new_wmslayer_url, lyr):
            print("Error: failed to create wmslayer {0}:{1}".format(workspace, layername))
            exit(1)
    print("Created wmslayer {0}:{1}".format(workspace, layername))

# ./script.py --baseurl http://localhost:8000/geoserver_2.10 --capabilitiesurl http://localhost:8000/geoserver_2.10/charts/wms?request=getcapabilities --workspace cite --datastore charts_casc --layername world_borders --username admin --password geoserver
if __name__ == "__main__":
    main(sys.argv[1:])
    
    





















