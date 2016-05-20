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
    """Base class for NameSilo errors."""
    pass


class HTTPSNotUsed(NameSiloError):
    """Raised if request is made without HTTPS."""
    pass


class NoVersionSpecified(NameSiloError):
    """Raised if no version is specified in the request."""
    pass


class InvalidAPIVersion(NameSiloError):
    """Raised if the ApI version specified is invalid."""
    pass


class NoTypeSpecified(NameSiloError):
    """Raised if no type is specified in request."""
    pass


class InvalidAPIType(NameSiloError):
    """Raised if API type is invalid."""
    pass


class NoOperationSpecified(NameSiloError):
    """Raised if no operation is specified in request."""
    pass


class issingAPIParameters(NameSiloError):
    """Raised if there are missing parameters for the specified operation."""
    pass


class InvalidAPIOperation(NameSiloError):
    """Raised if the API operaiton is invalid."""
    pass


class MissingOperationParameters(NameSiloError):
    """Raised if parameters are missing from the API operation."""
    pass


class NoAPIKeySpecified(NameSiloError):
    """Raised if no API key is specified for request."""
    pass


class InvalidAPIKey(NameSiloError):
    """Raised if the API key is invalid."""
    pass


class InvalidUser(NameSiloError):
    """Raised if user associatedwith API key is invalid."""
    pass


class APINotAvailableToSubAccounts(NameSiloError):
    pass


class invalidIPAddress(NameSiloError):
    pass


class InvalidDomainSyntax(NameSiloError):
    pass


class CentralRegistryNotResponding(NameSiloError):
    pass


class InvalidSandboxAccount(NameSiloError):
    pass


class CreditCardProfileDoesNotExist(NameSiloError):
    pass


class UnverifiedCreditCardProfile(NameSiloError):
    pass


class InsufficientAccountFunds(NameSiloError):
    pass


class ApIKeyNotPassedasGet(NameSiloError):
    pass


class DomainNotActive(NameSiloError):
    pass


class InteralSystemError(NameSiloError):
    pass


class DomainAlreadyAutoRenew(NameSiloError):
    pass


class DomainAlreadyNotAutoReview(NameSiloError):
    pass


class DomainAlreadyLocked(NameSiloError):
    pass


class DomainAlreadyUnlocked(NameSiloError):
    pass


class NameserverUpdateError(NameSiloError):
    pass


class DomainAlreadyPrivate(NameSiloError):
    pass


class DomainAlreadyNotPrivate(NameSiloError):
    pass


class ProcessingError(NameSiloError):
    pass


class DomainAlreadyActive(NameSiloError):
    pass


class InvalidNumberOfYears(NameSiloError):
    pass


class DomainRenewalError(NameSiloError):
    pass


class DomainTransferError(NameSiloError):
    pass


class DomainTransferDoesNotExist(NameSiloError):
    pass


class InvalidDomainName(NameSiloError):
    pass


class DNSModificationErrror(NameSiloError):
    pass


NAMESILO_ERRORS = { 
    '101': HTTPSNotUsed,
    '102': NoVersionSpecified,
    '103': InvalidAPIVersion,
    '104': NoTypeSpecified,
    '105': InvalidAPIType,
    '106': NoOperationSpecified,
    '107': InvalidAPIOperation,
    '108': MissingOperationParameters,
    '109': NoAPIKeySpecified,
    '110': InvalidAPIKey,
    '111': InvalidUser,
    '112': APINotAvailableToSubAccounts,
    '113': invalidIPAddress,
    '114': InvalidDomainSyntax,
    '115': CentralRegistryNotResponding,
    '116': InvalidSandboxAccount,
    '117': CreditCardProfileDoesNotExist,
    '118': UnverifiedCreditCardProfile,
    '119': InsufficientAccountFunds,
    '120': ApIKeyNotPassedasGet,
    '200': DomainNotActive,
    '201': InteralSystemError,
    '210': NameSiloError,
    '250': DomainAlreadyAutoRenew,
    '251': DomainAlreadyNotAutoReview,
    '252': DomainAlreadyLocked,
    '253': DomainAlreadyUnlocked,
    '254': NameserverUpdateError,
    '255': DomainAlreadyPrivate,
    '256': DomainAlreadyNotPrivate,
    '261': ProcessingError,
    '262': DomainAlreadyActive,
    '263': InvalidNumberOfYears,
    '264': DomainRenewalError,
    '265': DomainTransferError,
    '266': DomainTransferDoesNotExist,
    '267': InvalidDomainName,
    '280': DNSModificationErrror,
}


class NameSilo(object):
    LIVE_BASE_URL = 'https://www.namesilo.com/api/'
    SANDBOX_BASE_URL = 'http://sandbox.namesilo.com/api/'

    VERSION = '1'
    RESPONSE_TYPE = 'xml'

    def __init__(self, api_key, live=False):
        self.api_key = api_key
        self.base_url = self.LIVE_BASE_URL if live else self.SANDBOX_BASE_URL

    def __getattr__(self, name):
        if name in NAMESILO_OPERATIONS:
            def handle_request(**kwargs):
                return self.request(name, **kwargs)
            return handle_request
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
        self.handle_error(reply)
        return reply

    def handle_error(self, reply):
        code = reply.get('code')
        if code in NAMESILO_ERRORS:
            error = NAMESILO_ERRORS[code]
            raise error(reply.get('detail'))

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
