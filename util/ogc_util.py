import requests
import os
from lxml import etree, objectify
from lxml.etree import XMLParser, XMLSchema, parse, XMLSyntaxError, XML


requests.packages.urllib3.disable_warnings()
#required due to bug, see for more https://stackoverflow.com/a/33513324
#http.client.HTTPConnection._http_vsn = 10
#http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

def exists_resource(url, username, password):
    response = requests.get(url,
                        auth=requests.auth.HTTPBasicAuth(
                          username,
                          password))
    if (response.status_code==200):
            return True
    return False

def get_resource_bytes(url, username="", password=""):
    headers = {'accept': 'application/xml'}

    if not username and not password:
        response = requests.get(url,
                    headers=headers)
    else:
        response = requests.get(url,
                    auth=requests.auth.HTTPBasicAuth(
                      username,
                      password),
                    headers=headers)
    return response.content


def get_resource(url, username="", password=""):
    headers = {'accept': 'application/xml'}

    if not username and not password:
        response = requests.get(url,
                    headers=headers)
    else:
        response = requests.get(url,
                    auth=requests.auth.HTTPBasicAuth(
                      username,
                      password),
                    headers=headers)
    return response.text

def get_resource_response(url, username, password, headers):
    response = requests.get(url, auth=requests.auth.HTTPBasicAuth(
        username,password), headers=headers)
    return response
    
def create_resource_put(url, username, password, payload):
    headers = {'content-type': 'application/xml'}
    response = requests.put(url,
                        data=payload,
                        auth=requests.auth.HTTPBasicAuth(
                          username,
                          password),
                        headers=headers)
    if (response.status_code==200):
            return True
    return False

def delete_resource(url, username, password):
    response = requests.delete(url,
                        auth=requests.auth.HTTPBasicAuth(
                          username,
                          password))
    #print("response status_code:" + str(response.status_code))
    if (response.status_code==200):
            return True
    return False


def create_resource(url, username, password, payload, headers):
    #headers = {'content-type': 'application/xml'}
    response = requests.post(url,
                        data=payload,
                        auth=requests.auth.HTTPBasicAuth(
                          username,
                          password),
                        headers=headers)
    if (response.status_code==201):
            return True
    return False

def remove_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

def validate_xml(xml):
    schema_path = "schema/gmd/gmd.xsd"
    result = ""
    with open(schema_path, 'rb') as xml_schema_file:
         schema_doc = etree.XML(xml_schema_file.read(), base_url=schema_path)
         schema = etree.XMLSchema(schema_doc)
         parser = XMLParser(schema=schema)
         xml = XML(xml)
         if not schema.validate(xml):
             for error in schema.error_log:
                  result += "error: {0}, line: {1}, column {2}".format(error.message, error.line, error.column)
    return result

