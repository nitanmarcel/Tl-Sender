import argparse
import glob
import os
from typing import Union
from telethon import TelegramClient

session_path = '' # the path where to save the session file
api_id = 0 # api_id
api_hash = '' # api_hash

client = TelegramClient('/home/marcel/.tlsender', api_id=api_id, api_hash=api_hash)


def get_file(file_path):
    return [f for f in glob.glob(file_path)]

async def send_recursive(dir: str, chat, force_document):
    file = get_file(dir + '/*')
    if file:
        for f in file:
            if os.path.isfile(f):
                if os.stat(f).st_size != 0:
                    try:
                        await client.send_file(int(chat) if chat.isdigit() else chat, f, force_document=force_document)
                    except Exception as exc:
                        print('Failed to send {} : {}'.format(f, str(exc)))
                else:
                    print("Skipping {} due file being empty".format(f))

async def send_normal(file, chat, force_document):
    for f in file:
        if os.path.isfile(f):
            if os.stat(f).st_size != 0:
                try:
                    await client.send_file(int(chat) if chat.isdigit() else chat, file, force_document=force_document)
                except Exception as exc:
                    print('Failed to send {} : {}'.format(f, str(exc)))
            else:
                print("Skipping {} due file being empty".format(f))

        else:
            print("-r not specified; omitting directory {}".format(f))

async def send(file_path: str, chat: Union[str, int], force_document: bool = False, recursive: bool = False):
    async with client:
        if not recursive:
            file = get_file(file_path)
            if file:
                await send_normal(file, chat, force_document)
            else:
                exit("No such file or directory {}".format(dir if dir not in ['*', '.*', '*.'] else ''))
        else:
            file = get_file(file_path)
            if file:
                for f in file:
                    if os.path.isdir(f):
                        await send_recursive(f, chat, force_document)
            else:
                print("No such file or directory {}".format(file if file not in ['*', '.*', '*.'] else ''))

async def get_chats():
    async with client:
        chat_list = 'CHATS : \n'
        async for chat in client.iter_dialogs():
            username = "@" + chat.entity.username if chat.entity.username else str(chat.entity.id)
            chat_list += "\n" + chat.name + " - " + username
        print(chat_list)

def start(awaitable):
    import asyncio
    asyncio.get_event_loop().run_until_complete(awaitable)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--force_document', action='store_true')
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('-f', '--file', nargs='+')
    parser.add_argument('-c', '--chat')
    parser.add_argument('-l', '--list', action='store_true')
    args = parser.parse_args()
    force_doc = False

    if args.file:
        if args.chat:
            if args.force_document:
                force_doc = True
            for file in args.file:
                if args.recursive:
                    start(send(file, args.chat, force_doc, True))
                else:
                    start(send(file, args.chat, force_doc))
        else:
            exit("There's no chat to send the file to!")
    elif args.list:
        start(get_chats())
    else:
        exit('There\'s no file to send')
