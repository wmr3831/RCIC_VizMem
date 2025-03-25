from psychopy import visual, event, core, gui
from psychopy.hardware import keyboard
from os import listdir, path, chdir, system
from screeninfo import get_monitors
import random
import numpy as np
import pandas
import sys
import sqlite3


datFile = 'participant_data.db'
# Set working directory
mainDir = path.dirname(path.abspath(sys.argv[0]))
chdir(mainDir)

if len(sys.argv) > 1:
    pid = int(sys.argv[1])
else:
    conn = sqlite3.connect(datFile)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM p_log
        ORDER BY pid DESC
        LIMIT 1
    ''')
    
    row = cursor.fetchone()

    conn.close()
    if row == None:
        pid = 0
    else:
        pid = int(row[0]) + 1
    #print(pid)
            
monitors = get_monitors()
screenRes = (monitors[0].width, monitors[0].height)

# Create gui window and mouse listener
win = visual.Window(fullscr=True, size = screenRes, color=(-1,-1,-1))
intro = visual.TextStim(win, text='Throughout the whole experiment, press enter when you have finished reading all text on the screen to move on.', autoDraw=True)
textim = visual.ImageStim(win, pos=(0, 0), autoLog=False)
textim.size *= 2
win.flip()
event.waitKeys(keyList=['return', 'q'])
intro.setAutoDraw(False)
textim.setAutoDraw(True)
textim.setImage('./consent1.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./consent2.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./consent3.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./consent4.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./consent5.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./consent6.png')
win.flip()



response = event.waitKeys(keyList=['y', 'n'])
conn = sqlite3.connect(datFile)
cursor = conn.cursor()

if 'y' in response:
    cursor.execute("INSERT INTO p_log (pid, consent) VALUES (?,?)", (int(pid), 1))
    win.close()
    
    conn.commit()
    conn.close()
    system("python ./presentStim.py " + str(pid))
    system("python ./rcTask.py " + str(pid))
    system("python ./2afcTask.py " + str(pid))
    system("python ./colorTask.py " + str(pid))
    system("python ./debrief.py " + str(pid))
else:
    cursor.execute("INSERT INTO p_log (pid, consent) VALUES (?,?)", (int(pid), 0))
    win.close()
    conn.commit()
    conn.close()