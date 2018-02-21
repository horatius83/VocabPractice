# automatic kanji lookup
# ui
# threshold for questions (all questions with less than 70% pass rate)
# automatically convert files ending in .txt to a json file and load that file
# when encountering a txt file, check for a corresponding json file first

import sys
from typing import Iterable, List, Tuple
from FileManagement import OpenJsonFile, ProcessJsonObj, OutputJsonFile
from Vocab import Quiz, EightsQuizFunction
from Parsing import ConvertFile
from os.path import isfile, isdir
from os import walk
import os
import datetime
import json

def RunTest(filename: str) -> None:
    add_recent_file(filename)
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

#recent_files_path = './recent_files.txt'
recent_files_path = './recent_files.json'
def get_recent_files() -> List[Tuple[str, datetime.datetime]]:
    with open(recent_files_path,'r') as in_data:
        raw_list = in_data.read()
        if(raw_list != ''):
            json_obj = json.loads(raw_list, encoding='utf-8')
            for (file_path, str_datetime) in json_obj:
                yield (file_path, datetime.datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S.%f'))
        else:
            return []


def update_recent_files(files: Iterable[Tuple[str, datetime.datetime]]) -> None:
    with open(recent_files_path, 'w') as out_data:
        out_data.write(json.dumps([(f,str(dt)) for (f,dt) in files]))

def add_recent_file(most_recent_file: str) -> None:
    recent_files = list(get_recent_files())
    if most_recent_file not in [rf for (rf,_) in recent_files]:
        update_recent_files(recent_files[-9:] + [(most_recent_file, datetime.datetime.now())])

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg.endswith('.txt'):
            ConvertFile(arg)
            print('Converted {0} to {1}'.format(arg, arg.replace('.txt', '.json')))
        elif arg.endswith('.json'):
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
            except Exception as e:
                print(e)
else:
    files = []
    if isfile(recent_files_path): 
        files = list(get_recent_files())
        print('--==((Recent Files))==--')
        for (selection, file) in enumerate(files):
            print('({0}): {1}'.format(selection, file[0]))
    selection = input('Enter Selection: ')
    try:
        selection_as_number = int(selection)
        selected_file = files[selection_as_number]
        RunTest(selected_file[0])
    except Exception as e:
        print(e)
