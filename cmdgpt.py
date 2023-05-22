import os
import requests
import json
import pprint
import argparse

GPT_MODEL = "gpt-3.5-turbo"
GPT_URL = "https://api.openai.com/v1/chat/completions"
USER_DIR = os.path.expanduser('~')
CMDGPT_DIR_NAME = ".cmdgpt"
CMDGPT_DIR =  os.path.join(USER_DIR,CMDGPT_DIR_NAME)
CMDGPT_APIKEY_FILENAME = "cmdgpt.key"
CMDGPT_APIKEY = os.path.join(CMDGPT_DIR,CMDGPT_APIKEY_FILENAME)


def create_cmdgpt_dir():
    if not os.path.exists(CMDGPT_DIR):
        os.makedirs(CMDGPT_DIR)


def save_api_key(api_key):
    # Got to Home Direct ~
    create_cmdgpt_dir()

    key_exist = False
    proceed = True

    if os.path.exists(CMDGPT_APIKEY):
        key_exist = True
        print("File Already Exit..")
        a = input("Overwrite OpenAI Key? Y/N: ")
        if a.upper() == 'Y':
            proceed = True
        else:
            proceed = False
            print("NOT Overwriting OpenAI Key File")


    if proceed:
        final_key = dict()
        final_key["key"] = api_key

        with open(CMDGPT_APIKEY, 'w') as f:
            json.dump(final_key,f) 

def load_key():

    if not os.path.exists(CMDGPT_APIKEY):
        print("Error, Key File Doesn't Exist")
        exit(1)
    else:
        with open(CMDGPT_APIKEY, 'r') as f:
            data = json.load(f)
    key = data["key"]
    return key

verbose = False
json_output = False

parser = argparse.ArgumentParser(description='Command line ChatGPT')
parser.add_argument('-m', '--message', type=str, help='Message to send to ChatGPT', required=False)
parser.add_argument('-v', '--verbose', const=True, nargs="?", help='Show all GPT Responses', required=False)
parser.add_argument('-a', '--apikey', type=str, help='Save OpenAI API Key', required=False)
parser.add_argument('-j', '--json', type=str, const=True,nargs="?", help='Output JSON', required=False)
args = parser.parse_args()


GPT_KEY = load_key()

if args.apikey and args.apikey != "":
    save_api_key(args.apikey)
    exit(1)

if args.verbose:
    verbose = True

if args.json:
    json_output = True

if not args.message:
    chat = input("Enter Your Prompt \n")
else:
    chat = args.message

url = "https://api.openai.com/v1/chat/completions"

payload = json.dumps({
  "model": GPT_MODEL,
  "messages": [
    {
      "role": "user",
      "content": chat
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer %s' % GPT_KEY
}

response = requests.request("POST", GPT_URL, headers=headers, data=payload)



if verbose:
    print("Request:\n")
    pprint.pprint(payload)
    print("\nResponse:\n")
    pprint.pprint(response.json())
    exit(0)

# print("Response: \n")

for resp in response.json()["choices"]:
    if json_output:
        all_message = dict()

        all_message["message"] = resp["message"]["content"]

        pprint.pprint(all_message)
    else:    
        print(resp["message"]["content"])