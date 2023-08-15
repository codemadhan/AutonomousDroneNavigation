#!/usr/bin/expect -f

#Starting mavproxy.py
spawn mavproxy.py --out 127.0.0.1:14550

#Getting the file from the flight controller to the Onboard Computer
while {1} {
    if {[file exists "Navigation/waypoint_to_go.json"]} {
        break
    } else {
        expect ">>>"
        send "ftp get waypoints/waypoint_to_go.json Navigation/waypoint_to_go.json\r"
        expect ">>>"
    }
}


#opening another terminal to run our mission files
spawn gnome-terminal -- bash -c "./way.sh; exec bash"

#Starting mavproxy.py again 
spawn mavproxy.py --out 127.0.0.1:14550

#removing the file from the flight controller
expect ">>>"
send "ftp rm waypoints/waypoint_to_go.json\r"
expect ">>>"





