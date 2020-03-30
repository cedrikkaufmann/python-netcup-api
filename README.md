# Python Netcup API Client
This client can be used to access the Netcup API. 

## Features
- Add new DNS records
- Update existing DNS records
- Delete existing DNS records
- Script to update ACME challenge for Let´s encrypt certificates

## Usage
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