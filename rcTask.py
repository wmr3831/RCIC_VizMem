# Details --------------------------------------------------------
#
# @details
# SCAPE Lab PxP Reverse Correlation task
# Experiment GUI for 2IFC reverse correlation task using PsychoPy
#
# @author Willow Rose (ejb3831@rit.edu)
#
# References ------------------------------------------------------
#
# @libraries
# Peirce, J. W., Gray, J. R., Simpson, S., MacAskill, M. R., Höchenberger, R., Sogo, H., Kastman, E., Lindeløv, J. (2019). PsychoPy2: experiments in behavior made easy. Behavior Research Methods. https://doi.org/10.3758/s13428-018-01193-y
#
# @examples
# Ron Dotsch. (2022). rcicr_examples. Python script. https://github.com/rdotsch/rcicr_examples
# Schmitz, M., Rougier, M., Yzerbyt, V. (Preprint, 2021). Introducing the Brief Reverse Correlation. http://dx.doi.org/10.31234/osf.io/xg693
#
# Parameters -------------------------------------------------------
#
# @param stimDir path to stimuli directory
# @param datFile output data file
# @param winSize size of experiment gui
# 
# Output -----------------------------------------------------------
# @return nothing, data saved to datFile
# Output data structure: {id: participant id, trial: current trial number, stim: stimulus number, oristimpath: path to original stimulus image, invstimpath: path to inverted stimulus image, response: stimulus selected}

# Setup ------------------------------------------------------------
# Load libraries
from psychopy import visual, event, core, gui
from psychopy.hardware import keyboard
from os import listdir, path, chdir
from screeninfo import get_monitors
import random
import numpy as np
import pandas
import sys
import sqlite3

# Set working directory
mainDir = path.dirname(path.abspath(sys.argv[0]))
chdir(mainDir)

# Set parameters
stimDir = './img/'
datFile = 'participant_data.db'
obs = 15
tests = 3
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

# Setup info dictionary
# @param Instruction text prompt to be displayed
# @param ITI inter-task interval duration
info = {'Instruction':'Which of these faces most resembles the face of a person you would imagine being affected by climate change?', 'Stimuli folder':stimDir, 'Data file':datFile,'ITI':0.5}

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

# Load all .png files in stimulus directory
stim = [f for f in listdir (stimulidir) if '.png' in f]
oridict = {i+1: {} for i in range(obs)}
invdict = {i+1: {} for i in range(obs)}



for item in stim:
    splt = item.split('_')
    stimnum = int(splt[0][4:])
    itemnum = int(splt[2])
    noise = splt[3][:3]
    if(noise == 'ori'):
        oridict[stimnum][itemnum] = item
    else:
        invdict[stimnum][itemnum] = item



    

stop = './Stop.jpg'


# Wait for instructions
intro = visual.TextStim(win, text='The following task will present you with two images.\n\nClick the image which is closest to the object as you remember it.\n\nIn cases where neither object looks particularly close, still do your best to choose the one closest to the object in memory.\n\nThere are 300 trials.', autoDraw=True)

win.flip()
event.waitKeys(keyList=['return', 'q'])
intro.setAutoDraw(False)


# Determine number of trials by dividing the number of stimuli loaded by 2
ntrials = int(len(stim) / (2 * obs) )

size = .7
# Set left and right stimulus location in gui window
stimLeft = visual.ImageStim(win, pos=(-0.5, -0.2), size=(1,1.5))
stimRight = visual.ImageStim(win, pos=(0.5, -0.2), size=(1,1.5))

stimLeft.size *= size
stimRight.size *= size

stopImg = visual.ImageStim(win, image=stop)

# Set instruction text location in gui window
reminderInstr = visual.TextStim(win, pos=(0, 0.7), wrapWidth=2)

# Autodraw instructions
reminderInstr.setAutoDraw(True)

# Randomize stimulus presentation order


# Generate random participant ID not already present in data file
#dataf = pandas.read_csv(datafile)
#ids = dataf['id'].tolist()
#pid = random.choice([x for x in range(1000) if x not in ids])

# Experiment -----------------------------------------------------



# Iterate through stimulus list to, should have 1 trial per stimulus pair
for i in range(tests):
    curob = ((pid + i) % obs) + 1
    
    stimOrder = np.random.permutation(range(ntrials))
    
    # @param tNum  current trial number
    tNum = 0
    ndict = {1:'first', 2:'second', 3:'third'}
    reminderInstr.setText("Which of these objects most resembles the " + ndict[i+1] +" object you were shown today?")
    print(stimOrder)
    for trial in stimOrder:
        
        # Increase trial count
        tNum+=1
        
        # Set original and inverted stimulus image which are stored sequentially in stim list
        oristimf = oridict[curob][trial+1]
        invstimf = invdict[curob][trial+1]
        
        
        # Randomize which side original/inverted stimulus appear on
        if random.randint(0,1) == 0:
            stimleftf = oristimf
            stimrightf = invstimf
        else:
            stimleftf = invstimf
            stimrightf = oristimf
        
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
        if selectedstim == oristimf: # if original selected, response = 1
            response = 1
        else: # if inverted selected, response = -1
            response = -1
        
        # Wait for mouse press to continue
        while mouse.getPressed()[0]:
            core.wait(0.01)
        
        # Create dataframe with trial data
        trialDat = pandas.DataFrame({'pid':[pid], 'trial':[tNum], 'stim':[trial+1], 'obj':[curob], 'oristimpath':[oristimf], 'invstimpath':[invstimf], 'response':[response]})
        
        # Append trial dataframe to data file
        conn = sqlite3.connect(datFile)
        cursor = conn.cursor()
        print(oristimf)
        cursor.execute("INSERT INTO rc_data (pid, trial, obj, stim, oristimpath, invstimpath, response) VALUES (?,?,?,?,?,?,?)", (int(trialDat['pid']), int(trialDat['trial']), int(trialDat['obj']), int(trialDat['stim']), str(oristimf), str(invstimf), int(trialDat['response'])))
        
        conn.commit()
        conn.close()
        # Wait for ITI before next trial
        core.wait(iti)

# Experiment end    
   

# Close gui window    
win.close() 
