from psychopy import visual, event, core, gui
from psychopy.hardware import keyboard
from os import listdir, path, chdir
from screeninfo import get_monitors
import random
from math import floor, ceil
import numpy as np
import pandas
import sys
import sqlite3

# Set working directory
mainDir = path.dirname(path.abspath(sys.argv[0]))
chdir(mainDir)

# Set parameters
stimDir = './grayStim/'
datFile = 'participant_data.db'


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

# Setup info dictionary
# @param Instruction text prompt to be displayed
# @param ITI inter-task interval duration
info = {'Instruction':'Click the object which you were shown earlier.', 'Stimuli folder':stimDir, 'Data file':datFile,'ITI':0.5}

# Setup PsychoPy gui parameters
# @param title window title
#infoDlg = gui.DlgFromDict(dictionary=info, title='Prototype Task', order=['Instruction', 'Stimuli folder', 'Data file'])

# Check gui setup correct, if not exit program

stimulidir = info['Stimuli folder']
datafile = info['Data file']
instruction = info['Instruction']
#winsize = (info['Window size'], info['Window size'])
iti = info['ITI']

monitors = get_monitors()
screenRes = (monitors[0].width, monitors[0].height)

# Create gui window and mouse listener
win = visual.Window(fullscr=True, size = screenRes, color=(-1,-1,-1))
mouse = event.Mouse()

baseimgs = listdir (stimulidir + "baseImgs/")
rotateimgs = listdir (stimulidir + "rotated/")
swapimgs = listdir (stimulidir + "shapeSwap/")

basedir = {}
rotatedir = {}
swapdir = {}


for item in baseimgs:
    splt = item.split('_')
    stimnum = int(splt[1][:-4])
    basedir[stimnum] = item
    
for item in rotateimgs:
    splt = item.split('_')
    stimnum = int(splt[1][:-4])
    rotatedir[stimnum] = item

for item in swapimgs:
    splt = item.split('_')
    stimnum = int(splt[1][:-4])
    swapdir[stimnum] = item



ntrials = len(basedir)

stimOrder = np.random.permutation(range(ntrials))
if pid % 2 == 1:
    rtrials = stimOrder[ceil(ntrials/2):]
    strials = stimOrder[:floor(ntrials/2)]
else:
    rtrials = stimOrder[floor(ntrials/2):]
    strials = stimOrder[:ceil(ntrials/2)]

stimOrder = np.random.permutation(range(ntrials))
stop = './Stop.jpg'


# Wait for instructions
intro = visual.TextStim(win, text='The following task will present you with two objects.\n\nClick the object which you were shown earlier.', autoDraw=True)

win.flip()
event.waitKeys(keyList=['return', 'q'])
intro.setAutoDraw(False)


# Determine number of trials by dividing the number of stimuli loaded by 2

size = .7
# Set left and right stimulus location in gui window
stimLeft = visual.ImageStim(win, pos=(-0.5, -0.2), size=(1,1.5))
stimRight = visual.ImageStim(win, pos=(0.5, -0.2), size=(1,1.5))

stimLeft.size *= size
stimRight.size *= size

stopImg = visual.ImageStim(win, image=stop)

# Set instruction text location in gui window
reminderInstr = visual.TextStim(win, text=instruction, pos=(0, 0.7), wrapWidth=2)

# Autodraw instructions
reminderInstr.setAutoDraw(True)


tNum = 0
for trial in stimOrder:
        
    # Increase trial count
    tNum+=1
    
    # Set original and inverted stimulus image which are stored sequentially in stim list
    test = basedir[trial+1]
    if trial in rtrials:
        foil = rotatedir[trial+1]
        fpath = "rotated/"
        dtype = 1
    else:
        foil = swapdir[trial+1]
        fpath = "shapeSwap/"
        dtype = 0
    
    
    # Randomize which side original/inverted stimulus appear on
    if random.randint(0,1) == 0:
        stimleftf = "baseImgs/" + test
        stimrightf = fpath + foil
    else:
        stimleftf = fpath + foil
        stimrightf = "baseImgs/" + test
    
    # Set left stimulus image
    stimLeft.setImage(stimulidir + stimleftf)
    stimLeft.draw()
    
    # Set right stimulus image
    stimRight.setImage(stimulidir + stimrightf)
    stimRight.draw()
    
    # Update gui window
    win.flip()
    
    # @param stimulus selected
    selected = False
    
    # Wait on input while stimulus not selected
    while not selected:
        
        # Check for key events
        for key in event.getKeys():
                if key in ['escape', 'q']: # if q or escape quit program
                    core.quit() 
                elif key in ['1', 'e']: # if 1 or e select left stimulus
                    selected = 'left'
                    selectedstim = stimleftf
                elif key in ['0', 'i']: # if 0 or i select right stimulus
                    selected = 'right'
                    selectedstim = stimrightf
        
        # Check for mouse events
        if mouse.isPressedIn(stimLeft): # if left stimulus clicked select left stimulus
            selected = 'left'
            selectedstim = stimleftf
        elif mouse.isPressedIn(stimRight): # if right stimulus clicked select right stimulus
            selected = 'right'
            selectedstim = stimrightf
    
    # If stimulus selected, lower opacity of unselected stimulus
    if selected == 'left':
        stimRight.opacity = 0.25
    elif selected == 'right':
        stimLeft.opacity = 0.25
    stimRight.draw()
    stimLeft.draw()
    
    # Rerturn opacity to normal without drawing to setup next trial
    stimLeft.opacity = 1.0
    stimRight.opacity = 1.0
    
    # Update gui window
    win.flip()
    
    # Determine whether original or inverted stimulus was selected
    if selectedstim == test: # if original selected, response = 1
        response = 1
    else: # if inverted selected, response = -1
        response = -1
    
    # Wait for mouse press to continue
    while mouse.getPressed()[0]:
        core.wait(0.01)
    
    # Create dataframe with trial data
    trialDat = pandas.DataFrame({'pid':[pid], 'trial':[tNum], 'obj':[trial+1], 'dtype':[dtype], 'response':[response]})
    conn = sqlite3.connect(datFile)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fc_data (pid, trial, obj, dtype, response) VALUES (?,?,?,?,?)", (int(trialDat['pid']), int(trialDat['trial']), int(trialDat['obj']), int(trialDat['dtype']), str(trialDat['response'])))
    
    conn.commit()
    conn.close()
    # Append trial dataframe to data file
    
    # Wait for ITI before next trial
    core.wait(iti)
win.close()
