import argparse
from pprint import pprint

from telegram.client import Telegram

import utils


def main():
    utils.setup_logging()

    parser = argparse.ArgumentParser()
    utils.add_api_args(parser)
    utils.add_proxy_args(parser)
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key='changeme1234',
        proxy_server=args.proxy_server,
        proxy_port=args.proxy_port,
        proxy_type=utils.parse_proxy_type(args)
    )
    # you must call login method before others
    tg.login()

    result = tg.get_me()
    result.wait()
    pprint(result.update)


if __name__ == '__main__':
    main()
