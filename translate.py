# TODO

# creat a list of language and assign values to them
# let user select source language and store value
# let user select target language and store value
# Ask user for text -- ensure it is in source language. validate if possible with lang codes
# get user input in varraible
# init sun bird api with --source lang, text, target lang, api key 
# get the surnbird api result
# Display results to the user 
# useing tinker for gui

# used for making requsts to sunbird
import requests as rq
import tkinter as tk
import os
from dotenv import load_dotenv
load_dotenv()



# request URL
url = "https://api.sunbird.ai/tasks/nllb_translate"
# Get the sunbird api key from env file

access_token = os.getenv("sunbirdApiKey")
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}



print("Choose Source Language Number: 1 FOR Engish, 2 FOR Luganda, 3 FOR Runyankole, 4 FOR Acholi, 5 FOR Acholi")

source_language_num = int(input())


print("Choose Target Language Number: 1 FOR Engish, 2 FOR Luganda, 3 FOR Runyankole, 4 FOR Acholi, 5 FOR Acholi")

target_language_num = int(input())

print("Enter Translation Text")

translate_text = input()

print("source lang", source_language_num)
print("target lang", target_language_num)
print("Translate text", translate_text)

# Translation logic
source_language=""
target_language=""


if(source_language_num == 1):
    print("worked here =================")
    source_language = "eng"


if(source_language_num == 2):
    source_language = "lug"


if(source_language_num == 3):
    source_language = "nyn"


if(source_language_num == 4):
    source_language = "ach"


if(source_language_num == 5):
    source_language = "teo"


if(target_language_num == 1):
    target_language = "eng"


if(target_language_num == 2):
    target_language = "lug"


if(target_language_num == 3):
    target_language = "nyn"


if(target_language_num == 4):
    target_language = "ach"


if(target_language_num == 5):
    target_language = "teo"



print( "source_language", source_language)
print( "target_language", target_language)
print( "text", translate_text)
    
    
data = {
    "source_language": source_language,
    "target_language": target_language,
    "text": translate_text
}

response = rq.post(url, headers=headers, json=data)

print(response.json())

# 










