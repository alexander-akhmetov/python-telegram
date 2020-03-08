import logging
import argparse
import json
from datetime import datetime

from telegram.client import Telegram
import utils

logger = logging.getLogger(__name__)

def confirm(message):
    sure = input(message + ' ')
    if sure.lower() not in ['y', 'yes']:
        exit(0)

def dump_my_msgs(tg, chat_id):
    msg_id = 0
    num_msgs = 0
    num_my_msgs = 0
    all_mine = []
    last_timestamp = 0
    while True:
        last_date = '' if last_timestamp == 0 else str(datetime.fromtimestamp(last_timestamp))
        print(f'.. Fetching {num_my_msgs}/{num_msgs} msgs @{msg_id} {last_date}')
        r = tg.get_chat_history(chat_id, 1000, msg_id)
        r.wait()
        if not r.update['total_count']:
            break
        msgs = r.update['messages']
        my_msgs = [m for m in msgs if m['sender_user_id'] == me]
        all_mine.extend(my_msgs)

        num_msgs += len(msgs)
        msg_id = msgs[-1]['id']
        last_timestamp = msgs[-1]['date']

    deletable_msg_ids = [m['id'] for m in all_mine if m['can_be_deleted_for_all_users']]

    print('msgs:', num_msgs)
    print('mine:', len(all_mine))
    print('deletable:', len(deletable_msg_ids))
    return all_mine, deletable_msg_ids


def delete_messages(chat_id, message_ids):
    BATCH=20
    num = len(message_ids)
    for i in range(0, num, BATCH):
        print(f'.. Deleting {i}-{i+BATCH-1} / {num}...')
        r = tg.delete_messages(chat_id, message_ids[i:i+BATCH], revoke=True)
        r.wait(raise_exc=True)

if __name__ == '__main__':
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

    # get me
    result = tg.get_me()
    result.wait()
    me = result.update['id']
    print(result.update)

    # get chats
    result = tg.get_chats(9223372036854775807)  # const 2^62-1: from the first
    result.wait()
    chats = result.update['chat_ids']

    # get each chat
    print('Chat List')
    chat_map = {}
    for chat_id in chats:
        r = tg.get_chat(chat_id)
        r.wait()
        title = r.update['title']
        print('  %20d\t%s' % (chat_id, title))
        chat_map[chat_id] = r.update

    selected = int(input('Select a group to clear: ').strip())
    chat_info = chat_map[selected]
    print(f'You selected: {selected} {json.dumps(chat_info, indent=2)}')
    print(f'Chat: {chat_info["title"]}')

    confirm('Are you sure?')

    # dump all my messages directly
    all_mine, deletable_msg_ids = dump_my_msgs(tg, selected)

    confirm(f'Continue to delete all {len(deletable_msg_ids)}?')

    delete_messages(selected, deletable_msg_ids)

    # continue on basic group if it's a super group
    if chat_info['type']['@type'] == 'chatTypeSupergroup':
        supergroup_id = chat_info['type']['supergroup_id']
        r = tg.get_supergroup_full_info(supergroup_id)
        r.wait()
        basic_group_id = r.update['upgraded_from_basic_group_id']
        max_message_id = r.update['upgraded_from_max_message_id']
        print(f'Found basic group: {basic_group_id} @ {max_message_id}')

        r = tg.create_basic_group_chat(basic_group_id)
        r.wait()
        basic_group_chat_id = r.update['id']
        print(f'Basic group chat: {basic_group_chat_id}')

        all_mine, deletable_msg_ids = dump_my_msgs(tg, basic_group_chat_id)

        confirm(f'Continue to delete all {len(deletable_msg_ids)}?')

        delete_messages(basic_group_chat_id, deletable_msg_ids)

    print('Done')
    tg.stop()
