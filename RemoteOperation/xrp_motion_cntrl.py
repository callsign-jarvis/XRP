#Filename:  xrp_motion_cntrl.py
#Author : Aswin S Babu
from XRPLib.defaults import *
from machine import Timer, UART, Pin
import select
import sys
import time

# Set up the poll object for detecting incoming data
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)  # Register stdin for polling

print('XRP robot at your service!')
print("Awaiting remote commands")
def corr_Motion(command):
    if command == 'F':  # Forward command
        drivetrain.set_effort(0.5, 0.5)
        time.sleep(2)
        
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(2) #wait for some 1 sec 
    elif command == 'B':  # Backward command
        drivetrain.set_effort(-0.5, -0.5)
        time.sleep(2) #wait for some time
        
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(2) #wait for some 1 sec
    elif command == 'L':  # Left command
        drivetrain.set_effort(-0.5, 0.5)
        time.sleep(2)
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(2) #wait for some 1 sec
    elif command == 'R':  # Right command
        drivetrain.set_effort(0.5, -0.5)
        time.sleep(2)
        
        drivetrain.set_effort(0, 0) #Stop the robot
        time.sleep(2) #wait for some 1 sec
    else:
        drivetrain.set_effort(0, 0)  # Stop if unknown command
        time.sleep(5) #wait for some 5 sec
    return None


# Loop indefinitely to check for incoming data
while True:
    poll_results = poll_obj.poll(1000)  # Wait for data for 1000 milliseconds (1 second)
    if poll_results:
        # Read the data from stdin and strip whitespace/newline
        data = sys.stdin.readline().strip()
        # Print or process received data; adjust stdout use if issues arise
        print(f"\nReceived data: {data}")
        corr_Motion(data)
    else:
        # No data received; continue loop or handle other tasks
        #print("No data received, waiting...")
        time.sleep(2)  # Delay to reduce unnecessary looping
