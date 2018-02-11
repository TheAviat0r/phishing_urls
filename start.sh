#!/bin/bash

python3.5 bot.py  & \

NWORKERS=1

if [ $1 -gt 1 ]
then
    NWORKERS=$1
fi

for i in $(seq 1 1 $NWORKERS)
do
    python3.5 url_worker.py & \
done
python3.5 final_receiver.py

