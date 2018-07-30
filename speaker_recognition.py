from piwho import recognition
from piwho import vad
from sound_recorder import record

def find_speaker(flag):
    
    recog = recognition.SpeakerRecognizer()

    # Record voice until silence is detected
    # save WAV file
    #vad.record()
    record(5,'test.wav')

    # use newly recorded file for recognition
    name = []
    name = recog.identify_speaker('test.wav')
    dictn = recog.get_speaker_scores()
    
    print(name[0])
    print(dictn)
    
    if flag == 1:
        if float(dictn[name[0]]) < 0.5:
            print ('Congratulation !!! with distance ' + dictn[name[0]])
            return "CONGRATULATIONS!"
        else:
            print ('Sorry... with distance ' + dictn[name[0]])
            return "Please retry."
    elif flag == -1:
        if float(dictn[name[0]]) < 0.4:
            print ('Congratulation !!! with distance ' + dictn[name[0]])
            return "CONGRATULATIONS!"
        else:
            print ('Sorry... with distance ' + dictn[name[0]])
            return "Please retry."

