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
    csv_path = "csv"
    return csv_path

def get_count_csv_file(csv_path):
    count_csv_name = "verify_layers_report_count.csv"
    count_csv_file = os.path.join(csv_path, count_csv_name)
    return count_csv_file

def get_errors_csv_file(csv_path):
    errors_csv_name = "verify_layers_report_layer_errors.csv"
    errors_csv_file = os.path.join(csv_path, errors_csv_name)
    return errors_csv_file

def main(args):
    args = parse_args(args)
    gs_user = args.gs_user
    gs_password = args.gs_password 
    gs_url = args.gs_url
    gs_client = GeoserverClient(gs_user, gs_password, gs_url)
    workspaces = gs_client.list_workspaces()
    results = []
    broken_layers = []
    results.append(["workspace_name", "working_layers_count", "broken_layers_count"])
    broken_layers.append(["workspace_name", "layername", "reflect_url", "service_exception_message"])
    start = time.time()
    break_count = 0
    for workspace in workspaces:
        print("WS:" + workspace)
        start = time.time()
        layernames = gs_client.get_wms_layers_in_workspace(workspace)
        broken_layers_count = 0
        working_layers_count = 0
        layernames = [layername.split(":")[1] if ":" in layername else layername for layername in layernames]
        end = time.time()
        print("ws_loop: {0}".format(end-start))
        
        start = time.time()
        for layer in layernames:
            print("ly:" + layer)
            error_message = gs_client.test_valid_wms_response(workspace, layer)
            if error_message:
                reflect_url = gs_client.get_reflect_url(workspace, layer)
                error_message = error_message.replace("@","\@")
                broken_layers.append([workspace, layer, reflect_url, error_message])
                broken_layers_count += 1
            else:
                working_layers_count += 1
        end = time.time()
        print("layer_loop: {0}".format(end-start))

        start = time.time()        
        results.append([workspace, working_layers_count, broken_layers_count])
        break_count += 1
        if break_count > 2:
            break
        end = time.time()
        print("end_loop: {0}".format(end-start))


    end = time.time()
    print("perf'_loop': {0}".format(end-start))

    start = time.time()
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
    end = time.time()
    print("perf_middle: {0}".format(end-start))


    start = time.time()
    with open(count_csv_file, "w") as file:
        writer = csv.writer(file, delimiter='@')
        writer.writerows(results)

    with open(errors_csv_file, "w") as file:
        writer = csv.writer(file, delimiter='@')
        writer.writerows(broken_layers)
    end = time.time()
    print("perf_csv: {0}".format(end-start))



# Call script with: verify_layers.py admin geoserver https://localhost:8080/geoserver
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
    
    





