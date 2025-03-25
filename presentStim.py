from psychopy import visual, event, core, gui
from psychopy.hardware import keyboard
from os import listdir, path, chdir
from screeninfo import get_monitors
import random
import numpy as np
import pandas
import sys
import sqlite3
from random import randint

# Set working directory
mainDir = path.dirname(path.abspath(sys.argv[0]))
chdir(mainDir)

# Set parameters
stimDir = './colorStim/'
datFile = 'participant_data.db'
obs = 15

# PsychoPy experiment setup ----------------------------------------

# Set PID if args included, otherwise create dialogue box to get PID
if len(sys.argv) > 1:
    pid = int(sys.argv[1])
else:
    validPid = False
    while not validPid:
        pidDlg = gui.Dlg()
        pidDlg.addField('PID:')
        pid = int(pidDlg.show()[0])
        if pidDlg.OK:
            validPid = True
            
colorstim = listdir (stimDir)
colordict = {i+1: {} for i in range(obs)}

for item in colorstim:
    splt = item.split('_')
    stimnum = int(splt[0][5:])
    angle = int(splt[2][:-4])
    colordict[stimnum][angle] = item
    
info = {'Instruction':'Which of these faces most resembles the face of a person you would imagine being affected by climate change?','ITI':0.5}

# Setup PsychoPy gui parameters
# @param title window title
#infoDlg = gui.DlgFromDict(dictionary=info, title='Prototype Task', order=['Instruction', 'Stimuli folder', 'Data file'])

# Check gui setup correct, if not exit program


#datafile = info['Data file']
instruction = info['Instruction']
#winsize = (info['Window size'], info['Window size'])
iti = info['ITI']



monitors = get_monitors()
screenRes = (monitors[0].width, monitors[0].height)

# Create gui window and mouse listener
win = visual.Window(fullscr=True, size = screenRes, color=(-1,-1,-1))
mouse = event.Mouse()

stim = visual.ImageStim(win, pos=(0, 0), autoLog=False, size=(1, 1.5))
intro = visual.TextStim(win, text='Next you will be shown a series of objects.\n\nDo your best to memorize their configuration and color, as well as their presentation order\n\nWhen you are ready to begin, press enter.', autoDraw=True)
stim.size *= .495

cross = visual.TextStim(win, text='+', pos =(0,0))
out = visual.TextStim(win, text= "Now you may take a 5 minute break. When you are ready to begin, press enter.")

stimOrder = np.random.permutation(range(obs))
win.flip()
intro.setAutoDraw(False)
event.waitKeys(keyList=['return', 'q'])


for i in range(obs):
    ob = ((pid + i) % obs) + 1
    color = randint(0,360)
    curob = colordict[ob][color]
    stim.setImage(stimDir + curob)
    stim.draw()
    win.flip()
    conn = sqlite3.connect(datFile)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stim_info (pid, obj, angle) VALUES (?,?,?)", (int(pid), int(ob), int(color)))
    
    conn.commit()
    conn.close()
    for key in event.getKeys():
        if key in ['escape', 'q']: # if q or escape quit program
            core.quit() 
    core.wait(5)
    cross.draw()
    win.flip()
    core.wait(3)
out.draw()
win.flip()
event.waitKeys(keyList=['return', 'q'])
win.flip()
core.wait(297)
core.quit()     
