import os
import re

def file_read():
    file = open("visitor_verification.txt","r")
    line = file.readline()
    i = line.split(",")[0]
    ii = line.split(",")[1]
    iii = line.split(",")[2]
    file.close()
    return int(i), int(ii), int(iii)
    
def file_write(i,ii,iii):
    file = open("visitor_verification.txt","w") 
    file.write(str(i) + "," + str(ii) + "," +str(iii))
    file.close()
    
    
def column_write(index, value):
    
    i, ii, iii = file_read()
    
    file = open("visitor_verification.txt","w")
    
    if index == 0:
        file.write(str(value) + "," + str(ii) + "," +str(iii))
    elif index == 1:
        file.write(str(i) + "," + str(value) + "," +str(iii))
    elif index == 2:
        file.write(str(i) + "," + str(ii) + "," +str(value))
    file.close()