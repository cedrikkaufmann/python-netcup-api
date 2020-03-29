import requests


class DNSRecord:

    def __init__(self, hostname, record_type, destination, priority=None, domain_id=None, delete_record=False):
        self._hostname = hostname
        self._record_type = record_type
        self._domain_id = domain_id
        self._destination = destination
        self._priority = priority
        self._delete_record = delete_record

    def get_host(self):
        return self._hostname

    def set_host(self, hostname):
        self._hostname = hostname

    hostname = property(get_host, set_host)

    def get_record_type(self):
        return self._record_type

    def set_record_type(self, record_type):
        self._record_type = record_type

    record_type = property(get_record_type, set_record_type)

    def get_destination(self):
        return self._destination

    def set_destination(self, destination):
        self._destination = destination

    destination = property(get_destination, set_destination)

    def get_delete_record(self):
        return self._delete_record

    def set_delete_record(self, delete):
        self._delete_record = delete

    delete = property(get_delete_record, set_delete_record)

    def get_domain_id(self):
        return self._domain_id

    def set_domain_id(self, domain_id):
        self._domain_id = domain_id

    domain_id = property(get_domain_id, set_domain_id)

    def get_priority(self):
        return self._priority

    def set_priority(self, priority):
        self._priority = priority

    priority = property(get_priority, set_priority)

    def json(self):
        return {
            'id': self._domain_id,
            'hostname': self._hostname,
            'type': self._record_type,
            'priority': self._priority,
            'destination': self._destination,
            'deleterecord': self._delete_record
        }


class Client:
    REST_URI = 'https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON'

    def __init__(self, apiKey, apiPassword, customerNumber):
        self._apiKey = apiKey
        self._apiPassword = apiPassword
        self._customerNumber = customerNumber
        self._sessionID = ''
        self._login()

    def __del__(self):
        self._logout()

    def _login(self):
        payload = {
            'action': 'login',
            'param': {
                'apikey': self._apiKey,
                'apipassword': self._apiPassword,
                'customernumber': self._customerNumber
            }
        }

        r = requests.post(url=Client.REST_URI, json=payload)

        if r.json()['status'] != 'success':
            raise Exception(r.json()['shortmessage'], r.json()['longmessage'], payload)

        self._sessionID = r.json()['responsedata']['apisessionid']

    def _logout(self):
        payload = {
            'action': 'logout',
            'param': {
                'apikey': self._apiKey,
                'apisessionid': self._sessionID,
                'customernumber': self._customerNumber
            }
        }

        r = requests.post(url=Client.REST_URI, json=payload)

        if r.json()['status'] != 'success':
            raise Exception(r.json()['shortmessage'], r.json()['longmessage'], payload)

    def get_dns_records(self, domainname):
        payload = {
            "action": "infoDnsRecords",
            "param": {
                "domainname": domainname,
                "apikey": self._apiKey,
                "apisessionid": self._sessionID,
                "customernumber": self._customerNumber
            }
        }

        r = requests.post(url=Client.REST_URI, json=payload)

        if r.json()['status'] != 'success':
            raise Exception(r.json()['shortmessage'], r.json()['longmessage'], payload)

        dns_records_raw = r.json()['responsedata']['dnsrecords']
        dns_records = list()

        for record in dns_records_raw:
            dns_records.append(DNSRecord(domain_id=record['id'], hostname=record['hostname'],
                                         record_type=record['type'], destination=record['destination']))

        return dns_records

    def update_dns_records(self, domainname, *records):
        payload = {
            "action": "updateDnsRecords",
            "param": {
                "domainname": domainname,
                "apikey": self._apiKey,
                "apisessionid": self._sessionID,
                "customernumber": self._customerNumber,
                "dnsrecordset": {
                    "dnsrecords": []
                }
            }
        }

        for record in records:
            payload['param']['dnsrecordset']['dnsrecords'].append(record.json())

        r = requests.post(url=Client.REST_URI, json=payload)

        if r.json()['status'] != 'success':
            raise Exception(r.json()['shortmessage'], r.json()['longmessage'], payload)

    def delete_dns_records(self, domainname, *records):
        payload = {
            "action": "updateDnsRecords",
            "param": {
                "domainname": domainname,
                "apikey": self._apiKey,
                "apisessionid": self._sessionID,
                "customernumber": self._customerNumber,
                "dnsrecordset": {
                    "dnsrecords": []
                }
            }
        }

        for record in records:
            record.delete = True
            payload['param']['dnsrecordset']['dnsrecords'].append(record.json())

        r = requests.post(url=Client.REST_URI, json=payload)

        if r.json()['status'] != 'success':
            raise Exception(r.json()['shortmessage'], r.json()['longmessage'], payload)

    def add_dns_records(self, domainname, *records):
        payload = {
            "action": "updateDnsRecords",
            "param": {
                "domainname": domainname,
                "apikey": self._apiKey,
                "apisessionid": self._sessionID,
                "customernumber": self._customerNumber,
                "dnsrecordset": {
                    "dnsrecords": []
                }
            }
        }

        for record in records:
            payload['param']['dnsrecordset']['dnsrecords'].append(record.json())

        r = requests.post(url=Client.REST_URI, json=payload)

        if r.json()['status'] != 'success':
            raise Exception(r.json()['shortmessage'], r.json()['longmessage'], payload)
