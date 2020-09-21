# Open the watchman process
cd watchman
python receiver.py &
WATCHMAN=$!
cd ..

# Open the GCS in a new terminal
osascript -e 'tell app "Terminal"
   do script "cd \"/Users/Dan/Documents/OneDrive - UNSW/thesis/watchman/uav\" && echo $$ > pid && python gcs.py -a"
end tell'

# Sleep for 5 seconds to allow the GCS to open
sleep 5

# Get the PID of the GCS
GCS=`cat uav/pid`
rm uav/pid

# Check if the watchman process has exited
# If it has, kill the GCS process
while [ true ]
do
if ! ps -p $WATCHMAN > /dev/null
  then
    echo 'Killing GCS...'
    kill -9 $GCS
    echo 'done'
    break
fi
done