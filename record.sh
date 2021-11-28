#!/bin/sh

# DATETIME=$(date '+%d/%m/%Y %H:%M:%S')
USER=$(whoami)
# LOG_FILE=/home/$USER/logs/out-$(date +"%d-%m-%y").log
TEMP_SONG_FILE=/home/$USER/temp_song.wav
FINAL_SONG_FILE=/home/$USER/final_song.mp3

# shellcheck disable=SC2046
echo 'Start recording   -- '$(date '+%d/%m/%Y %H:%M:%S') &&
sudo arecord -t wav -B $(expr $1 \* 1000 \* 60) -f S16_LE -c 2 -r 44100 -d $1 --device="hw:1,0" "$TEMP_SONG_FILE" &&
# sudo arecord -f S16_LE -r 11025 -d $1 --device="hw:1,0" ~/temp_song.wav &&
echo 'Stop recording    -- '$(date '+%d/%m/%Y %H:%M:%S') &&
echo 'Convert to mp3    -- '$(date '+%d/%m/%Y %H:%M:%S')  &&
ffmpeg -i "$TEMP_SONG_FILE" -acodec mp3 -y "$FINAL_SONG_FILE" &&
echo 'Converted to mp3  -- '$(date '+%d/%m/%Y %H:%M:%S')

# echo 'Start compressing  -- '$DATETIME >> $LOG_FILE &&
# sox $TEMP_SONG_FILE -r 4000 $FINAL_SONG_FILE &&
# echo 'Stop compressing   -- '$DATETIME >> $LOG_FILE
