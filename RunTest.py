# automatic kanji lookup
# answer returned from user and answer displayed can be different
# ui
# threshold for questions (all questions with less than 70% pass rate)
# automatically convert files ending in .txt to a json file and load that file
# when encountering a txt file, check for a corresponding json file first

import sys
from FileManagement import OpenJsonFile, ProcessJsonObj, OutputJsonFile
from Vocab import Quiz, EightsQuizFunction
from Parsing import ConvertFile

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
defaultFile = './Italian/Italian3.json'

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg.endswith('.txt'):
            ConvertFile(arg)
        elif arg.endswith('.json'):
            RunTest(arg)
else:
    RunTest(defaultFile)
