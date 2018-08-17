#!/usr/bin/env python
"""remove_all_layers_workspace_geoserver.py: removes all layers in a workspace and (TODO) removes the linked metadata in the catalogue"""
import argparse
import requests
from sys import exit
from util.geoserver_client import *
from util.csw_client import *
from lxml import etree, objectify
import csv
import os
import xml.etree.ElementTree as ET

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--cat_user", type=str, help="Catalogue user, only required when rm_md=True")
    parser.add_argument("--cat_password", type=str, help="Password for catalogue user, only required when rm_md=True")
    parser.add_argument("--cat_url", type=str, help="Catalogue url, only required when rm_md=True")
    parser.add_argument("gs_user", type=str, help="GeoServer user")
    parser.add_argument("gs_password", type=str, help="Password for GeoServer user")
    parser.add_argument("gs_url", type=str, help="GeoServer url")
    parser.add_argument("gs_workspace", type=str, help="GeoServer workspace to remove, script will remove all layers from workspace and workspace")
    parser.add_argument('--rm_md', action='store_true', help="remove linked metadata record from catalogue")
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    gs_user = args.gs_user
    gs_password = args.gs_password 
    gs_url = args.gs_url
    gs_workspace = args.gs_workspace
    rm_md = args.rm_md
    if rm_md:
        gn_url = args.cat_url
        gn_user = args.cat_user
        gn_password = args.cat_password

    gs_client = GeoserverClient(gs_user, gs_password, gs_url)
    layers_in_workspace = gs_client.list_layers(gs_workspace)
    md_ids = set()
    for l in layers_in_workspace:
        layer_url = gs_client.get_layer_url(gs_workspace, l)
        ft_url = gs_client.get_featuretypeurl_by_layer(gs_workspace, l)
        md_id = ""
        if rm_md:
            md_id = gs_client.get_metadataid_from_featuretype(ft_url)
            md_ids.add(md_id)
    
    if rm_md:
        csw_client = CSWClient(gn_user, gn_password, gn_url)
        for md_id in md_ids:
            record_url = csw_client.get_record_url(md_id)
            if csw_client.resource_exists(record_url):
                # remove record
                print("remove record")
        # TODO: delete metadata of layer
        #gs_client.delete_gs_resource(layer_url)
        #gs_client.delete_gs_resource(ft_url)

# remove_all_layers_workspace admin geoserver http://localhost:8000/geoserver_2.13 swd --rm_md --cat_user admin --cat_password admin --cat_url http://localhost:8000/geonetwork
if __name__ == "__main__":
    main(sys.argv[1:])

    





