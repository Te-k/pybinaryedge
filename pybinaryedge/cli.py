import os
import sys
import json
import argparse
import configparser
from .api import BinaryEdge, BinaryEdgeException, BinaryEdgeNotFound


def main():
    parser = argparse.ArgumentParser(description='Request BinaryEdge API')
    subparsers = parser.add_subparsers(help='Commands')
    parser_a = subparsers.add_parser('config', help='Configure pybinary edge')
    parser_a.add_argument('--key', '-k', help='Configure the API key')
    parser_a.set_defaults(which='config')
    parser_b = subparsers.add_parser('ip', help='Query an IP address')
    parser_b.add_argument('IP', help='IP to be requested')
    parser_b.add_argument(
        '--historical', '-H', action='store_true',
        help='Requests historical data about an IP'
    )
    parser_b.add_argument(
        '--score', '-s', action='store_true',
        help='Requests vulnerability score about an IP'
    )
    parser_b.add_argument(
        '--image', '-i', action='store_true',
        help='Requests images identified for an IP'
    )
    parser_b.add_argument(
        '--dns', '-d', action='store_true',
        help='Requests images identified for an IP'
    )
    parser_b.add_argument(
        '--torrent', '-t', action='store_true',
        help='Request torrents identified for an IP'
    )
    parser_b.add_argument('--page', '-p', type=int, default=1,
            help='Get specific page')
    parser_b.set_defaults(which='ip')
    parser_c = subparsers.add_parser('search', help='Search in the database')
    parser_c.add_argument('SEARCH', help='Search request')
    parser_c.add_argument('--page', '-p', type=int, default=1,
            help='Get specific page')
    parser_c.add_argument(
        '--image', '-i', action='store_true',
        help='Requests images identified for an IP'
    )
    parser_c.set_defaults(which='search')
    parser_d = subparsers.add_parser('dataleaks', help='Search in the leaks database')
    parser_d.add_argument('EMAIL', help='Search email in the leaks database')
    parser_d.add_argument(
        '--domain', '-d', action='store_true',
        help='Search for domain instead of email'
    )
    parser_d.set_defaults(which='dataleaks')
    parser_e = subparsers.add_parser('domains', help='Search information on a domain')
    parser_e.add_argument('DOMAIN', help='Domain to be requested')
    parser_e.add_argument('--page', '-p', type=int, default=1,
            help='Get specific page')
    parser_e.add_argument(
        '--subdomains', '-s', action='store_true',
        help='Returns subdomains'
    )
    parser_e.add_argument(
        '--dns', '-d', action='store_true',
        help='Returns all dns entries for this domain'
    )
    parser_e.set_defaults(which='domain')
    args = parser.parse_args()

    configfile = os.path.expanduser('~/.config/binaryedge')

    if hasattr(args, 'which'):
        if args.which == 'config':
            if args.key:
                config = configparser.ConfigParser()
                config['BinaryEdge'] = {'key': args.key}
                with open(configfile, 'w') as cf:
                    config.write(cf)
            if os.path.isfile(configfile):
                print('In %s:' % configfile)
                with open(configfile, 'r') as cf:
                    print(cf.read())
            else:
                print('No configuration file, please use config --key')
        else:
            if not os.path.isfile(configfile):
                print('No configuration file, please use config --key')
                sys.exit(1)
            config = configparser.ConfigParser()
            config.read(configfile)
            try:
                be = BinaryEdge(config['BinaryEdge']['key'])
                if args.which == 'ip':
                    if args.score:
                        res = be.host_score(args.IP)
                    elif args.image:
                        res = be.image_ip(args.IP)
                    elif args.torrent:
                        if args.historical:
                            res = be.torrent_historical_ip(args.IP)
                        else:
                            res = be.torrent_ip(args.IP)
                    elif args.historical:
                        res = be.host_historical(args.IP)
                    elif args.dns:
                        res = be.domain_ip(args.IP, page=args.page)
                    else:
                        res = be.host(args.IP)
                    print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'search':
                    if args.image:
                        res = be.image_search(args.SEARCH, page=args.page)
                    else:
                        res = be.host_search(args.SEARCH, page=args.page)
                    print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'dataleaks':
                    if args.domain:
                        res = be.dataleaks_organization(args.EMAIL)
                    else:
                        res = be.dataleaks_email(args.EMAIL)
                    print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'domain':
                    if args.subdomains:
                        res = be.domain_subdomains(args.DOMAIN, page=args.page)
                    else:
                        res = be.domain_dns(args.DOMAIN, page=args.page)
                    print(json.dumps(res, sort_keys=True, indent=4))
                else:
                    parser.print_help()
            except ValueError as e:
                print('Invalid Value: %s' % e.message)
            except BinaryEdgeNotFound as e:
                print('Search term not found')
            except BinaryEdgeException as e:
                print('Error: %s' % e.message)
    else:
        parser.print_help()
