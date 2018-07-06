from util import *
from lxml import etree, objectify
import xml.etree.ElementTree as ET
from urllib import parse

class CSWClient:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.ns = {"csw":"http://www.opengis.net/cat/csw/2.0.2", "gmd":"http://www.isotc211.org/2005/gmd", "dc":"http://purl.org/dc/elements/1.1/"}

    def get_search_result(self, xml):
        root = etree.fromstring(xml)
        search_result = root.find(".//csw:SearchResults", self.ns)
        return search_result

    def get_total_records(self, search_result):
        total_records = search_result.attrib['numberOfRecordsMatched']
        if total_records:
            return int(total_records)
        else:
            raise Exception("Could not find SearchResults@numberOfRecordsMatched in CSW GetRecords response")

    def get_next_record(self, search_result):
        next_record = search_result.attrib['nextRecord']
        if next_record:
            return int(next_record)
        else:
            raise Exception("Could not find SearchResults@nextRecord in CSW GetRecords response")

    def get_records_returned(self, search_result):
        records_returned = search_result.attrib['numberOfRecordsReturned']
        if records_returned:
            return int(records_returned)
        else:
            raise Exception("Could not find SearchResults@numberOfRecordsReturned in CSW GetRecords response")

    def get_record_identifiers(self, xml):
        root = etree.fromstring(xml)
        records = root.findall(".//dc:identifier", self.ns)
        result =  [record.text for record in records]
        return result

    def get_record_url(self, record_id):
        get_record_url = "{0}?request=GetRecordById&service=CSW&version=2.0.2&outputFormat=application/xml&outputSchema=http://www.isotc211.org/2005/gmd&id={1}".format(self.url, record_id)
        return get_record_url

    def recource_exists(self, resource_url):
        return exists_resource(resource_url, self.username, self.password)

    def get_record(self,record_id):
        get_record_url = self.get_record_url(record_id)
        record_xml = get_resource_bytes(get_record_url)
        #remove csw getrecord envelop from XML
        root = etree.fromstring(record_xml)
        xml_md = root.find('.//gmd:MD_Metadata', self.ns)
        xml_md_str = etree.tostring(xml_md, pretty_print=True)
        return xml_md_str

    def get_all_records(self):
        first_url = "{0}?request=GetRecords&service=CSW&record=0&version=2.0.2&resultType=results".format(self.url)
        first_xml = get_resource_bytes(first_url)
        search_result = self.get_search_result(first_xml)
        next_record = self.get_next_record(search_result)
        total_records = self.get_total_records(search_result)
        records_returned = self.get_records_returned(search_result)
        all_records = []
        records = self.get_record_identifiers(first_xml)
        all_records.extend(records)

        if total_records > records_returned:
            i = 0
            while True:
                results_url = first_url + "&startPosition={0}".format(next_record) 
                results_xml = get_resource_bytes(results_url)
                search_result = self.get_search_result(results_xml)
                next_record = self.get_next_record(search_result)
                records = self.get_record_identifiers(results_xml)
                if len(records) == 0:
                    break
                else:
                    all_records.extend(records)
                #print("total number of records collected: {0}".format(len(all_records)))
                i += 1
        return all_records
