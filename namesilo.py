import xml.etree.cElementTree as ElementTree

import requests


NAMESILO_OPERATIONS = {
    'add_account_funds': 'addAccountFunds',
    'add_auto_renew': 'addAutoRenewal',
    'add_contact': 'contactAdd',
    'add_dns_record': 'dnsAddRecord',
    'add_email_forward': 'configureEmailForward',
    'add_portfolio': 'portfolioAdd',
    'add_privacy': 'addPrivacy',
    'add_registered_nameserver': 'addRegisteredNameServer',
    'associate_contact': 'contactDomainAssociate',
    'associate_portfolio': 'portfolioDomainAssociate',
    'change_nameservers': 'changeNameServers',
    'check_register_availability': 'checkRegisterAvailability',
    'check_transfer_availability': 'checkTransferAvailability',
    'check_transfer_status': 'checkTransferStatus',
    'delete_dns_record': 'dnsUpdateRecord',
    'delete_portfolio': 'portfolioDelete',
    'delete_registered_nameserver': 'deleteRegisteredNameServer',
    'forward_domain': 'domainForward',
    'get_account_balance': 'getAccountBalance',
    'get_auth_code': 'retrieveAuthCode',
    'get_domain_info': 'getDomainInfo',
    'list_contacts': 'contactList',
    'list_dns_records': 'dnsListRecords',
    'list_domains': 'listDomains',
    'list_email_forwards': 'listEmailForwards',
    'list_portfolios': 'portfolioList',
    'list_registered_nameservers': 'listRegisteredNameServers',
    'lock_domain': 'domainLock',
    'register_domain': 'registerDomain',
    'renew_domain': 'renewDomain',
    'remove_auto_renewal': 'removeAutoRenewal',
    'remove_email_forward': 'deleteEmailForward',
    'remove_privacy': 'removePrivacy',
    'transfer_domain': 'ransferDomain',
    'unlock_domain': 'domainUnlock',
    'update_contact': 'contactUpdate',
    'update_dns_record': 'dnsUpdateRecord',
    'update_portfolio': 'portfoliopdate',
    'update_registered_nameserver': 'modifyRegisteredNameServer',
    'update_registered_nameserver': 'updateRegisteredNameServer'
}


class NameSiloError(Exception):
    pass


class NameSilo(object):
    LIVE_BASE_URL = ' https://www.namesilo.com/api/'
    SANDBOX_BASE_URL = 'http://sandbox.namesilo.com/api/'

    VERSION = '1'
    RESPONSE_TYPE = 'xml'

    def __init__(self, api_key, live=False):
        self.api_key = api_key
        self.base_url = self.LIVE_BASE_URL if live else self.SANDBOX_BASE_URL

    def __getattr__(self, name):
        if name in NAMESILO_OPERATIONS:
            def request_handler(**kwargs):
                return self.request(name, **kwargs)
            return request_handler
        return super(NameSilo, self).__getattr__(name)

    def request(self, operation, **kwargs):
        operation = NAMESILO_OPERATIONS.get(operation, operation)
        kwargs.update(version=self.VERSION, type=self.RESPONSE_TYPE,
                      key=self.api_key)
        r = requests.get(self.base_url + operation, params=kwargs)
        r.raise_for_status()
        root = ElementTree.XML(r.text)
        response = XmlDictConfig(root)
        reply = response.get('reply')
        reply = self.format_reply(reply)
        return reply

    def format_reply(self, reply):
        for k, v in reply.iteritems():
            if isinstance(v, dict):
                reply[k] = self.format_reply(v)
            elif not isinstance(v, list):
                if v.lower() == 'yes':
                    reply[k] = True
                elif v.lower() == 'no':
                    reply[k] = False
                elif v.lower() == 'n/a':
                    reply[k] = None
        return reply


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
