# web.py
# import the Flask class from the flask module
from importlib import import_module
import os, shutil
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, Response
from functools import wraps
from camera_pi import Camera
import finger_recognition
import door_control
import message_control
import visitor_verification_upload
import time


music_dir = '/home/pi/smart_door_system/static/media/audio'
image_dir = '/home/pi/smart_door_system/static/media/image'

music_files_original = [f for f in os.listdir(music_dir) if f.endswith('wav')]
music_files_number_original = len(music_files_original)

data = {'message': 'false'}

def message_b(num):
    music_files = [f for f in os.listdir(music_dir) if f.endswith('wav')]
    music_files_number = len(music_files)
    global data2
    if music_files_number != num:
        data2 = {'message': 'true'}
    else:
        data2 = {'message': 'false'}
        
def message_a():
    global data1
    if message_control.file_read() == 1:
        data1 = {'message': 'true'}
    else:
        data1 = {'message': 'false'}

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'smart door'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
#@login_required
@app.route('/home')
def home():
    return render_template('home.html')  # render a template
    # return "Hello, World!"  # return a string


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'rw564') \
                or request.form['password'] != 'rw564':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            global music_files_number_original
            message_b(music_files_number_original)
            global data2
            message_a()
            global data1
            return render_template('index.html',
                                   title = 'Message',
                                   data1 = data1,
                                   data2 = data2)  # render a template
    return render_template('login.html', error=error)


@app.route('/logout')
#@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are logged out now.')
    return render_template('logout.html')  # render a template


@app.route('/index_1')
#@login_required
def index_1():
    global music_files_number_original
    message_b(music_files_number_original)
    global data2
    data1 = {'message': 'false'}
    message_control.file_write(0)
    a,b,c=visitor_verification_upload.file_read()
    return render_template('index_1.html',
                           data1 = data1,
                           data2 = data2,
                           a=a,
                           b=b,
                           c=c)  # render a template

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/index_2')
#@login_required
def index_2():
    music_files = [f for f in os.listdir(music_dir) if f.endswith('wav')]
    music_files_number = len(music_files)
    image_files = [f for f in os.listdir(image_dir) if f.endswith('jpg')]
    image_files_number = len(image_files)
    global music_files_number_original
    music_files_number_original = music_files_number 
    data2 = {'message': 'false'}
    message_a()
    global data1
    return render_template("index_2.html",
                        title = 'Message',
                        music_files_number = music_files_number,
                        music_files = music_files,
                        image_files_number = image_files_number,
                        image_files = image_files,
                        data1 = data1,
                        data2 = data2)


@app.route('/open', methods=['GET','POST'])
def open():
    print('Open the door!')
    door_control.door_ctrl()
    return "Door opening..."


@app.route('/delete_visitor', methods=['GET','POST'])
def delete_visitor():
    print('Delete visitor!')
    visitor_verification_upload.file_write(0,0,0)
    return "Deleting..."


@app.route('/delete_voice', methods=['GET','POST'])
def delete_voice():
    print('Delete message!')
    shutil.rmtree('/home/pi/smart_door_system/static/media/audio')
    os.mkdir('/home/pi/smart_door_system/static/media/audio')
    shutil.rmtree('/home/pi/smart_door_system/static/media/image')
    os.mkdir('/home/pi/smart_door_system/static/media/image')
    return "Delete...message"


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=True)
