from os import rename, listdir
import numpy as np

stimulidir = './img/'

stim = [f for f in listdir (stimulidir) if '.png' in f]

renamedict = {'1':'1', '2':'10', '3':'11', '4':'12', '5':'13', '6':'14', '7':'15', '8':'2', '9':'3', '10':'4', '11':'5', '12':'6', '13':'7', '14':'8', '15':'9'}

for item in stim:
    filename = item.split('_')
    filename.pop(0)
    stimname = filename.pop(0)
    number = stimname[4:]
    newname = "stim"+renamedict[number]
    filename = np.insert(filename, 0, newname)
    final = "_".join(x for x in filename)
    rename(stimulidir+item, stimulidir+final)
    