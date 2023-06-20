import logging
import argparse
import threading

from utils import setup_logging
from telegram.client import Telegram

"""
Sends a message to a chat

Usage:
    python examples/send_message.py api_id api_hash phone chat_id text
"""


if __name__ == '__main__':
    setup_logging(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('api_id', help='API id')  # https://my.telegram.org/apps
    parser.add_argument('api_hash', help='API hash')
    parser.add_argument('phone', help='Phone')
    parser.add_argument('chat_id', help='Chat id', type=int)
    parser.add_argument('text', help='Message text')
    args = parser.parse_args()

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        database_encryption_key='changeme1234',
    )
    # you must call login method before others
    tg.login()

    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()

    # `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
    # You can wait for a result with the blocking `wait` method.
    result.wait()

    if result.error:
        print(f'get chats error: {result.error_info}')
    else:
        print(f'chats: {result.update}')

    sent_message_result = tg.send_message(
        chat_id=args.chat_id,
        text=args.text,
    )
    sent_message_result.wait()

    if sent_message_result.error:
        print(f'Failed to send the message: {sent_message_result.error_info}')

    # When python-telegram sends a message to tdlib,
    # it does not send it immediately. When the message is sent, tdlib sends an updateMessageSendSucceeded event.

    message_has_been_sent = threading.Event()

    # The handler is called when the tdlib sends updateMessageSendSucceeded event
    def update_message_send_succeeded_handler(update):
        print(f'Received updateMessageSendSucceeded: {update}')
        # When we sent the message, it got a temporary id.
        # In the event we can also find the new id of the message.
        #
        # Check that this event is for the message we sent.
        if update['old_message_id'] == sent_message_result.update['id']:
            message_id = update['message']['id']
            message_has_been_sent.set()

    # When the event is received, the handler is called.
    tg.add_update_handler('updateMessageSendSucceeded', update_message_send_succeeded_handler)

    # Wait for the message to be sent
    message_has_been_sent.wait(timeout=60)

    if result.error:
        print(f'Send message error: {result.error_info}')
    else:
        print(f'Message has been sent.')

    tg.stop()
