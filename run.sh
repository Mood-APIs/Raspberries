LOG_FILE=~/logs/out-$(date +"%d-%m-%y").log

python3 -u ~/mood-scripts/app.py >> $LOG_FILE &
