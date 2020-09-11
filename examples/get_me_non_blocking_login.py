import argparse
import getpass
from pprint import pprint

from telegram.client import Telegram
from telegram.client import AuthorizationState

import utils


if __name__ == '__main__':
    utils.setup_logging()

    parser = argparse.ArgumentParser()
    utils.add_api_args(parser)
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key='changeme1234',
    )

    # you must call login method before others
    state = tg.login(blocking=False)

    print ("Checking the return state of the login(blocking=False) function call")

    if state == AuthorizationState.WAIT_CODE:
        print("Pin is required. In this example, the main program is asking it, not the python-telegram client")
        pin = input("Please insert pin code here: ")
        print("In this example, the main program is more polite than the python-telegram client")
        tg.send_code(pin)
        state = tg.login(blocking=False)

    if state == AuthorizationState.WAIT_PASSWORD:
        print("Password is required. In this example, the main program is asking it, not the python-telegram client")
        pwd = getpass.getpass('Insert password here (but please be sure that no one is spying on you): ')
        tg.send_password(pwd)
        state = tg.login(blocking=False)

    print('Authorization state: %s' % tg.authorization_state)

    result = tg.get_me()
    result.wait()

    pprint(result.update)
