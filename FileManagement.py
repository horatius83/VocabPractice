import json

def OpenJsonFile(filename):
    """Open a file and return the json object or None if an exception occurs"""
    with open(filename,encoding='utf-8') as inData:
        print('opened...')
        txt = inData.read()
        print('read...')
        return json.loads(txt)
    return None
    
def OutputJsonFile(jsonObj,filename):
    """Output a JSON object to the given filename"""
    with open(filename,encoding='utf-8',mode='w') as outData:
        json.dump(jsonObj,outData,ensure_ascii=False,indent=4,sort_keys=True)
    
def tryOrGet(op, default):
    """return the result of op or the default"""
    try:
        return op()
    except:
        return default

def ProcessJsonObj(jsonObj):
    """Get a json object and convert it into a version with statistics"""
    newJsonObj = {'name' : jsonObj['name']}
    def modifyJsonList(vocabWords):
        for vocabWord in vocabWords:
            if 'kanji' in vocabWord.keys():
                kanji, hiragana, definition = vocabWord['kanji']
                yield {'question' : kanji, 'answer' : "({0}) {1}".format(hiragana, definition), 'tried' : 0, 'failed' : 0}
                yield {'question' : hiragana, 'answer' : "({0}) {1}".format(kanji,definition), 'tried' : 0, 'failed' : 0}
                yield {'question' : definition, 'answer' : "({0}) {1}".format(kanji,hiragana), 'tried' : 0, 'failed' : 0}
            elif 'vocab' in vocabWord.keys():
                word, definition = vocabWord['vocab']
                yield {'question' : word, 'answer' : definition, 'tried' : 0, 'failed' : 0}
                yield {'question' : definition, 'answer' : word, 'tried' : 0, 'failed' : 0}
            elif 'question' in vocabWord.keys():
                if 'tried' not in vocabWord.keys():
                    vocabWord['tried'] = 0
                if 'failed' not in vocabWord.keys():
                    vocabWord['failed'] = 0
                yield vocabWord
    newJsonObj['vocab'] = [x for x in modifyJsonList(jsonObj['vocab'])]
    return newJsonObj
