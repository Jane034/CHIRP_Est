import csv
import random
import sounddevice as sd
import soundfile as sf
import numpy as np
import PySimpleGUI as gui
import sys, os
from scipy.io.wavfile import write
import time
import pyautogui
#import keyboard


with open('WordList.csv') as csvfile:
    csvContent = csv.DictReader(csvfile)
    GroupNum = 1
    WordGroup = [[]]
    WavFileNames = [[]]
# Go through each row in WordList.csv file and choose random word to display from each group
    for row in csvContent:
        
        # this part continues adding words to the groups
        if GroupNum == int(row['ListNum']):
            WordGroup[GroupNum-1] += [row ['WordToDisplay'].strip('\xa0')]
            WavFileNames[GroupNum-1] += [row ['WavFileNameSansExtension'].strip('\xa0')]
            
        # here the next group of words is started
        else:
            GroupNum += 1
            WordGroup.append([])
            WavFileNames.append([])
            WordGroup[GroupNum-1] += [row ['WordToDisplay'].strip('\xa0')]
            WavFileNames[GroupNum-1] += [row ['WavFileNameSansExtension'].strip('\xa0')]

# Retrieve the path and generate a list of numbers of groups in random order for later in the GUI
p = os.path.abspath('Suss.py')
GroupOrder = list(range(0,GroupNum))
random.shuffle(GroupOrder)

### The first part starts the GUI, asks for the patient ID and creates a respective folder to save the data
gui.theme('LightGrey1') #color of the GUI for both parts
layout = [ [gui.Text('Patsiendi ID: '), gui.InputText()],
           [gui.Button('Edasi'), gui.Button('Tühista')] ]
window = gui.Window('Suss', layout)

run = True
while run:
    event, values = window.read()
    if event == 'Edasi':
        #Create subfolders with the patient ID to save respective recordings
        DateTime = time.gmtime(time.time()) #Get time and date
        TimeStamp = str(DateTime[0])+'-'+str(DateTime[1])+'-'+str(DateTime[2])+'_'+str(DateTime[3])+'-'+str(DateTime[4])+'-'+str(DateTime[5])# Timestamp of the subfolder
        
        #Create folder with patient ID and subfolder with TimeStamp
        RecordingPath = 'Recordings' + '\\' + values[0] + '\\' + TimeStamp
        os.makedirs(RecordingPath)
        
        break
    
    if event == gui.WIN_CLOSED or event == 'Tühista':
        run = False
        break
window.close()

### The second GUI chooses words randomly, plays sample audio, records the patient and saves the recordings

for i in range(0,len(GroupOrder)):
    ChosenGroup = WordGroup[GroupOrder[i]]
    ChosenWord = random.choice(ChosenGroup)
    AudioGroup = WavFileNames[GroupOrder[i]]
    AudioName = AudioGroup[ChosenGroup.index(ChosenWord)] + '.wav'
    width, height = pyautogui.size() # Get the size of your screen
    
    layout = [ [gui.VPush()],
               [gui.Push(), gui.Text(ChosenWord, justification='center', size=(10,1), font=('MerriWeather', 50)), gui.Push()],
               [gui.VPush()],
               [gui.Push(), gui.Button('Esita heli'), gui.Button('Salvesta')],
               [gui.Push(), gui.Button('Edasi'), gui.Button('Tühista')] ]
    window = gui.Window('CHIMT Est', layout, resizable = True, size =(width,height-100))
    
    while run:
        event, values = window.read()
                               
        #This part is finding and playing the respective .wav file after pressing the button
        if event == 'Esita heli':
                               
            # Get the path of AudioFiles
            pathAudio = p.replace('Suss.py', 'AudioFiles')
            
            # Generate the path of the needed audiofile
            file = os.path.join(pathAudio, AudioName)
            
            # Play the respective audiofile
            data, fs = sf.read(file, dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()
        
        #This part is going to record the audio and save the recording
        if event == 'Salvesta':
            
            #Record the sound
            duration = 5
            fs = 48000
            recording = sd.rec(int(duration * fs), samplerate = fs, channels = 2)
            sd.wait()
            
            # Write the audiofile
            RecordingFile = os.path.join(RecordingPath, AudioName)
            write(RecordingFile, fs, recording.astype(np.float32))
            
        if event == 'Edasi':
            # This ends the current window and lets the program display the next word in a new window
            break
        if event == gui.WIN_CLOSED or event == 'Tühista':
            # This closes the window
            run = False
            break
        
    window.close()
            
