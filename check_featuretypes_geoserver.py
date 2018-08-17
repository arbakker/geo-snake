#!/usr/bin/env python
"""check_wms_layers_geoserver.py: test for all layers in GeoServer if the WMS service for that layer is functional"""
import argparse
import requests
import sys
import time
from sys import exit
import csv
import os
from random import randint
from time import sleep
from util.geoserver_client import *

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("gs_user", type=str, help="GeoServer user")
    parser.add_argument("gs_password", type=str, help="Password for GeoServer user")
    parser.add_argument("gs_url", type=str, help="GeoServer url")
    args = parser.parse_args(args)
    return args

def get_csv_path():
    base_path = os.path.abspath(os.path.dirname(__file__))
    csv_path = "csv"
    return os.path.join(base_path, csv_path)

def get_count_csv_file(csv_path):
    count_csv_name = "verify_fts_report_count.csv"
    count_csv_file = os.path.join(csv_path, count_csv_name)
    return count_csv_file

def get_errors_csv_file(csv_path):
    errors_csv_name = "verify_fts_report_layer_errors.csv"
    errors_csv_file = os.path.join(csv_path, errors_csv_name)
    return errors_csv_file

def main(args):
    start = time.time()
    args = parse_args(args)
    gs_user = args.gs_user
    gs_password = args.gs_password 
    gs_url = args.gs_url
    gs_client = GeoserverClient(gs_user, gs_password, gs_url)

    workspaces = gs_client.list_workspaces()

    results = []
    broken_fts = []
    results.append(["workspace_name", "working_fts", "broken_fts"])
    broken_fts.append(["workspace_name", "ft", "ft_url", "exception_message"])
    count=0
    for ws in workspaces:
        fts = gs_client.list_featuretypes(ws)

        broken_count = 0
        working_count = 0
        for ft in fts:
            ft_url = gs_client.get_feature_url(ws, ft)
            try:
                xml = gs_client.get_resource(ft_url)    
                gs_client.validate_ft(xml)
                working_count += 1
            except Exception as e:
                broken_count +=1
                template = "Exception type: {0}. Message: {1}"
                message = template.format(type(e).__name__, str(e))
                broken_fts.append([ws, ft, ft_url, message])
                
        results.append([ws, working_count, broken_count])
        count+=1
        if count > 2:
            break

    total_broken = 0
    total_working = 0

    # skip first item in collection
    iterresults = iter(results)
    next(iterresults)
    for result in iterresults:
        total_working += result[1]
        total_broken += result[2]

    results.append(["total",total_working, total_broken])

    csv_path = get_csv_path()
    count_csv_file = get_count_csv_file(csv_path)
    errors_csv_file = get_errors_csv_file(csv_path)

    remove_file(count_csv_file)
    remove_file(errors_csv_file)

    with open(count_csv_file, "w") as file:
        writer = csv.writer(file, delimiter='@')
        writer.writerows(results)

    with open(errors_csv_file, "w") as file:
        writer = csv.writer(file, delimiter='@')
        writer.writerows(broken_fts)
    end = time.time()
    #print("runtime script {0}: {1}".format(os.path.basename(__file__),end-start))



# Call script with: verify_layers.py admin geoserver https://localhost:8080/geoserver
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
    
    





