import os
import sys
import json
import argparse
import configparser
from .api import BinaryEdge, BinaryEdgeException


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
        '--torrent', '-t', action='store_true',
        help='Request torrents identified for an IP'
    )
    parser_b.set_defaults(which='ip')
    parser_c = subparsers.add_parser('search', help='Search in the database')
    parser_c.add_argument('SEARCH', help='Search request')
    parser_c.add_argument(
        '--image', '-i', action='store_true',
        help='Requests images identified for an IP'
    )
    parser_c.set_defaults(which='search')
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
                    else:
                        res = be.host(args.IP)
                    print(json.dumps(res, sort_keys=True, indent=4))
                elif args.which == 'search':
                    if args.image:
                        res = be.image_search(args.SEARCH)
                    else:
                        res = be.host_search(args.SEARCH)
                    print(json.dumps(res, sort_keys=True, indent=4))
                else:
                    parser.print_help()
            except ValueError as e:
                print('Invalid Vaue: %s' % e.message)
            except BinaryEdgeException as e:
                print('Error: %s' % e.message)
    else:
        parser.print_help()
