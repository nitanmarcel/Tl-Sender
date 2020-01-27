# Tl-Sender
Small personal app to send files from my pc to a telegram chat

## Install:

```bash
git pull https://github.com/nitanmarcel/Tl-Sender/
cd Tl-Sender/
python3 setup.py install
```


## Configure

```bash
export tl_api_id="your api id"0
export tl_api_hash="your api hash"
```

## Usage:

```bash
usage: tl [-h] [-f FILE [FILE ...]] [-r] [-d] [-c CHAT] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE [FILE ...], --file FILE [FILE ...]
                        File(s) to send. Allows usage of cp/mv syntax for file
                        selections (ex: *, *.txt)
  -r, --recursive       Send directories recursively
  -d, --force_document  Force sending as document
  -c CHAT, --chat CHAT  Username/ID of chat to send file(s) to
  -l, --list            Get a list of all chats in format Title/FirstName -
                        Username/ID

```

Example:
```bash
tl -f *.txt -c me # Sends all of the txt files found in the current dir to Saved Messages
```


## Buy me a beer/vodka/weed:

 - https://www.paypal.me/marcelalexandrunitan?locale.x=en_US
 - Revolut: Hit me on telegram with a payment link: https://t.me/nitanmarcel
 
 
 
 ## License: MIT
