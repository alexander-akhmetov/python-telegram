import logging
import argparse

from telegram.client import Telegram

from utils import setup_logging


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
    )
    # you must call login method before others
    tg.login()

    result = tg.get_web_page_instant_view(url=args.url)

    result.wait()
    if result.error:
        print(f'error: {result.error_info}')
    else:
        print(f'Instant view: {result.update}')
