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


width, height = pyautogui.size()
run = True
ChosenWord = 'kaks'
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
        break                   

    
    #This part is going to record the audio and save the recording
    if event == 'Salvesta':
        break
        
    if event == 'Edasi':
        # This ends the current window and lets the program display the next word in a new window
        break
    if event == gui.WIN_CLOSED or event == 'Tühista':
        # This closes the window
        run = False
        break
    
window.close()
