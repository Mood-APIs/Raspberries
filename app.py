import requests
from datetime import datetime
import subprocess
import shlex
import sched
import time
import os
import sys

bar_id = 'E2:63:DA:BA:56:81'
path_file = f'/home/{os.getlogin()}/final_song.mp3'

# identity: rasp_pi
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTQ1Mjg3MywianRpIjoiMjQ3NmJlOTktNDQ2Yi00ZTBjLTk2NmQtNjBkOTBjODgzMWE4IiwibmJmIjoxNjM1NDUyODczLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoicmFzcF9waSIsImV4cCI6MTYzNTQ3NDQ3M30.U5i9eIlqziPgPGKJviLEvgBuloNIXR9iPWsPRIywaao'
ref_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTQ1Mjg3MywianRpIjoiMmEwMTMyNzUtOGFmYy00NmQyLWIwNzctZTZiZjEwMGJkNzE4IiwibmJmIjoxNjM1NDUyODczLCJ0eXBlIjoicmVmcmVzaCIsInN1YiI6InJhc3BfcGkiLCJleHAiOjE3MzAwNjA4NzN9.f7JbSX_aCu87DNg2gzdrpAZJvABbrgLyea9XSjatVlc'

global start_time, end_time, record_time, log_file

def update_init_settings():

    global log_file
    date_now = datetime.now().strftime('%d-%m-%Y')
    log_file = f'/home/{os.getlogin()}/logs/out-{date_now}.log'
    with open(log_file, 'a') as file:

        # sys.stdout = open(log_file, 'wt')

        url = "https://r9rjketed6.execute-api.eu-south-1.amazonaws.com/dev/init"
        payload = {}
        files = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        f.write(response.text)

        global start_time, end_time, record_time

        settings = response.json()['settings']
        basic_timeframe = settings['basic_timeframe']
        start_time = datetime.strptime(basic_timeframe['start'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(basic_timeframe['end'], '%Y-%m-%d %H:%M:%S')
        record_time = settings['record_timeOffset']

        return file


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
    f.write(response.text)

    return response.json()

def refresh_token(token):

    url = "https://r9rjketed6.execute-api.eu-south-1.amazonaws.com/dev/refresh_token"
    payload = {}
    files = {}
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("PUT", url, headers=headers, data=payload, files=files)
    f.write(response.text)

    return response.json()['access_token']

def upload():

    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    f.write('Start uploading -- ' + datetime_str + '\n')

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
    f.write('Stop uploading -- ' + datetime_str)


while True:

    # Set the correct path for th log file
    f = update_init_settings()

    f.write(f'Running at ({os.getpid()})')

    # Out of recording timeframe
    now_time = datetime.now()
    if now_time > end_time or now_time < start_time:
        f.write('Out of recording timeframe!')
        f.write(f'Now time: {str(now_time)}')
        f.write(f'Start time: {str(start_time)}')
        f.write(f'End time: {str(end_time)}')
        f.write('----------------------------------------------------------------')
        time.sleep(1800)

    # Recording
    while start_time < now_time < end_time:

        f.write('-----------------------------')
        f.write(f'Now time: {str(now_time)}')
        f.write(f'Start time: {str(start_time)}')
        f.write(f'End time: {str(end_time)}')
        f.write('-----------------------------')

        subprocess.call(shlex.split(f'/home/{os.getlogin()}/mood-scripts/record.sh ' + str(record_time)))
        upload()
        f.write('----------------------------------------------------------------')

        # Check if a half-hour passed
        minutes = datetime.now().minute
        if minutes % 30 <= 3:
            update_init_settings()
