
from lxml import etree, objectify
import xml.etree.ElementTree as ET
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
try:
    from ogc_util import *
except ImportError:
    from util.ogc_util import *

class GeoserverClient:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        if url.endswith("/"):
            url = url[:-1]
        self.url = url

    def get_workspace_url(self, workspace):
        return "{0}/rest/workspaces/{1}.xml".format(self.url, workspace)

    def get_workspaces_url(self):
        return "{0}/rest/workspaces.xml".format(self.url)

    def get_layer_url(self, workspace, layer):
        return "{0}/rest/layers/{1}:{2}.xml".format(self.url, workspace, layer)

    def get_features_in_datastore_url(self, workspace, datastore):
        return "{0}/rest/workspaces/{1}/datastores/{2}/featuretypes.xml".format(self.url, workspace, datastore)

    def get_feature_url(self, workspace, datastore, ft):
        return "{0}/rest/workspaces/{1}/datastores/{2}/featuretypes/{3}.xml".format(self.url, workspace, datastore, ft)

    def get_style_url(self, workspace, style_name):
        return "{0}/rest/workspaces/{1}/styles/{2}.xml".format(self.url, workspace, style_name)

    def get_new_style_url(self, workspace, style_name):
        return "{0}/rest/workspaces/{1}/styles.xml?name={2}".format(self.url, workspace, style_name)

    def list_layers(self, workspace):
        wms_url = "{0}/{1}/wms?request=getcapabilities".format(self.url, workspace)
        cap_xml = self.get_resource(wms_url)
        root = ET.fromstring(cap_xml)
        ns = {"wms":"http://www.opengis.net/wms"}
        layers = root.findall(".//wms:Layer", ns)
        layernames = []
        for layer in layers:
            layer_name_object = layer.find('wms:Name',ns)
            if layer_name_object is not None:
                layernames.append(layer_name_object.text)
        return layernames

    def list_workspaces(self):
        workspaces_url = self.get_workspaces_url()
        workspaces_xml = self.get_resource(workspaces_url)
        root = ET.fromstring(workspaces_xml)
        workspaces = root.findall('workspace')
        str_workspaces = [workspace.find('name').text for workspace in workspaces]
        return str_workspaces


    def get_featuretypeurl_by_layer(self, workspace, layer):
        # http://localhost:8000/geoserver_2.13/rest/layers/def_query:1.xml
        layer_url = "{0}/rest/layers/{1}:{2}.xml".format(self.url, workspace, layer)
        layer_xml = self.get_resource(layer_url)
        root = ET.fromstring(layer_xml)
        ns = {"atom":"http://www.w3.org/2005/Atom"}
        resource = root.find(".//resource/atom:link", ns)
        return resource.attrib['href']

    def get_wms_layers_in_workspace(self, workspace):
        wms_url = "{0}/{1}/wms?request=getcapabilities".format(self.url, workspace)
        cap_xml = self.get_resource(wms_url)
        root = ET.fromstring(cap_xml)
        ns = {"wms":"http://www.opengis.net/wms"}
        layers = root.findall(".//wms:Layer", ns)
        layernames = []
        for layer in layers:
            layer_name_object = layer.find('wms:Name',ns)
            if layer_name_object is not None:
                layernames.append(layer_name_object.text)
        return layernames

    def get_reflect_url(self, workspace, layer):
        return "{0}/wms/reflect?format=image/png&layers={1}:{2}&width=500".format(self.url, workspace, layer)

    def test_valid_wms_response(self, workspace, layer):
        reflect_url = self.get_reflect_url(workspace, layer)
        headers = {"Accept" : "image/png"}
        response = self.get_resource_response(reflect_url, headers)

        assert( response.status_code == 200 )
        
        error_message = ""

        if response.headers['content-type'] != "image/png":
            ns = {"ogc":"http://www.opengis.net/ogc"}
            root = ET.fromstring(response.text)
            service_exception = root.find(".//ogc:ServiceException", ns)
            if service_exception is not None:
                error_message = service_exception.text
        return error_message


    def get_metadataid_from_featuretype(self, feature_type_url):
        md_id = ""
        ft_xml = self.get_resource(feature_type_url)
        root = ET.fromstring(ft_xml)
        links = root.findall(".//metadataLinks/metadataLink")
        md_url = ""

        for link in links:
            md_type_el = link.find(".//metadataType")
            if md_type_el.text == "TC211":
                content_el = link.find(".//content")
                md_url = content_el.text
                break

        if md_url:
            url_dict = parse.parse_qs(parse.urlsplit(md_url).query)
            md_id = url_dict['id'][0]
        return md_id

    def get_resource_response(self, resource_url, headers):
        return get_resource_response(resource_url, self.username, self.password, headers)

    def get_resource(self, resource_url):
        return get_resource(resource_url, self.username, self.password)

    def create_resource(self, resource_url, data, headers):
        create_resource(resource_url, self.username, self.password, data, headers)

    def delete_gs_resource(self, resource_url):
        if self.exists_gs_resource(resource_url):
            delete_resource(resource_url, self.username, self.password)

    def exists_gs_resource(self, resource_url):
        return exists_resource(resource_url, self.username, self.password)






