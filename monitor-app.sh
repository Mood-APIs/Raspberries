APP_PID=$(ps aux | grep app.py | grep -v grep | awk '{print $2}')

ALL_RECORDS_PIDS=$(ps aux | agrep record | grep -v grep | awk '{print $2}')
RECORD_PID=$(echo $ALL_RECORDS_PIDS | awk '{print $2}')

FFMPEG_PID=$(ps aux | grep ffmpeg | grep -v grep | awk '{print $2}')

USER=$(whoami)
if [ -z "$APP_PID" ]
then
	/home/$USER/mood-scripts/run.sh
else
	kill $APP_PID &&
	sleep 2 &&
	kill $RECORD_PID &&
	sleep 2 &&
	kill $FFMPEG_PID &&
	sleep 2 &&
	/home/$USER/mood-scripts/run.sh
fi
