import argparse
from netcup_api.dns import Client
from netcup_api.dns import DNSRecord


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action='store', type=str, help='API-Key to access Netcup DNS API', required=True)
    parser.add_argument('--password', action='store', type=str, help='API-Password to access Netcup DNS API',
                        required=True)
    parser.add_argument('--customernumber', action='store', type=str, help='Netcup customer number', required=True)
    parser.add_argument('--domain', action='store', type=str, help='Domain to issue wildcard certificate for',
                        required=True)
    parser.add_argument('--certbot_validation', action='store', type=str, help='Let´s encrypt challenge', required=True)
    parser.add_argument('--cleanup', action='store_true')

    args = parser.parse_args()

    acme_challenge = '_acme-challenge'

    client = Client(args.key, args.password, args.customernumber)

    if args.cleanup:
        records = client.get_dns_records(args.domain)

        for r in records:
            if r.hostname == acme_challenge:
                client.delete_dns_records(args.domain, r)
                break

    else:
        challenge_record = DNSRecord(
            hostname=acme_challenge, record_type='TXT', destination=args.certbot_validation
        )

        client.add_dns_records(args.domain, challenge_record)


if __name__ == '__main__':
    main()
