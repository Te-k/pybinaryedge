import argparse
import configparser
import json
import os
import sys
from typing import Dict, Any

from .api import BinaryEdge, BinaryEdgeException, BinaryEdgeNotFound


def process_args(client: BinaryEdge, args) -> Dict[str, Any]:
    res = None
    if args.which == 'ip':
        if args.score:
            res = client.host_score(args.IP)
        elif args.image:
            res = client.image_ip(args.IP)
        elif args.torrent:
            if args.historical:
                res = client.torrent_historical_ip(args.IP)
            else:
                res = client.torrent_ip(args.IP)
        elif args.historical:
            res = client.host_historical(args.IP)
        elif args.dns:
            res = client.domain_ip(args.IP, page=args.page)
        else:
            res = client.host(args.IP)
    elif args.which == 'search':
        if args.image:
            res = client.image_search(args.SEARCH, page=args.page)
        elif args.domains:
            res = client.domain_search(args.SEARCH, page=args.page)
        else:
            res = client.host_search(args.SEARCH, page=args.page)
    elif args.which == 'dataleaks':
        if args.domain:
            res = client.dataleaks_organization(args.EMAIL)
        else:
            res = client.dataleaks_email(args.EMAIL)
    elif args.which == 'domain':
        if args.subdomains:
            res = client.domain_subdomains(args.DOMAIN, page=args.page)
        else:
            res = client.domain_dns(args.DOMAIN, page=args.page)
    return res


def main():
    parser = argparse.ArgumentParser(description='Request BinaryEdge API')
    parser.add_argument(
        '--no-verify', action='store_false',
        help='Disable SSL verification'
    )
    parser.add_argument(
        '--pages', type=int, default=-2,
        help='Enables pagination until the supplied page'
    )
    parser.add_argument(
        '--no-pretty', action='store_false', help='Non-prettified output'
    )
    subparsers = parser.add_subparsers(help='Commands')
    parser_a = subparsers.add_parser('config',
                                     help='Configure pybinary edge')
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
    parser_b.add_argument(
        '--page', '-p', type=int, default=1,
        help='Get specific page'
    )
    parser_b.set_defaults(which='ip')
    parser_c = subparsers.add_parser('search', help='Search in the database')
    parser_c.add_argument('SEARCH', help='Search request')
    parser_c.add_argument(
        '--page', '-p', type=int, default=1,
        help='Get specific page'
    )
    parser_c.add_argument(
        '--image', '-i', action='store_true',
        help='Search for screenshots and details extracted based on a query'
    )
    parser_c.add_argument(
        '--domains', '-d', action='store_true',
        help='Search for Domains/DNS data based on a query.'
    )
    parser_c.set_defaults(which='search')
    parser_d = subparsers.add_parser(
        'dataleaks',
        help='Search in the leaks database'
    )
    parser_d.add_argument('EMAIL', help='Search email in the leaks database')
    parser_d.add_argument(
        '--domain', '-d', action='store_true',
        help='Search for domain instead of email'
    )
    parser_d.set_defaults(which='dataleaks')
    parser_e = subparsers.add_parser(
        'domains',
        help='Search information on a domain'
    )
    parser_e.add_argument('DOMAIN', help='Domain to be requested')
    parser_e.add_argument(
        '--page', '-p', type=int, default=1,
        help='Get specific page'
    )
    parser_e.add_argument(
        '--subdomains', '-s', action='store_true',
        help='Returns subdomains'
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
                be = BinaryEdge(
                    config['BinaryEdge']['key'],
                    args.no_verify
                )
                jsonArgs = {'sort_keys': True, 'indent': 4} if args.no_pretty else {}
                if args.which in ['ip', 'search', 'dataleaks', 'domains']:
                    page = 1
                    if args.page and args.pages != -2:
                        page = args.pages
                    for current_page in range(0, page):
                        if hasattr(args, 'page'):
                            args.page = current_page + 1
                        res = process_args(client=be, args=args)
                        if len(res['events']) == 0:
                            break
                        print(json.dumps(res, **jsonArgs))
                        if 'pagesize' not in res:
                            break
                        if 'events' not in res:
                            break

                else:
                    parser.print_help()
            except ValueError as e:
                print('Invalid Value: %s' % e.message)
            except BinaryEdgeNotFound:
                print('Search term not found')
            except BinaryEdgeException as e:
                print('Error: %s' % e.message)
    else:
        parser.print_help()
