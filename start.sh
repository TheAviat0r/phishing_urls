#!/bin/bash


NWORKERS=1

if [ $1 -gt 1 ]
then
    NWORKERS=$1
fi

python3.5 phishing_urls/bot.py  & \

for i in $(seq 1 1 $NWORKERS)
do
    python3.5 phishing_urls/url_worker.py & \
done
python3.5 phishing_urls/final_receiver.py

