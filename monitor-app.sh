APP_PID=$(ps aux | grep app.py | grep -v grep | awk '{print $2}') &&
USER=$(whoami)
if [ -z "$APP_PID" ]
then
	/home/$USER/mood-scripts/run.sh
else
	kill $APP_PID &&
	sleep 2 &&
	/home/$USER/mood-scripts/run.sh
fi
