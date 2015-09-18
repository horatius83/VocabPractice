import os
import random
import time

def GetTime():
    """Get the current time as a dictionary"""
    return time.time()

#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def CutIntoLengths(lst, length):
    """ Yield successive n-sized chunks from lst"""
    for i in range(0,len(lst),length):
        yield lst[i:i+length]

def ShuffleList(lst):
    """Shuffle a given list"""
    r = random.Random()
    previousList = lst
    r.shuffle(lst)
    if len(previousList) > 1 and previousList[0] == lst[-1]:
        nl = lst[1:]
        nl.insert(r.randint(1,len(nl)),lst[0])
    return lst

def Clear():
    for x in range(0,80):
        print('')
        
