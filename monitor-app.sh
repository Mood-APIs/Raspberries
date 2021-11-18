APP_PID=$(ps aux | grep app.py | grep -v grep | awk '{print $2}')

ALL_RECORDS_PIDS=$(ps aux | grep arecord | grep -v grep | awk '{print $2}')
RECORD_PID=$(echo $ALL_RECORDS_PIDS | awk '{print $2}')

FFMPEG_PID=$(ps aux | grep ffmpeg | grep -v grep | awk '{print $2}')

USER=$(whoami)

# Kill record processes
if [ -z "$RECORD_PID" ]
then
	echo "no record processes"
else
	kill $RECORD_PID &&
	sleep 2
fi

# Kill ffmpeg processes
if [ -z "$FFMPEG_PID" ]
then
	echo "no ffmpeg processes"
else
	kill $FFMPEG_PID &&
	sleep 2
fi

if [ -z "$APP_PID" ]
then
	/home/$USER/mood-scripts/run.sh
else
	kill $APP_PID &&
	sleep 2 &&
	/home/$USER/mood-scripts/run.sh
fi
