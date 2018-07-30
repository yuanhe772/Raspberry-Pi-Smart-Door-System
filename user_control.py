import time
import os
import re

def file_read():
    file = open("user.txt","r")
    line = file.readline()
    file.close()
    return int(line)
    
def file_write(line):
    file = open("user.txt","w") 
    file.write(str(line))
    file.close()

   
    
   

