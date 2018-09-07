#!/usr/bin/env python
"""validate_all_csw_records_geonetwork.py: requests all records in csw catalog and validates xml schema of these records, results are saved in csv file"""
import argparse
import sys
from sys import exit
from util import *
import csv
from util.csw_client import *
import os

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("gn_url", type=str, help="GeoNetwork url")
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    gn_url = args.gn_url
    csw_endpoint = "srv/dut/csw"
    csv_path = "csv"
    csw_url = "{0}/{1}".format(gn_url, csw_endpoint)
    log_results = []
    log_results.append(["record_id", "exception_message"])
    valid_count = 0 
    invalid_count = 0
    errorresult = []
    errorresult.append(["metadata_url", "validation_error"])

    gn_client = CSWClient("", "", csw_url)
    all_records = gn_client.get_all_records()
    count = 0 
    for record_id in all_records:
        count += 1
        record_xml = gn_client.get_record(record_id)
        
        if record_xml:
            validation_error = validate_xml(record_xml)
        else:
            validation_error = "metadata record empty"

        if validation_error:
            invalid_count += 1
            errorresult.append([gn_client.get_record_url(record_id),validation_error])
        else:
            valid_count += 1
        #if count>50:
        #    break

    counts = []
    counts.append(["valid","invalid","total"])
    counts.append([valid_count, invalid_count, valid_count+invalid_count])

    count_csv_name = "csw_validator_count.csv"
    errors_csv_name = "csw_validator_errors.csv"

    count_csv_file = os.path.join(csv_path, count_csv_name)
    errors_csv_file = os.path.join(csv_path, errors_csv_name)
    remove_file(count_csv_file)
    remove_file(errors_csv_file)

    with open(count_csv_file, "w") as file:
        writer = csv.writer(file)
        writer.writerows(counts)

    with open(errors_csv_file, "w") as file:
        writer = csv.writer(file)
        writer.writerows(errorresult)

# call script with url "validate_all_csw_records_geonetwork.py http://localhost/geonetwork
if __name__ == "__main__":
    main(sys.argv[1:])















