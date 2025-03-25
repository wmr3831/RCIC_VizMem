import copy
import errno
import json
import math
from screeninfo import get_monitors
from os import listdir, path, chdir, getcwd
import pandas
import random
import sys
import sqlite3

import numpy as np

from psychopy import visual, event, core, gui, tools, logging

logging.console.setLevel(logging.CRITICAL)


def convert_color_value(color):
    """Converts a list of 3 values from 0 to 255 to -1 to 1.

    Parameters:
    color -- A list of 3 ints between 0 and 255 to be converted.
    """

    return [round(((n/127.5)-1), 2) for n in color]

def load_color_wheel(path):
    """
    Loads the json color wheel file.

    Parameters:
        path -- Str or Path of the json file.
    """
    with open(path) as f:
        color_wheel = json.load(f)

    color_wheel = [convert_color_value(i) for i in color_wheel]

    return np.array(color_wheel)

def draw_color_wheels(window, wheel, size, rotation):
    """
    Draws color wheels at stimuli locations with random rotation.

    Parameters:
        coordinates -- A list of (x, y) tuples
        wheel_rotations -- A list of 0:359 ints describing how much each wheel
            should be rotated.
    """
    mask = np.zeros([100, 1])
    mask[-30:] = 1

    
    rotated_wheel = np.roll(wheel, rotation, axis=0)
    tex = np.repeat(rotated_wheel[np.newaxis, :, :], 360, 0)

    visual.RadialStim(
        window, tex=tex, mask=mask, pos=[0,0], angularRes=360,
        angularCycles=1, interpolate=False, size=(1,1.5), autoLog=False).draw()


def calc_mouse_color(mouse_pos):
    """
    Calculates the color of the pixel the mouse is hovering over.

    Parameters:
        mouse_pos -- A position returned by mouse.getPos()
    """
    
    if mouse_pos[0] == 0 and mouse_pos[1] == 0:
        return 0
    
    
    angle = np.degrees(np.arctan2(-mouse_pos[1], mouse_pos[0]))
    
    
    
    # Ensure angle is positive and round to nearest whole degree
    angle = int(round(angle)) % 360
    return angle

mainDir = path.dirname(path.abspath(sys.argv[0]))
chdir(mainDir)


print(getcwd())
# Things you probably want to change
set_sizes = [1, 2, 4, 6]
trials_per_set_size = 5  # per block
number_of_blocks = 2
datFile = 'participant_data.db'
iti_time = 1
sample_time = 2
delay_time = 1
monitor_distance = 90
obs = 15

wheelpath = './colors.json'

experiment_name = 'ResolutionWR'
graydir = './grayStim/baseImgs/'
colordir = './colorStim/'

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

graystim = listdir (graydir)
colorstim = listdir (colordir)
colordict = {i+1: {} for i in range(obs)}
graydict = {}

# Setup info dictionary
# @param Instruction text prompt to be displayed
# @param ITI inter-task interval duration
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

for item in graystim:
    splt = item.split('_')
    
    stimnum = int(splt[1][:-4])
    graydict[stimnum] = item

for item in colorstim:
    splt = item.split('_')
    stimnum = int(splt[0][5:])
    angle = int(splt[2][:-4])
    colordict[stimnum][angle] = item
    


# Wait for instructions
intro = visual.TextStim(win, text='The following task will present you with an object inside a color ring.\n\nMoving the mouse around the ring will change the color of the object. \n\n Do you best to match the objects color to how it was before.', autoDraw=True, autoLog=False)

win.flip()
event.waitKeys(keyList=['return', 'q'])
intro.setAutoDraw(False)


# Determine number of trials by dividing the number of stimuli loaded by 2

size = 1.5
# Set left and right stimulus location in gui window
stim = visual.ImageStim(win, pos=(0, 0), autoLog=False, size=(1, 1.5))
#basestim = visual.ImageStim(win, pos=(0, 0), autoLog=False, size=(1, 1.5))
wheel = load_color_wheel(wheelpath)


#basestim.size *= .5
stim.size *= .495



stimOrder = np.random.permutation(range(obs))



win.flip()
tNum = 0

for trial in stimOrder:
    
    # Increase trial count
    tNum+=1
    
    
    # @param stimulus selected
    selected = False
    
    stim.setImage(graydir+graydict[trial+1])
    stim.draw()
    draw_color_wheels(win, wheel, 1, 55)
    mouse.setPos((0,0))
    initialpos = mouse.getPos()
    win.flip()
    while np.array_equal(np.array(mouse.getPos()), initialpos):
        core.wait(0.01)
    
    
    # Wait on input while stimulus not selected
    while not mouse.getPressed()[0]:
        
        # Check for key events
        
    
        
        stim.draw()
        
        angle = calc_mouse_color(mouse.getPos())
        stim.setImage(colordir+colordict[trial+1][angle])
        draw_color_wheels(win, wheel, 1, 55)
        
        
        for key in event.getKeys():
                if key in ['escape', 'q']: # if q or escape quit program
                    core.quit() 
        win.flip()
        
    while mouse.getPressed()[0]:
            core.wait(0.01)
    
    conn = sqlite3.connect(datFile)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO color_data (pid, trial, obj, response) VALUES (?,?,?,?)", (int(pid), int(tNum), int(trial+1), int(angle)))
    
    conn.commit()
    conn.close()
    
    
    
    
    # Wait for ITI before next trial
    core.wait(iti)

# Experiment end    

win.flip()

# Close gui window    
win.close() 
core.quit()