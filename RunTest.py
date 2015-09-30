# automatic kanji lookup
# answer returned from user and answer displayed can be different
# ui
# threshold for questions (all questions with less than 70% pass rate)
# automatically convert files ending in .txt to a json file and load that file
# when encountering a txt file, check for a corresponding json file first

from FileManagement import OpenJsonFile, ProcessJsonObj, OutputJsonFile
from Vocab import Quiz, EightsQuizFunction

def RunTest(filename):
    print("Opening file: {0}".format(file))
    jo = OpenJsonFile(file)
    print("Processing file...")
    joPrime = ProcessJsonObj(jo)
    print("Making backup of the file to {0}.old".format(file))
    OutputJsonFile(joPrime,file + '.old')
    print("Starting test...")
    newWords = Quiz(joPrime, EightsQuizFunction)
    print("Recording results...")
    OutputJsonFile(newWords,file)
    print("Done.")    

#file = "./KanjiByOldLevel/KanjiQuizLevel3.json"
#file = "./Vocabulary/N3.json"
#file = "./Genki2/Chapter13.json"
#file = './Genki2/Chapter14.json'
#file = './Genki2/Chapter13_AtTheBank.json'
#file = './Genki2/Chapter15.json'
#file = './Italian/Italian1.json'
#file = './Italian/Italian2.json'
file = './Italian/Italian3.json'

RunTest(file)
