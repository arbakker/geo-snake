#!/usr/bin/python
import os
import re

base_dir = "/usr/local/apache-tomcat-8.0.33/webapps/"
geoserver_dir = "geoserver_2.13"
manifest_name = "MANIFEST.MF"

full_path = os.path.join(base_dir, geoserver_dir)
manifest_path = os.path.join(full_path, manifest_name)

gs_version = ""

with open(manifest_path) as f:
    for line in f:
        version_search = re.search('Project-Version:\s(.*)', line, re.IGNORECASE)
        if version_search:
            gs_version = version_search.group(1)

print(gs_version)