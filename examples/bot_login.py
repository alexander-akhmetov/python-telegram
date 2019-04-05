import argparse

from telegram.client import Telegram


def bot_get_me(api_id, api_hash, token):
    tg = Telegram(
        api_id=api_id,
        api_hash=api_hash,
        bot_token=token,
        database_encryption_key='changeme1234',
    )
    # you must call login method before others
    tg.login()

    result = tg.get_me()
    result.wait()
    print(result.update)
    tg.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    parser.add_argument('api_hash', help='API hash')
    parser.add_argument('token', help='Bot token')
    args = parser.parse_args()
    bot_get_me(args.api_id, args.api_hash, args.token)
