import sys
import logging
import argparse

from telegram.proxy import SOCKS5Proxy, MTProtoProxy, HTTPProxy


def setup_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def add_api_args(parser: argparse.ArgumentParser):
    parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    parser.add_argument('api_hash', help='API hash')
    parser.add_argument('phone', help='Phone')


def add_proxy_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--proxy_server', help='Proxy server', default='', required=False
    )
    parser.add_argument('--proxy_port', help='Proxy port', default='', required=False)
    parser.add_argument(
        '--proxy_type',
        help='Proxy type (socks5, http, mtproxy)',
        default='',
        required=False,
    )
    parser.add_argument(
        '--proxy_username', help='Proxy user name', default='', required=False
    )
    parser.add_argument(
        '--proxy_password', help='Proxy password', default='', required=False
    )
    parser.add_argument(
        '--proxy_secret', help='Proxy secret (mtproxy)', default='', required=False
    )


def parse_proxy_type(args):
    if not args.proxy_type:
        return None

    default = {
        'host': args.proxy_server,
        'port': args.proxy_port,
    }
    if args.proxy_type == 'socks5':
        proxy = SOCKS5Proxy(
            **default, username=args.proxy_username, password=args.proxy_password
        )
    elif args.proxy_type == 'http':
        proxy = HTTPProxy(
            **default, username=args.proxy_username, password=args.proxy_password
        )
    elif args.proxy_type in ('mtproxy', 'mtproto'):
        proxy = MTProtoProxy(**default, secret=args.proxy_secret)
    else:
        raise ValueError('Invalid proxy type: %s')

    return proxy
