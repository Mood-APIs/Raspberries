#!/bin/sh

USER=$(whoami)
TEMP_SONG_FILE=/home/$USER/temp_song.wav
FINAL_SONG_FILE=/home/$USER/final_song.mp3

# shellcheck disable=SC2046
echo 'Start recording   -- '$(date '+%d/%m/%Y %H:%M:%S') &&
arecord -t wav -B $(expr $1 \* 1000 \* 60) -f S16_LE -c 2 -r 44100 -d $1 --device="hw:1,0" "$TEMP_SONG_FILE" &&
echo 'Stop recording    -- '$(date '+%d/%m/%Y %H:%M:%S') &&
echo 'Convert to mp3    -- '$(date '+%d/%m/%Y %H:%M:%S')  &&
# Silence the all outputs
ffmpeg -i "$TEMP_SONG_FILE" -acodec mp3 -y "$FINAL_SONG_FILE" >> /dev/null 2>&1 &&
echo 'Converted to mp3  -- '$(date '+%d/%m/%Y %H:%M:%S')