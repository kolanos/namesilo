import xml.etree.cElementTree as ElementTree

import requests


class NameSiloError(Exception):
    pass


class NameSilo(object):
    LIVE_BASE_URL = ' https://www.namesilo.com/api/'
    SANDBOX_BASE_URL = 'https://sandbox.namesilo.com/api/'

    VERSION = '1'
    RESPONSE_TYPE = 'xml'

    def __init__(self, api_key, live=False):
        self.api_key = api_key
        self.base_url = self.LIVE_BASE_URL if live else self.SANDBOX_BASE_URL

    def handle_request(self, operation, **kwargs):
        kwargs.update(version=self.VERSION, type=self.RESPONSE_TYPE,
                      key=self.api_key)
        r = requests.get(self.base_url + operation, params=kwargs)
        r.raise_for_status()
        root = ElementTree.XML(r.text)
        xmldict = XmlDictConfig(root)
        return xmldict.get('reply')

    def register_domain(self, **kwargs):
        return self.handle_request('registerDomain', **kwargs)

    def list_domains(self):
        return self.handle_request('listDomains')


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
