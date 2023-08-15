#!/usr/bin/python3.6

import time
import argparse
import json
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import sin, cos, sqrt, atan2, radians
from pymavlink import mavutil
import os

#Creating a log file for the mission 
file=open("/home/username/Navigation/flight_log.txt","w")
file.write("-------------------------------------------------------------------------------------------\n")


#For getting the time
def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

import os

def generate_optimal_path(homeLatitude, homeLongitude):
    # Specify the path to the directory containing the 'order.py' file
    navigation_folder = "/home/username/Navigation"

    # Build the complete path to the 'order.py' file
    order_script_path = os.path.join(navigation_folder, "order.py")

    # Check if the file exists before attempting to run it
    if os.path.exists(order_script_path):
        # Use the os.system() function to run the 'order.py' script
        os.system(f"python3 {order_script_path} --latitude {homeLatitude} --longtitude {homeLongitude}")
    else:
        print("The 'order.py' file does not exist in the specified directory.")



#For shuttering the camera through the companion computer 
def shutter(i):
    file_path = f"../Desktop/images/droneim{i}.jpg"
    command = f"gphoto2 --capture-image-and-download --filename {file_path}"

    return_code = os.system(command)
    print(f"Return Code: {return_code}")
    file.write(f"{time_stamp()} shutter function: {return_code}\n")

    
def _convert_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = int(((decimal_degrees - degrees) * 60 - minutes) * 60)
    return ((degrees, 1), (minutes, 1), (seconds, 1))


#Function for Arming and Taking Off
def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    file.write(time_stamp() + " Basic pre-arm checks\n")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        file.write(time_stamp() + " Waiting for vehicle to initialize...\n")
        time.sleep(1)

    print("Arming motors")
    file.write(time_stamp() + " Arming motors\n")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        file.write(time_stamp() + " Waiting for arming...\n")
        time.sleep(1)

    print("Taking off!")
    file.write(time_stamp() + " Taking off!\n")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        file.write(" Altitude: " + str(vehicle.location.global_relative_frame.alt) + "\n")
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            file.write(time_stamp() + " Reached target altitude\n")
            break
        time.sleep(1)


#Function for calculation distance
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of Earth in meters
    R = 6371000

    # convert coordinates to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # calculate the differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # apply Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # calculate the distance
    distance = R * c
    return distance




#For connecting to the drone
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()
#Example of establishing connection
#    python3 projectMission.py --connect 127.0.0.1:14550
connection_string = args.connect

sitl = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


vehicle = connect(connection_string, wait_ready=True)


#getting the home position 
home_latitude=vehicle.location.global_relative_frame.lat
home_longitude=vehicle.location.global_relative_frame.lon


#for generating the optimal path
generate_optimal_path(home_latitude, home_longitude)


arm_and_takeoff(10)


file.write(time_stamp() + " Set default/target airspeed to 5\n")
vehicle.airspeed = 5

waypoints = []

with open('optimal_path.json', 'r') as file:
    data = json.load(file)
    waypoints_data = data['waypoints']
    for waypoint_data in waypoints_data:
        waypoint = LocationGlobalRelative(waypoint_data['latitude'], waypoint_data['longitude'], waypoint_data['altitude'])
        waypoints.append(waypoint)

counter=0

for waypoint in waypoints:	  
    vehicle.simple_goto(waypoint, groundspeed=5)
    while vehicle.mode.name == "GUIDED":  
        file=open("/home/username/Navigation/flight_log.txt","a")
        remaining_distance = calculate_distance(
            vehicle.location.global_relative_frame.lat,
            vehicle.location.global_relative_frame.lon,
            waypoint.lat,
            waypoint.lon
        )
        print("Distance to waypoint: ", remaining_distance)
        if remaining_distance <= 1:  # Check if the drone has reached the waypoint
            print("Reached waypoint")
            file.write(time_stamp() + " Reached waypoint\n")   
            shutter(counter)
            time.sleep(3)
            #os.rename(f"../Desktop/JetsonYolov5-main/images/droneim{counter}.jpg",f"../Desktop/JetsonYolov5-main/captured/droneim{counter}.jpg")

home_altitude = 10

# Create a new waypoint
new_waypoint = LocationGlobalRelative(home_latitude, home_longitude, home_altitude)

# Go back to home position
vehicle.simple_goto(new_waypoint, groundspeed=5)
while vehicle.mode.name == "GUIDED":
    remaining_distance = calculate_distance(
        vehicle.location.global_relative_frame.lat,
        vehicle.location.global_relative_frame.lon,
        new_waypoint.lat,
        new_waypoint.lon
    )
    print("Distance to additional waypoint: ", remaining_distance)
    file.write(time_stamp() + " Distance to additional waypoint: " + str(remaining_distance) + "\n")
    if remaining_distance <= 1:
        print("Reached additional waypoint")
        file.write(time_stamp() + " Reached additional waypoint\n")
        break
    time.sleep(1)


# Land and disarm the drone
print("Landing...")
file.write(time_stamp() + " Landing...\n")
vehicle.mode = VehicleMode("LAND")

while True:
    current_altitude = vehicle.location.global_relative_frame.alt
    print(" Altitude: ", current_altitude)
    file.write(time_stamp() + " Altitude: " + str(current_altitude) + "\n")
    if current_altitude <= 0.2:
        print("Landed")
        file.write(time_stamp() + " Landed\n")
        vehicle.armed = False
        break
    time.sleep(1)


while vehicle.armed:  # Wait for the drone to disarm
    print("Waiting for disarming...")
    file.write(time_stamp() + " Waiting for disarming...\n")
    time.sleep(1)

print("Close vehicle object")
file.write(time_stamp() + " Close vehicle object\n")
vehicle.close()

if sitl:
    sitl.stop()


file.write(time_stamp() + " file removed")
file.write("-------------------------------------------------------------------------------------------\n")
file.close()
