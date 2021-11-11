import requests
from datetime import datetime
import subprocess
import shlex

import os

bar_id = '84:d8:1b:8c:b3:fb'
path_file = f'/home/{os.getlogin()}/final_song.wav'
log_path = f'/home/{os.getlogin()}/logs/out-' + datetime.now().strftime('%d-%m-%y') + '.log'

# identity: rasp_pi
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTQ1Mjg3MywianRpIjoiMjQ3NmJlOTktNDQ2Yi00ZTBjLTk2NmQtNjBkOTBjODgzMWE4IiwibmJmIjoxNjM1NDUyODczLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoicmFzcF9waSIsImV4cCI6MTYzNTQ3NDQ3M30.U5i9eIlqziPgPGKJviLEvgBuloNIXR9iPWsPRIywaao'
ref_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTQ1Mjg3MywianRpIjoiMmEwMTMyNzUtOGFmYy00NmQyLWIwNzctZTZiZjEwMGJkNzE4IiwibmJmIjoxNjM1NDUyODczLCJ0eXBlIjoicmVmcmVzaCIsInN1YiI6InJhc3BfcGkiLCJleHAiOjE3MzAwNjA4NzN9.f7JbSX_aCu87DNg2gzdrpAZJvABbrgLyea9XSjatVlc'

def init():

    url = "https://r9rjketed6.execute-api.eu-south-1.amazonaws.com/dev/init"
    payload = {}
    files = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    print(response.text)

    return response.json()

def new_song(token):

    url = "https://r9rjketed6.execute-api.eu-south-1.amazonaws.com/dev/new_song/" + bar_id
    payload = {}
    files = [
      ('file', ('2021-03-18-10_47_59.mp3', open(path_file, 'rb'), 'audio/mpeg'))
    ]
    headers = {
      'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

    return response.json()

def refresh_token(token):

    url = "https://r9rjketed6.execute-api.eu-south-1.amazonaws.com/dev/refresh_token"
    payload = {}
    files = {}
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("PUT", url, headers=headers, data=payload, files=files)
    print(response.text)

    return response.json()['access_token']

def upload():

    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print('Start uploading -- ' + datetime_str + '\n')

    global access_token
    response = new_song(access_token)

    # Check if access_token is expired
    if 'error' in response.keys() and response['error']['status'] == '402':

        # Refresh it & try again
        access_token = refresh_token(ref_token)
        new_song(access_token)

    # Spotify token expired
    if 'statusCode' in response.keys() and response['statusCode'] == 408:
        new_song(access_token)

    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print('Stop uploading -- ' + datetime_str)


print(f'Running at ({os.getpid()})')
init_response = init()
if init_response['statusCode'] == 200:
    settings = init_response['settings']

    # Read recording timeframes
    basic_timeframe = settings['basic_timeframe']
    start_time = datetime.strptime(basic_timeframe['start'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(basic_timeframe['end'], '%Y-%m-%d %H:%M:%S')
    now_time = datetime.now()
    
    # Out of recording timeframe
    if now_time > end_time or now_time < start_time:
        print('Out of recording timeframe!')
        print(f'Now time: {str(now_time)}')
        print(f'Start time: {str(start_time)}')
        print(f'End time: {str(end_time)}')
        print('----------------------------------------------------------------')

    # Recording
    while start_time < now_time < end_time:
        record_time = settings['record_timeOffset']
        subprocess.call(shlex.split(f'/home/{os.getlogin()}/mood-scripts/record.sh ' + str(record_time)))
        upload()
        print('----------------------------------------------------------------')

