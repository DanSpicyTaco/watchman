#!/bin/sh

# Log directory
LOG=../log

# Run snort
snort -q -A fast -l $LOG -h '192.168.1.0/24' -c ./snort.conf &
SNORT=$!

#Get current line count
LINES=`wc -l $LOG/alert | tr -d -c 0-9`

# If there's been a new alert, 
while [ true ]
do
NEWCOUNT=`wc -l $LOG/alert | tr -d -c 0-9` #Get new line count
if [ $LINES != $NEWCOUNT ]
  then
    DIFF=`expr $NEWCOUNT - $LINES`
    LINES=$NEWCOUNT
    COMMAND="$(tail -n1 $LOG/alert)"
    echo $COMMAND
    break
fi
done

# sleep 10

# Cleanup
rm $LOG/snort.log.*
kill -9 $SNORT