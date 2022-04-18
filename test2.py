import sounddevice as sd
import soundfile as sf
#import numpy as np
import PySimpleGUI as gui
import sys, os
from scipy.io.wavfile import write
#import time#, queue, multiprocessing
import pyautogui
#from pydub import AudioSegment

import time
import numpy as np
import scipy.signal as signal
#q = queue.Queue()

p = os.path.abspath('test.py')
DateTime = time.gmtime(time.time()) #Get time and date
TimeStamp = str(DateTime[0])+'-'+str(DateTime[1])+'-'+str(DateTime[2])+'_'+str(DateTime[3])+'-'+str(DateTime[4])+'-'+str(DateTime[5])# Timestamp of the subfolder

#Create folder with patient ID and subfolder with TimeStamp
RecordingPath = 'Recordings' + '\\' + TimeStamp
os.makedirs(RecordingPath)

width, height = pyautogui.size()
run = True
ChosenWord = 'kaks'
layout = [ [gui.VPush()],
           [gui.Push(), gui.Text(ChosenWord, justification='center', size=(10,1), font=('MerriWeather', 50)), gui.Push()],
           [gui.VPush()],
           [gui.Push(), gui.Button('Esita heli'), gui.Button('Salvesta'), gui.Button('Stopp')],
           [gui.Push(), gui.Button('Edasi'), gui.Button('Tühista')] ]
window = gui.Window('CHIMT Est', layout, resizable = True, size =(width,height-100))

###
fulldata = np.array([])

def callback(in_data, fs, time, flag):
    print('kutsunf')
    sd.InputStream.stop(mic_queue)
    #array = in_data.read(fs)
    sd.InputStream.start(mic_queue)
    fulldata = np.append(fulldata, in_data)
    return fulldata

###

while run:
    event, values = window.read()
    rec = 'off'                       
    #This part is finding and playing the respective .wav file after pressing the button
    if event == 'Esita heli':
        break                   

    
    #This part is going to record the audio and save the recording
    if event == 'Salvesta':
        rec = 'on'
        fs = 48000
        AudioName = 'a.wav'
        RecordingPath = os.path.join(RecordingPath, AudioName)
        RecordingFile = sf.SoundFile(RecordingPath, mode = 'x', samplerate = fs, channels = 2)
        mic_queue = sd.InputStream(samplerate = fs, channels = 2, callback = callback)
        sd.InputStream.start(mic_queue)
        while True:
            time.sleep(5)
        print('Alustas salvestamist')
        
        break
    if event == 'Stopp' and rec == 'on':
        stop_recording(mic_queue)
        recording = sd.mic_queue.read(fs)
        write(RecordingPath, fs, recording.astype(np.float32))
        break
        
# #         try:
# #             RecordingFile = sf.SoundFile(RecordingPath, mode = 'x', samplerate = fs, channels = 2)
# #             mic_queue = sd.InputStream(samplerate = fs, channels = 2)
# #             sd.InputStream.start(mic_queue)
# #             print('Alustas salvestamist')
# #             if event == 'Stopp':
# #                 sd.InputStream.stop(mic_queue)
# #                 file = mic_queue.read(fs)
# #         except KeyboardInterrupt:
# #             sd.InputStream.stop(mic_queue)
            
#                     #RecordingFile.write(q.get())
#                    # aa = sd.InputStream.read(mic_queue, fs)
#                     #write(RecordingFile, aa.astype(np.float32))
#                 
#                     if event == 'Stopp':
#                         print('lõppes')
#                         sd.InputStream.stop(mic_queue)
#                         False
                        
            #RecordingFile = sd.InputStream.read(mic_queue, fs)

                        
#                 try:
#                     while True:
#                         RecordingFile.write(mic_queue.get())
#                 except event == 'Salvesta':
#                     stop_recording(RecordingFile)
        
            
        #recording = 
        
        
        # Write the audiofile
        

        
        
        ### Below is the old working version
        
#         #Record the sound
#         duration = 5
#         fs = 48000
#         recording = sd.rec(int(duration * fs), samplerate = fs, channels = 2)
#         sd.wait()
#         
#         # Write the audiofile
#         AudioName = 'kaks.wav'
#         RecordingFile = os.path.join(RecordingPath, AudioName)
#         write(RecordingFile, fs, recording.astype(np.float32))
#         break
        
    if event == 'Edasi':
        # This ends the current window and lets the program display the next word in a new window
        break
    if event == gui.WIN_CLOSED or event == 'Tühista':
        # This closes the window
        run = False
        break
    
window.close()
