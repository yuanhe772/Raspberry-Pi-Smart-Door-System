import sys
import RPi.GPIO as GPIO
import os
import shutil
import pygame
import time
import cv2
import pygame.camera
import numpy as np
import speaker_recognition
import finger_recognition
import door_control
import message_control
import user_control
import visitor_verification_upload
from PIL import Image
from io import BytesIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from sound_recorder import record
from pygame.locals import *


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#os.putenv('SDL_VIDEODRIVER','fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb1')
#os.putenv('SDL_MOUSEDRV', 'TSLIB')
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(True)
 
#Setup frame's size
size = width, height = 320,240
screen  = pygame.display.set_mode(size)

# Countdown interval
ct = 0.6

# Color Library
WARM = (254,221,120)
CREAM = (255,234,180)
BLACK = (0,0,0)
HORIZON = (160,186,205)
LAKE = (177,212,219)
HOME = (125,180,205)
WHITE = (255,255,255)
RED = (255, 0 , 0)

#Fonts
font1 = '/home/pi/ttf_font/DK Gamboge.otf'

#home level
level = 0

# Define buttons
home_buttons={'Owner':(80,120), 'Visitor':(240,120)}
visitor_buttons={'Knock-Knock':(160, 65), 'Leave A Message':(160, 175)}
message_buttons={'Remake voice message':(150, 40), 'Delete and back to Home':(160, 120),'continue and leave a selfie':(160, 200)}
selfie_buttons={'Retake a selfie':(150, 40), 'Delete and back to Home':(160, 120),'Done':(160, 200)}

# index for message
ii = 0

''' Text Drawing '''
def draw_text(text, pos, font_size, color):
    my_font = pygame.font.Font(font1, font_size)
    text_surface = my_font.render(text, True, color)
    rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, rect)

################################# Loading.... Clearing Cache ##############################################

screen.fill(LAKE)
draw_text("Loading...", (160,120), 40, WHITE)
pygame.display.flip()

shutil.rmtree('/home/pi/smart_door_system/static/media/audio')
os.mkdir('/home/pi/smart_door_system/static/media/audio')
shutil.rmtree('/home/pi/smart_door_system/static/media/image')
os.mkdir('/home/pi/smart_door_system/static/media/image')

################################# Loading.... Initialize door_state and user_state ##############################################

file = open("Global_variable_for_door.txt","w") 
file.write(str(0) + "," + str(0))
file.close()
message_control.file_write(0)
user_control.file_write(0)
visitor_verification_upload.file_write(0,0,0)

################################# Loading... Face recognition Training ##########################################

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.createLBPHFaceRecognizer()
recognizer2 = cv2.createLBPHFaceRecognizer()

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    images = []
    labels = []
    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        faces = faceCascade.detectMultiScale(image)
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
    return images, labels

            
def face_train(path, recognizer):
    images, labels = get_images_and_labels(path)
    cv2.destroyAllWindows()
    recognizer.train(images, np.array(labels))

    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]
    for image_path in image_paths:
        predict_image_pil = Image.open(image_path).convert('L')
        predict_image = np.array(predict_image_pil, 'uint8')
        faces = faceCascade.detectMultiScale(predict_image)
        for (x, y, w, h) in faces:
            nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
            nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
            if nbr_actual == nbr_predicted:
                print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
            else:
                print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)
            
            
face_train('./cornellfaces',recognizer)
face_train('./visitorfaces',recognizer2)
            
                      
draw_text("Loading...", (160,120), 40, LAKE)
pygame.display.flip()

############################# Functions ######################################################

'''face_recognition'''
def face_recognize(flag):
    global recognizer2, recognizer
    if flag == -1:
        reco = recognizer2
        path = './visitorfaces'
    else:
        reco = recognizer
        path = './cornellfaces'
        
    t_start = time.time()
    fps = 0
    face_recognized = 0
    # Capture frames from the camera
    for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
        image = frame.array    
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # Detect the face in the image
        face_income = faceCascade.detectMultiScale(gray)
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]    
        for (x, y, w, h) in face_income:
            nbr_predicted, conf = reco.predict(gray[y: y + h, x: x + w])        
            for image_path in image_paths:
                #nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
                print "Confidence {}".format(conf)
                if nbr_predicted == 6 and conf <= 130:
                    face_recognized += 1
                elif nbr_predicted == 1 and conf <= 70:
                    face_recognized += 1
                elif nbr_predicted == 7 and conf <= 70:
                    face_recognized += 1
        if face_recognized >= 1:
            #print "CONGRATULATIONS!!!{} is Correctly Recognized with confidence {}".format(nbr_predicted, conf)
            print "CONGRATULATIONS!!!"
            return "CONGRATULATIONS!"#{} is Correctly Recognized with confidence {}"#.format(nbr_actual1, conf)
        fps = fps + 1
        rawCapture.truncate( 0 )
        if fps >= 2:
            #print "SORRY...Incorrect Recognized as {} with confidence {}".format(nbr_predicted, conf)
            print "SORRY..."
            return "Please retry."

    
''' Count-Down Animation '''  
def count_down(text):
    draw_text(text, (160,80), 30, WHITE)
    draw_text("in ", (140,120), 40, WHITE)
    for t in range(1,4):
        t = 4-t
        if t < 4:
            screen.fill(LAKE)
            draw_text(text, (160,80), 30, WHITE)
            draw_text("in ", (140,120), 40, WHITE)
        draw_text(str(t), (170,120), 40, WHITE)
        pygame.display.flip()
        time.sleep(ct)
        #delay_and_home(ct)


''' Init camera through pygame library '''
def smooth_init():
    pygame.camera.init()
    cam_list = pygame.camera.list_cameras()
    cam = pygame.camera.Camera(cam_list[0],(320,240))
    cam.start()
    return cam


''' Return back to home directory '''
def delay_and_home(dt): # ct is the delay interval
    pygame.draw.rect(screen,HORIZON,[0,170,320,240],0) #0 means finishing filling
    draw_text("Home", (160,205),28, WHITE)
    pygame.display.flip()
    global level
    ts = time.time()
    while time.time()- ts < dt:
        for event in pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y > 170:
                    print "'Home' pressed"
                    level = 0
                    break

########################################### Main Method ########################################

start_time = time.time()
door_state = True

while  time.time() - start_time < 1800:
    
    screen.fill(LAKE)
    
    if ( not GPIO.input(6) ):
        print "Button 6 pressed"
        door_control.door_ctrl()
        #Debounce
        time.sleep(0.1)
        
    if ( not GPIO.input(27) ):
        print "Button 27 pressed,quit"
        quit()

    ################################ HomePage ###############################
    
    if level == 0:
        
        pygame.draw.rect(screen,HORIZON,[0,0,160,240],0) #0 means finishing filling
        user_control.file_write(0)

        for  event  in  pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if x > 300:
                    print "'Quit' pressed"
                    quit()
                if x > 160:
                    print "'Visitor' pressed"
                    user_control.file_write(-1)
                    level = 2                    
                else:
                    print "'Owner' pressed"
                    user_control.file_write(1)
                    level = 1                   
        for  text, pos  in  home_buttons.items():
            draw_text(text, pos, 40, WHITE)
    
    ############################### Owner ####################################################
    
    if level == 1:
        
        screen.fill(LAKE)
        draw_text("Put your head in frame",(160,120), 30, WHITE)
        pygame.display.flip()
        time.sleep(4*ct)
        count_down("Tap anywhere when ready")
        cam = smooth_init()
        camera = cam
        
        level = 3
                          
    ############################# Owner Mirror ##############################################
    
    if level == 3:
        
        global cam
        image1 = cam.get_image()
        image1 = pygame.transform.scale(image1,(640,480))
        ecli = pygame.draw.ellipse(image1, WHITE, [70, 0, 180, 240], 4)
        screen.blit(image1,(0,0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                print "'Face Recognition Authentation' pressed"
                cam.stop()
                global camera
                camera = PiCamera()
                camera.resolution = ( 640, 480 )
                camera.framerate = 20
                rawCapture = PiRGBArray( camera, size=( 640, 480 ) )
                level = 4
                     
    ############################# Face-Recognition ##############################################
    
    if level == 4:
        #screen.fill(LAKE)
        flag = user_control.file_read()
        text = face_recognize(flag)
        #draw_text(text, (170,110), 40, WHITE)
        
        if text=="CONGRATULATIONS!" :
            global camera
            camera.close()
            if flag == -1:
                visitor_verification_upload.column_write(0,1)
            level = 5
        else:
            
            if flag == -1:
                visitor_verification_upload.column_write(0,-1)
                global camera
                camera.close()
                level = 5
            else:
                level = 7
                              
    ############################# Face-Recognition-retry ##############################################
    
    if level == 7:
        screen.fill(LAKE)
        draw_text("Please retry.", (170,110), 40, WHITE)
        
        pygame.draw.rect(screen,HOME,[160,170,160,240],0) #0 means finishing filling
        draw_text("Retry", (240,205),28, WHITE)
        
        pygame.draw.rect(screen,HORIZON,[0,170,160,240],0) #0 means finishing filling
        draw_text("Home", (80,205),28, WHITE)
        
            
        for event in pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                
                if y > 170:
                    if x > 160:
                        print "back to last level pressed"
                        global camera
                        camera.close()
                        global cam
                        cam = smooth_init()
                        level = 3
                    else:
                        print "'Home' pressed"
                        global camera
                        camera.close()
                        level = 0
                            
    ############################# Speaker-Recognition ##############################################                  
                      
    if level == 5:
        screen.fill(LAKE)
        count_down("Start speaking")
        screen.fill(LAKE)
        draw_text("Start speaking", (160,80), 30, WHITE)
        pygame.display.flip()
        flag = user_control.file_read()
        text = speaker_recognition.find_speaker(flag)
        
        if text=="CONGRATULATIONS!" :
            if flag == -1:
                visitor_verification_upload.column_write(1,1)
            level = 6
        else:
            
            if flag == -1:
                visitor_verification_upload.column_write(1,-1)
                level = 6
            else:
                level = 8
            
            
    ############################# Speaker-Recognition-retry ##############################################
    
    if level == 8:
        screen.fill(LAKE)
        draw_text("Please retry.", (170,110), 40, WHITE)
        
        pygame.display.flip()
        
        delay_and_home(4*ct)
       
        if level != 0:
            level = 5
        
    ############################# Fingerprint-Recognition ############################################## 
        
    if level == 6:
        screen.fill(LAKE)
        count_down("Put finger on device")
        screen.fill(LAKE)
        draw_text("Put finger on device", (160,80), 30, WHITE)
        pygame.display.flip()
        
        flag = user_control.file_read()
        text, owner = finger_recognition.finger(flag)
        
        if text=="CONGRATULATIONS!" :
            if flag == -1:
                level = 11
                visitor_verification_upload.column_write(2,1)
            else:
                level = 10
        else:
            
            if flag == -1:
                visitor_verification_upload.column_write(2,-1)
                level = 11
            else:
                level = 9

            
    ############################# Finger-Recognition-retry ##############################################
    
    if level == 9:
        screen.fill(LAKE)
        draw_text("Please retry.", (170,110), 40, WHITE)
     
        pygame.display.flip()
        
        delay_and_home(4*ct)
        
        if level != 0:
            level = 6
        
    ############################# Welcome! ############################################## 
        
    if level == 10:
        global owner
        if owner == 0:
            people = "Yuan He"
        elif owner == 1:
            people = "Rongguang Wang"
        screen.fill(LAKE)
        draw_text("Welcome home : )", (160,90), 35, WHITE)
        draw_text(people, (160,150), 35, WHITE)
        pygame.display.flip()
        
        #open the door, let'em in, and close the door
        door_control.door_ctrl()
        time.sleep(4*ct)
        door_control.door_ctrl()
        
        level = 0
            
    ############################## Visitor #############################################
    
    if level == 2:
        
        screen.fill(LAKE)
        pygame.draw.rect(screen,HORIZON,[0,0,320,120],0) #0 means finishing filling
        
        for  text, pos  in  visitor_buttons.items():
            draw_text(text, pos, 40, WHITE)
        
        for  event  in  pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y < 120:
                    level = 1
                else:
                    level = 12
                         
    ############################## Knock-knock #############################################
    
    if level == 11:
        screen.fill(LAKE)
        draw_text("Your request was sent!", (160,80), 30, WHITE)
        draw_text("Waiting for response...", (160,120), 30, WHITE)
        pygame.display.flip()
        #message sent
        message_control.file_write(1)
        #wait fro response
        time.sleep(10*ct)
        if message_control.file_read() == 1:
            screen.fill(LAKE)
            draw_text("Owner not online", (160,80), 30, WHITE)
            draw_text("please leave a message", (160,120), 30, WHITE)
            pygame.display.flip()
            time.sleep(6*ct)
            level = 12
        else:
            screen.fill(LAKE)
            draw_text("Owner is responding", (160,80), 30, WHITE)
            draw_text("Please look at the camera", (160,120), 30, WHITE)
            pygame.display.flip()
            time.sleep(20*ct)
            level = 0
        
    ############################## Leave a voice-message #############################################
    
    if level == 12:
        
        count_down("Leave a 10s voice message")
        screen.fill(LAKE)
        draw_text("Leave a 10s voice message", (160,80), 30, WHITE)
        pygame.display.flip()
        
        global ii
        ii+=1
        record(10,'/home/pi/smart_door_system/static/media/audio/' + str(ii) + '.wav')
        
        level = 13

    ############################## re-leave a message or continue? #############################################
    
    if level == 13:
        
        screen.fill(LAKE)
        pygame.draw.rect(screen,HORIZON,[0,80,320,160],0)
        pygame.draw.rect(screen,HOME,[0,160,320,240],0)
        
        for  text, pos  in  message_buttons.items():
            draw_text(text, pos, 30, WHITE)
        
        for  event  in  pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y < 80:
                    print "re-leave a voice message"
                    os.remove('/home/pi/smart_door_system/static/media/audio/' + str(ii) + '.wav')
                    ii-=1
                    level = 12
                elif y < 160:
                    print "delete and back to home"
                    os.remove('/home/pi/smart_door_system/static/media/audio/' + str(ii) + '.wav')
                    ii-=1
                    level = 0
                else:
                    level = 14
        
    ##################################### Leave a selfie ###############################################
    
    if level == 14:
        count_down("tap anywhere to selfie")
        cam = smooth_init()
        camera = cam
        level = 15
        
    ##################################### Leave a selfie ###############################################
    
    if level == 15:
        global cam
        #cam = smooth_init()
        image1 = cam.get_image()
        image1 = pygame.transform.scale(image1,(640,480))
        screen.blit(image1,(0,0))
        pygame.display.update()
        
        for  event  in  pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                image = cam.get_image()
                pygame.image.save(image,'/home/pi/smart_door_system/static/media/image/' + str(ii) + '.jpg')
                screen.fill(WHITE)
                pygame.display.flip()
                time.sleep(0.05)
                screen.blit(image,(0,0))
                time.sleep(0.05)
                pygame.display.flip()
                cam.stop()
                level = 16
                
    ############################## re-take a selfie #############################################
    
    if level == 16:
        
        screen.fill(LAKE)
        pygame.draw.rect(screen,HORIZON,[0,80,320,160],0)
        pygame.draw.rect(screen,HOME,[0,160,320,240],0)
        
        for  text, pos  in  selfie_buttons.items():
            draw_text(text, pos, 30, WHITE)
        
        for  event  in  pygame.event.get():
            if(event.type  is  pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y < 80:
                    print "re-take a selfie"
                    os.remove('/home/pi/smart_door_system/static/media/image/' + str(ii) + '.jpg')
                    cam = smooth_init()
                    camera = cam
                    level = 15
                elif y < 160:
                    print "delete and back to home"
                    os.remove('/home/pi/smart_door_system/static/media/audio/' + str(ii) + '.wav')
                    os.remove('/home/pi/smart_door_system/static/media/image/' + str(ii) + '.jpg')
                    ii-=1
                    level = 0
                else:
                    print "Bye-bye"
                    level = 17
                    
    ############################## Bye-bye #############################################
    
    if level == 17:
    
        screen.fill(LAKE)
        draw_text("Thx, bye-bye ; )", (160,120), 35, WHITE)
        pygame.display.flip()
        
        time.sleep(3*ct)
        
        level = 0
    
    
    pygame.display.flip()
