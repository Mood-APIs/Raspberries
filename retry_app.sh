#!/bin/sh

USER=$(whoami)
# shellcheck disable=SC2009
APP_PID=$(ps aux | grep app.py | grep -v grep | awk '{print $2}')
# shellcheck disable=SC2009
RECORD_PID=$(ps aux | grep arecord | grep -v grep | awk '{print $2}')
# shellcheck disable=SC2009
FFMPEG_PID=$(ps aux | grep ffmpeg | grep -v grep | awk '{print $2}')


if [ -z "$APP_PID" ]
then	
	# Kill ffmpeg process
	if [ -z "$FFMPEG_PID" ]
	then
		echo "no ffmpeg processes"
	else	
		echo "ffmpeg -> " + "$FFMPEG_PID" &&
		kill "$FFMPEG_PID" &&
		sleep 1
	fi
	
	# kill record process
	if [ -z "$RECORD_PID" ]
	then
		echo "no record processes"
	else	
		echo "record -> " + "$RECORD_PID" &&
		kill "$RECORD_PID" &&
		sleep 2
	fi
	
	# Run basic script
	/home/"$USER"/mood-scripts/run.sh
else
	:
fi
