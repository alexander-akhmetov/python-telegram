import argparse

from telegram.client import Telegram

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    parser.add_argument('api_hash', help='API hash')
    parser.add_argument('phone', help='Phone')
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key='changeme1234',
    )
    # you must call login method before others
    tg.login()

    result = tg.get_me()
    result.wait()
    print(result.update)
