import argparse
import glob
import os
from typing import Union
from pathlib import Path
from telethon import TelegramClient


API_ID = os.environ.get('tl_api_id', None)
API_HASH = os.environ.get('tl_api_hash', None)

if not API_ID:
    quit('your api id can\'t be none. Set it using `export tl_api_id=your_api_id')
if not API_HASH:
    quit('your api hash can\'t be none. Set it using `export tl_api_hash=your_api_hash')

client = TelegramClient(str(Path.home()) + '/.tlsend', api_id=int(API_ID), api_hash=API_HASH)


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
    parser.add_argument('-f', '--file', nargs='+', help='File(s) to send. Allows usage of cp/mv syntax for file selections (ex: *, *.txt)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Send directories recursively')
    parser.add_argument('-d', '--force_document', action='store_true', help='Force sending as document')
    parser.add_argument('-c', '--chat', help='Username/ID of chat to send file(s) to')
    parser.add_argument('-l', '--list', action='store_true', help='Get a list of all chats in format Title/FirstName - Username/ID')
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
