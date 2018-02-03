# automatic kanji lookup
# ui
# threshold for questions (all questions with less than 70% pass rate)
# automatically convert files ending in .txt to a json file and load that file
# when encountering a txt file, check for a corresponding json file first

import sys
from FileManagement import OpenJsonFile, ProcessJsonObj, OutputJsonFile
from Vocab import Quiz, EightsQuizFunction
from Parsing import ConvertFile
from os.path import isfile, isdir
from os import walk
import os

def RunTest(filename):
    print("Opening file: {0}".format(filename))
    jo = OpenJsonFile(filename)
    print("Processing file...")
    joPrime = ProcessJsonObj(jo)
    print("Making backup of the file to {0}.old".format(filename))
    OutputJsonFile(joPrime,filename + '.old')
    print("Starting test...")
    newWords = Quiz(joPrime, EightsQuizFunction)
    print("Recording results...")
    OutputJsonFile(newWords,filename)
    print("Done.")    

#file = "./KanjiByOldLevel/KanjiQuizLevel3.json"
#file = "./Vocabulary/N3.json"
#file = "./Genki2/Chapter13.json"
#file = './Genki2/Chapter14.json'
#file = './Genki2/Chapter13_AtTheBank.json'
#file = './Genki2/Chapter15.json'
#file = './Italian/Italian1.json'
#file = './Italian/Italian2.json'
#defaultFile = './Italian/Italian3.json'
recent_files_path = './recent_files.txt'
def get_recent_files():
    with open(recent_files_path,'r') as in_data:
        files = [x for x in in_data.read().split('\n') if x.strip() is not '']
        return files

def update_recent_files(files):
    with open(recent_files_path, 'w') as out_data:
        out_data.write('\n'.join(files))

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg.endswith('.txt'):
            ConvertFile(arg)
            print('Converted {0} to {1}'.format(arg, arg.replace('.txt', '.json')))
        elif arg.endswith('.json'):
            # open recent_files
            recent_files = get_recent_files()
            # check if the file is in there
            # if not, add it
            if arg not in recent_files:
                print(recent_files)
                print(recent_files[:9])
                print(arg)
                print([arg])
                update_recent_files(recent_files[-9:] + [arg])
            RunTest(arg)
        elif isdir(arg):
            (_,_,all_files) = next(walk(arg))
            files = [f for f in all_files if f.endswith('.json')]
            first_30_files = ['{0}: {1}'.format(i,f) for (i,f) in enumerate(files[:30])]
            sections = [[first_30_files[x] for x in range(i,i+3)] for i in range(0,30,3)]
            print('\n'.join(map(lambda x: '\t'.join(x),sections)))
            try:
                result = int(input('Enter selection: '))
                RunTest(os.path.join(arg, files[result]))
            except:
                pass
else:
    #RunTest(defaultFile)
    files = []
    if isfile(recent_files_path): 
        files = get_recent_files()
        print('--==((Recent Files))==--')
        for (selection, file) in enumerate(files):
            print('({0}): {1}'.format(selection, file))
    selection = input('Enter Selection: ')
    try:
        selection_as_number = int(selection)
        RunTest(files[selection_as_number])
    except:
        pass
