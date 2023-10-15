# Autonomous Drone Navigation With Shortest Path Navigation


[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Overview

Autonomous Drone Navigation with Shortest Path Optimization is an innovative project that empowers drones to navigate complex missions while minimizing the distance traveled. This open-source solution leverages cutting-edge hardware and software components, making it adaptable for various applications, including object detection, surveying, and AI-driven tasks.

## Features

- **Waypoint Upload**: Easily upload a list of waypoints in real-time through Ground Control Stations (GCS) like Mission Planner. The waypoints are sent to the drone's companion computer for further processing.

- **Shortest Path Calculation**: The companion computer determines the shortest path among the uploaded waypoints, optimizing mission efficiency.

- **Return to Home**: After successfully completing the mission, the drone autonomously returns to its home point.

- **Versatile Applications**: Use this system for object detection, aerial surveying, and integrating AI models in the companion computer.

- **Minimal Communication Setup**: Supports Transmitter for Minimal Communication Setup

## Hardware Setup

- **Flight Controller**: Utilize a Pixhawk Cube Orange for precise control and navigation.

- **Companion Computer**: We've chosen the Jetson Nano Developer Kit to handle complex computations, such as path optimization and AI tasks.

- **Communication Device**: A transmitter for minimal communication setup.

## Software Setup

To get started with this project, you'll need to set up the software components as follows:

1. **Use a Linux-based OS**: We recommend using a Linux-based operating system like Ubuntu for the companion computer. Make sure you have it installed.

2. **Navigation Folder Setup**:
   - Clone or download the project repository onto the companion computer.
   - Navigate to the `Navigation` folder in the repository.

3. **Configure Path**:
   - In the `Navigation` folder, you'll find the `main.sh` and `way.sh` files. Edit these files to specify the correct paths according to your setup.
   
4. **Set `main.sh` in Startup**:
   - To enable the autonomous navigation system on startup, you can add the `main.sh` script to your system's startup configuration. The process for this may vary depending on your Linux distribution. Common methods include adding an entry to the crontab or creating a systemd service. Consult your OS documentation for details.

## Usage

Now Connect the drone to the GCS and then upload the waypoints file through MAVFTP 
