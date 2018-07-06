# README

Python scripts for performing various on GeoServer and/or GeoNetwork. Some examples:

- perform schema validation of all metadata in CSW catalogue (validate_all_csw_records_geonetwork)
- test whether all WMS layers in GeoServer are working (check_wms_layers_geoserver)
- create GeoWebCache layer in GeoServer based on WMS service (create_gwc_seed_job_geoserver)
- create vector layer in GeoServer based on existing datastore (create_vector_layer_geoserver)
- remove all layers from a workspace in GeoServer (remove_all_layers_workspace_geoserver)

CSV output of script is saved in the `csv` directory, this is not yet configurable. 

Execute `script -h` or `script --help` for help.

Compatible with python 2 and 3.

TODO: add requirements.txt file.
