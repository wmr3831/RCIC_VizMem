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
    validPid = False
    while not validPid:
        pidDlg = gui.Dlg()
        pidDlg.addField('PID:')
        pid = int(pidDlg.show()[0])
        if pidDlg.OK:
            validPid = True
            
monitors = get_monitors()
screenRes = (monitors[0].width, monitors[0].height)

# Create gui window and mouse listener
win = visual.Window(fullscr=True, size = screenRes, color=(-1,-1,-1))
textim = visual.ImageStim(win, pos=(0, 0), autoLog=False)
textim.setAutoDraw(True)
textim.size *= 2
textim.setImage('./debrief1.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./debrief2.png')
win.flip()
event.waitKeys(keyList=['return', 'q'])
textim.setImage('./debrief3.png')
win.flip()
response = event.waitKeys(keyList=['1', '2'])
conn = sqlite3.connect(datFile)
cursor = conn.cursor()

if '1' in response:
    cursor.execute("INSERT INTO debrief (pid, agree) VALUES (?,?)", (int(pid), 1))
    win.close()
    conn.commit()
    conn.close()
else:
    cursor.execute("INSERT INTO debrief (pid, agree) VALUES (?,?)", (int(pid), 0))
    win.close()
    conn.commit()
    conn.close()

