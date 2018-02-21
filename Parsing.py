from typing import Dict, Tuple, List
import FileManagement

#===========Parsing stuff, application specific================
def parseVocabularyList(x):
    with open(x,encoding='utf-8') as inData:
        lines = (x for x in inData.readlines())
        splitLines = (x.split('\t') for x in lines)
        for line in splitLines:
            if len(line) == 4:
                rv = [x.strip() for x in line]
                yield rv

def transformVocabularyListToJson(vl, listName):
    jsonFile = {"name" : listName}
    def convertVocabList(vl):
        def createEntry(question,answer):
            return {'question' : question, 'answer' : answer}
        for vocabLine in [x for x in vl][2:]:
            yield createEntry("Given the kanji \"{0}\" what is the definition?".format(vocabLine[0]), vocabLine[3])
            yield createEntry("Given the definition \"{0}\" what is the kanji?".format(vocabLine[3]),vocabLine[0])
            if(vocabLine[1].strip() != ''):
                yield createEntry("Given the kanji \"{0}\" what is the On reading(s)?".format(vocabLine[0]),vocabLine[1])
            if(vocabLine[2].strip() != ''):
                yield createEntry("Given the kanji \"{0}\" what is the Kun reading(s)?".format(vocabLine[0]), vocabLine[2])
    jsonFile['vocab'] = [x for x in convertVocabList(vl)]
    return jsonFile

def createEntry(question,answer):
        return {'question' : question, 'answer' : answer, 'tried' : 0, 'failed' : 0}

def generateQuestions(kanji, on, kun, definition):
    """Generate up to four questions based on the kanji, on, kun, and definition"""
    template = 'Given the {0} "{1}" what {3} the {2}?'
    definitionToken = ', '.join(definition)
    yield createEntry(template.format('kanji',kanji,'definition','is'),definitionToken)
    yield createEntry(template.format('definition',definitionToken,'kanji','is'),kanji)
    if(on != None):
        onToken = ', '.join(on)
        yield createEntry(template.format('kanji',kanji,'on readings','are'),onToken)
    if(kun != None):
        kunToken = ', '.join(kun)
        yield createEntry(template.format('kanji',kanji,'kun readings','are'),kunToken)

def parseDictionaryEntry(entry):
    """Given a dictionary entry generate a question"""
    kanji = entry['literal']
    kun = entry['kun']
    on = entry['on']
    definition = entry['meaning']
    if on == []:
        on = None
    if kun == []:
        kun = None
    yield from generateQuestions(kanji,on,kun,definition)

def parseDictionary(dictionary):
    """Give a dictionary object, parse each of its entries and generate questions"""
    for entry in dictionary:
        yield from parseDictionaryEntry(entry)

def generateVocabQuestion(kanji, kana, definition):
    """Given the kanji, kana (pronunciation) and definition produce a series of questions"""
    if kanji == kana: # sometimes the kana was appearing twice in the source files
        kanji = None
    if kanji != None:
        yield createEntry('What is the pronunciation of "{0}"?'.format(kanji),
                          "{0} ({1})".format(kana,definition))
        yield createEntry('What is the definition of "{0}"?'.format(kanji),
                          '{0} ({1})'.format(definition,kana))
        yield createEntry('Given the definition "{0}", what is the word?'.format(definition),
                          '{0} ({1})'.format(kanji,kana))
    if kanji == None:
        yield createEntry('What is the definition of "{0}"?'.format(kana), definition)
        yield createEntry('Given the definition "{0}", what is the word?'.format(definition),kana)

def loadVocabularyFile(filename):
    """Load a vocabulary file, and output arrays of tokens"""
    with open(filename,encoding='utf-8') as inData:
        lines = inData.readlines()
        tokens = (x.split('\t') for x in lines)
        cleanTokens = ([x.strip().replace('\ufeff','').replace(',',', ').replace('  ',' ') for x in y] for y in tokens)
        yield from cleanTokens

def parseVocab(lst):
    ll = len(lst)
    if ll == 3:
        yield from generateVocabQuestion(None, lst[1], lst[2])
    else:
        print('{0} is an invalid number of arguments for a vocab question.'.format(len(lst)))
        print(lst)

def parseKanji(lst):
    ll = len(lst)
    if ll == 4:
        yield from generateVocabQuestion(lst[1],lst[2],lst[3])
    else:
        print('{0} is an invalid number of arguments for a kanji question'.format(ll))
        print(lst)

def parseQuestion(lst):
    ll = len(lst)
    if ll == 3:
        yield createEntry(lst[1],lst[2])
    else:
        print('{0} is an invalid number of arguemnts for a question'.format(ll))
        print(lst)

parserDict = {
    'v': parseVocab,
    'k': parseKanji,
    'q': parseQuestion
    }

def convertVocabularyFile(filename):
    """Load a vocabulary file, and output vocab questions"""
    vocabFile = loadVocabularyFile(filename)
    firstLine = next(vocabFile)
    (version, title) = firstLine
    for line in vocabFile:
        if line[0] != '':
            yield from parserDict[line[0]](line)

def createVocabJsonObj(filename,testName):
    """Given a vocab file, generate a json test"""
    vocab = convertVocabularyFile(filename)
    jsonObj = {'name' : testName, 'vocab' : [x for x in vocab]}
    return jsonObj

def createTest(name: str, questions: List[Tuple[str,str]]) -> Dict[str,object]:
    '''Convert a name and a list of tuples into a test object'''
    vocab = [createEntry(q,a) for (q,a) in questions]
    return {'name': name, 'vocab': vocab}

def reparseAllTheVocabularyFiles():
    """Reparse all the files in ./Vocabulary"""
    folder = './Vocabulary/{0}'
    for x in range(3,6):
        inputFile = folder.format('N{0}.txt'.format(x))
        outputFile = folder.format('N{0}.json'.format(x))
        title = 'Japanese N{0} Vocabulary'.format(x)
        jsonObj = createVocabJsonObj(inputFile,title)
        FileManagement.OutputJsonFile(jsonObj,outputFile)

def ConvertFile(inputFilename, title=None):
    """Given an input filename, change the extension to .json and output"""
    outputFile = ''
    if inputFilename.endswith('.txt'):
        outputFile = inputFilename.replace('.txt','.json')
    else:
        outputFile = inputFilename + '.json'
    if title is None:
        title = outputFile
    jsonObj = createVocabJsonObj(inputFilename,title)
    FileManagement.OutputJsonFile(jsonObj, outputFile)    
