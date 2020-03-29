#!venv/bin/python

import argparse
from netcup_api.dns import Client


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action='store', type=str, help='API-Key to access Netcup DNS API', required=True)
    parser.add_argument('--password', action='store', type=str, help='API-Password to access Netcup DNS API',
                        required=True)
    parser.add_argument('--customernumber', action='store', type=str, help='Netcup customer number', required=True)
    parser.add_argument('--challenge', action='store', type=str, help='Let´s encrypt challenge', required=True)
    parser.add_argument('--domain', action='store', type=str, help='Domain name which should be accessed',
                        required=True)

    args = parser.parse_args()

    client = Client(args.key, args.password, args.customernumber)
    records = client.get_dns_records(args.domain)

    for r in records:
        if r.hostname == '_acme-challenge':
            r.destination = args.challenge
            client.update_dns_records(args.domain, r)
            break


if __name__ == '__main__':
    main()
