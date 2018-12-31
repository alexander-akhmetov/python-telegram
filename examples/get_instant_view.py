import logging
import argparse

from utils import setup_logging
from telegram.client import Telegram

"""
Prints short description of a webpage (using Telegram's instant view)

Usage:
    python examples/get_instant_view.py api_id api_hash phone https://hackernoon.com/im-harvesting-credit-card-numbers-and-passwords-from-your-site-here-s-how-9a8cb347c5b5
"""


if __name__ == '__main__':
    setup_logging(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    parser.add_argument('api_hash', help='API hash')
    parser.add_argument('phone', help='Phone')
    parser.add_argument('url', help='Webpage URL')
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key='changeme1234',
    )
    # you must call login method before others
    tg.login()

    # try this for example
    # https://hackernoon.com/im-harvesting-credit-card-numbers-and-passwords-from-your-site-here-s-how-9a8cb347c5b5
    result = tg.get_web_page_instant_view(
        url=args.url,
    )

    result.wait()
    if result.error:
        print(f'error: {result.error_info}')
    else:
        print('Instant view: ')
        short_text = result.update['page_blocks'][0]['title']['text']
        print(f'\n    {short_text}')
