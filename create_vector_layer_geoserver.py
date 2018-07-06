#!/usr/bin/env python
"""create_vector_layer_geoserver.py: create new vector layer from existing datastore in GeoServer"""
import argparse
import requests
from sys import exit
import http.client
from util.util import *
from util.geoserver_client import *

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("gs_url", type=str, help="GeoServer url")
    parser.add_argument("workspace", type=str, help="workspace")
    parser.add_argument("datastore", type=str, help="datastore")
    parser.add_argument("tablename", type=str, help="Name of table to publish")
    parser.add_argument("new_ft", type=str, help="Name of new featuretype to create")
    parser.add_argument("sld_file", type=str, help="Path of sld file")
    parser.add_argument("style_name", type=str, help="Name of new style to create")
    parser.add_argument("username", type=str, help="GeoServer username")
    parser.add_argument("password", type=str, help="GeoServer password")
    parser.add_argument('--rm', action='store_true', help="Remove layer")
    args = parser.parse_args()
    return args

def main(args):
    args = parse_args(args)
    base_url = args.gs_url #"http://192.168.179.1:8000/geoserver_2.13"
    workspace = args.workspace #"cite"
    datastore = args.datastore #"postgis"
    tablename = args.tablename #"usa_states"
    new_ft = args.new_ft #"new_ft"
    sld_file = args.sld_file #"sld.xml"
    style_name = args.style_name #"new_style"
    username = args.username #"admin"
    password = args.password #"geoserver" 
    rollback = args.rm #True

    gs_client = GeoserverClient(username, password, base_url)
    fts_url = gs_client.get_features_in_datastore_url(workspace, datastore)
    new_ft_url = gs_client.get_feature_url(workspace, datastore, new_ft)
    new_layer_url = gs_client.get_layer_url(workspace, new_ft)
    new_style_url = gs_client.get_style_url(workspace, style_name)
    styles_url = gs_client.get_new_style_url(workspace, style_name)

    # create new featuretype, http://docs.geoserver.org/stable/en/user/rest/api/featuretypes.html
    # /workspaces/<ws>/datastores/<ds>/featuretypes[.<format>]
    if rollback:
        gs_client.delete_gs_resource(new_layer_url)
        if gs_client.exists_gs_resource(new_layer_url):
            print("Error: failed to delete layer {0}:{1}".format(workspace, new_ft))
            exit(1)
        gs_client.delete_gs_resource(new_ft_url)
        if gs_client.exists_gs_resource(new_ft_url):
            print("Error: failed to delete featuretype {0}:{1}".format(workspace, new_ft))
            exit(1)
        gs_client.delete_gs_resource(new_style_url)
        if gs_client.exists_gs_resource(new_style_url):
            print("Error: failed to delete style {0}:{1}".format(workspace, style_name))
            exit(1)      
    else:
        with open('xml/ft.xml', 'r') as myfile:
            ft_template = myfile.read().replace('\n', '')
            ft = ft_template.format(new_ft, tablename)
            print("new ft url: " + fts_url)
            headers = {'content-type': 'application/xml'}
            
            gs_client.create_resource(fts_url, ft, headers)

            if not gs_client.exists_gs_resource(new_ft_url):
                print("Error: failed to create featuretype {0}:{1}".format(workspace, new_ft))
                exit(1)
            else:
                print("Created featuretype: {0}:{1}".format(workspace,new_ft))

            if not gs_client.exists_gs_resource(new_style_url):
                with open(sld_file, 'r') as mystyle:
                    # content-type: application/vnd.ogc.sld+xml
                    style_xml = mystyle.read()
                    headers = {'content-type': 'application/vnd.ogc.sld+xml'} 
                    gs_client.create_resource(styles_url, style_xml, headers)
                    if not gs_client.exists_gs_resource(new_style_url):
                        print("Error: failed to create style {0}:{1}".format(workspace, style_name))
                        exit(1)
                    else:
                        print("Created style: {0}:{1}".format(workspace, style_name))


#create_vector_layer_geoserver.py http://192.168.179.1:8000/geoserver_2.13 cite postgis usa_states new_ft xml/sld.xml new_style admin geoserver
if __name__ == "__main__":
    main(sys.argv[1:])
    
                    









