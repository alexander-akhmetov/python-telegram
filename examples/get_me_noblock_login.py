import argparse
import getpass

from telegram.client import Telegram
from telegram.client import AuthorizationState

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
    state = tg.start_login()

    print ("Checking the return state of the start_login() function call")
    if state == AuthorizationState.WAIT_CODE:
        print("Pin is required. In this example, the main program is asking it, not the python-telegram client")
        pin = input("Please insert pin code here: ")
        print("In this example, the main program is more polite than the python-telegram client")
        state = tg.send_code(pin)
    if state == AuthorizationState.WAIT_PWD:
        print("Password is required. In this example, the main program is asking it, not the python-telegram client")
        pwd = getpass.getpass('Insert password here (but please be sure that no one is spying on you): ')
        tg.send_password (pwd)

    result = tg.get_me()
    result.wait()
    print(result.update)