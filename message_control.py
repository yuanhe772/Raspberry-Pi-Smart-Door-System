import time
import os
import re

def file_read():
    file = open("message_for_video.txt","r")
    line = file.readline()
    file.close()
    return int(line)
    
def file_write(line):
    file = open("message_for_video.txt","w") 
    file.write(str(line))
    file.close()

   
    
   
