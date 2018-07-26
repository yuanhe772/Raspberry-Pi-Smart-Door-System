# R-Pi-Smart-Door-System-

## A Brief insight
An entrance-guarding system using Raspberry Pi, permitting access with face, voice and fingerprint recognition, with a local touch screen GUI and a secured-login web interface for remote control over the system 
Used Python Flask for setting up the server on Pi to support front-end web pages and restore visitor messages as key-value pair in local database
Face recognition ran at 15 FPS utilizing multi-core coordination, 3X faster than usual single-core implementation
Website for the project: https://courses.cit.cornell.edu/ece5990/ECE5725_Fall2017_projects/final_yh772_rw564/;

## Key words
Pygame for Pi-TFT, Server Design with Flask, Fingerprint Sensor for Raspberry-pi, Pi-Cam


## Tips for scripts of face recognition
In the scripts of .zip file, there are path names of "cornellfaces" and "visitorfaces" containing face recognition's training set. Please put your own biographic photos in the correct path accordingly, and the scripts in .zip file would have them trained for face-recognition purpose.
