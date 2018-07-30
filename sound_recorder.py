import pyaudio
import wave

def record(t,path):
 
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 8192
    RECORD_SECONDS = t
    WAVE_OUTPUT_FILENAME = path #"test.wav"
 
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        dev = audio.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels']))
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index = 0,
                    frames_per_buffer=CHUNK)
    print "recording..."
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()