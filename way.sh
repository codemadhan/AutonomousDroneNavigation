#!/bin/bash

#navigate to the path
cd Navigation


#python program for drone navigation
python3 Mission.py --connect 127.0.0.1:14550

sleep 60

#remove waypoints file
rm /home/username/Navigation/optimal_path.json

