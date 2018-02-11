#!/bin/bash


NWORKERS=1

LOC=$(pwd)

if [ $1 ]
then
    if [ $1 -gt 1 ]
    then
        NWORKERS=$1
    fi
fi

if [ !$1 ]
then
    echo "No arguments supplied. Note that you could pass nworkers parameter. Use docker run <container> -d -e nworkers=<number of workers required>"
fi


python3.5 ${LOC}/bot.py  & \

for i in $(seq 1 1 $NWORKERS)
do
    python3.5 ${LOC}/url_worker.py & \
done
python3.5 ${LOC}/final_receiver.py

