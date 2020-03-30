import argparse
from netcup_api.dns import Client
from netcup_api.dns import DNSRecord


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action='store', type=str, help='api key to access netcup dns api',
                        required=True)
    parser.add_argument('--password', action='store', type=str, help='api password to access netcup dns api',
                        required=True)
    parser.add_argument('--customernumber', action='store', type=str, help='netcup customer number',
                        required=True)
    parser.add_argument('--domain', action='store', type=str, help='domain to issue wildcard certificate for',
                        required=True)
    parser.add_argument('--certbot_validation', action='store', type=str, help='let´s encrypt challenge nonce',
                        required=True)
    parser.add_argument('--cleanup', action='store_true', help='deletes the previously created acme challenge record')

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
