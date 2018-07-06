#!/usr/bin/env python
"""checkmk_check_wms_layers_geoserver.py: Check MK local check to test for all layers in GeoServer if the WMS service for that layer is functional"""
import check_wms_layers_geoserver
import csv
import configparser

if __name__ == "__main__":

    # required to make checkmk_verify_layers.ini in this folder to set url to check with credentials:
    # example checkmk_check_wms_layers_geoserver.ini:
    # [DEFAULT]
    # user = admin
    # password = geoserver
    # url = http://localhost:8000/geoserver/
    config = configparser.ConfigParser()
    config.read('checkmk_check_wms_layers_geoserver.ini')
    user = config['DEFAULT']['user']
    password = config['DEFAULT']['password']
    url = config['DEFAULT']['url']

    check_wms_layers_geoserver.main([user, password, url])
    csv_path = check_wms_layers_geoserver.get_csv_path()
    count_csv_file = check_wms_layers_geoserver.get_count_csv_file(csv_path)

    total_broken = -1
    total_working = -1
    total_layers = -1

    with open(count_csv_file) as csvfile:
        reader = csv.DictReader(csvfile,delimiter='@')
        for row in reader:
            if row['workspace_name'] == "total":
                total_working = int(row['working_layers_count'])
                total_broken = int(row['broken_layers_count'])
                total_layers = total_working + total_broken
    if total_broken ==0:
        status = 0 
    elif 0 < total_broken < 6:
        status = 1
    else:
        status = 3
    status_string = "total layers: {0}, broken layers: {1}".format(total_working+total_broken, total_broken)
    print("{0} {1} invalid_layers={2};1;5; {3}".format(status, "Monitor-LayerIntegrity-GeoServer", total_broken, status_string))