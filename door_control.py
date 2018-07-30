import RPi.GPIO as GPIO
import time
import os
import re

def file_read():
    file = open("Global_variable_for_door.txt","r")
    line = file.readline()
    ds = line.split(",")[0]
    i = line.split(",")[1]
    file.close()
    return int(ds), int(i)
    
def file_write(ds,i):
    file = open("Global_variable_for_door.txt","w") 
    file.write(str(ds) + "," + str(i))
    file.close()


def door_ctrl():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    
    door_state,i = file_read()
    
    if i == 0:
        door_state = 1
        i+=1
        
    if door_state == 1:
        
        #open the door
        
        p = GPIO.PWM(5,46.5509)
        p.start(6.982)
        
    elif door_state == -1:
        #close the door
        p = GPIO.PWM(5,46.782)
        p.start(6.364)
        
##        p = GPIO.PWM(5,46.712)
##        p.start(6.540)
        
    file_write(door_state*(-1), i)
   
    print str(door_state), "           ", str(i)
    
    start_time_1 = time.time()
    
    while (time.time() - start_time_1) < 0.4:
        pass
   