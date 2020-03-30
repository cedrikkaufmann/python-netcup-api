# Python Netcup API Client
This client can be used to access the Netcup API. 

## Features
- Add new DNS records
- Update existing DNS records
- Delete existing DNS records
- Script to update ACME challenge for Let´s encrypt certificates

## API Client Usage
First let´s create a new api client:
```
# import the api client
from netcup_api.dns import Client

# create new instance and login using your credentials (api key, api password and customer number)
c = Client('apikey', 'apipassword', '12345')
```

If we want to create a new acme challenge entry for lets encrypt:
```
from netcup_api.dns import DNSRecord
acmeRecord = DNSRecord(hostname='_acme-challenge', record_type='TXT', destination='nonce')
client.add_dns_record('mydomain.tld', acmeRecord)
```

Now we update the previously created dns record, but first we want to fetch the records:
```
records = client.get_dns_records('mydomain.tld')

# look for the acme record
for r in records:
    if r.hostname == '_acme-challenge':
        # update value
        r.destination = 'another_nonce'
        # write updated record
        client.update_dns_records('mydomain.tld', r)
```

Next we delete the let´s encrypt challenge record:
```
records = client.get_dns_records('mydomain.tld')

# look for the acme record
for r in records:
    if r.hostname == '_acme-challenge':
        client.delete_dns_records('mydomain.tld', r)
```

If the client instance is destroyed it logs-out automatically.

## Let´s Encrypt Challenge Client Usage
```
usage: letsencrypt_acme_challenge_client.py [-h] --key KEY --password PASSWORD --customernumber CUSTOMERNUMBER --domain DOMAIN --certbot_validation CERTBOT_VALIDATION [--cleanup]

optional arguments:
  -h, --help            show this help message and exit
  --key KEY             api key to access netcup dns api
  --password PASSWORD   api password to access netcup dns api
  --customernumber CUSTOMERNUMBER
                        netcup customer number
  --domain DOMAIN       domain to issue wildcard certificate for
  --certbot_validation CERTBOT_VALIDATION
                        let´s encrypt challenge nonce
  --cleanup             deletes the previously created acme challenge record
```

## Dependencies
- requests

## License 
MIT licensed 2020 Cedrik Kaufmann. See the LICENSE file for further details.