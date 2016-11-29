#!/usr/bin/python

from FileManagement import OutputJsonFile, ProcessJsonObj, OpenJsonFile
from Utility import GetTime, CutIntoLengths, ShuffleList, Clear
from itertools import islice

def AskQuestion(question,answer, alternateAnswers):
    """Ask the question, compare to answer, if doesn't match ask for verification"""
    userAnswer = input("Question: {0} ".format(question))
    exitTokens = ['X', 'EXIT', 'Q', 'QUIT']
    if(userAnswer.upper() in exitTokens and userAnswer not in exitTokens):
        return (None, alternateAnswers)
    # Get the alternate answers
    if(userAnswer not in ([answer] + alternateAnswers)):
        if userAnswer == '':
            print('Answer was: {0}'.format(answer))
            _ = input('Press any key to continue...')
            return (False, alternateAnswers)
        check = input("Answer was     : {0}\nYour answer was: {1}\nIs this correct? ".format(answer,userAnswer))
        if(check.upper() not in ['Y','YES', 'T', 'TRUE']):
            return (False, alternateAnswers)
        else:
            return (True, [userAnswer] + alternateAnswers)
    return (True, alternateAnswers)

def EightsQuizFunction(vocabWords):
    """Cut the quiz into eights, then quiz over each section until 100% accuracy"""
    session = dict()
    vocabWords = ShuffleList(vocabWords)
    def sortingFunction(x):
        if x['tried'] != 0:
            return x['failed'] / x['tried']
        else:
            return 1
    vocabWords.sort(key=sortingFunction,reverse=True)
    sections = [x for x in CutIntoLengths(vocabWords,8)]
    lengthOfSections = len(sections)
    for count,section in enumerate(sections):
        correctWords = dict([(x['question'],False) for x in section])

        def getWrongAnswers(s):
            for x in s:
                if correctWords[x['question']] == False:
                    yield x

        while(False in correctWords.values()):
            #wrongAnswers = [x for x in section if correctWords[x['question']] == False]
            wrongAnswers = [x for x in getWrongAnswers(section)]
            lastWrongAnswer = wrongAnswers[-1]
            section = ShuffleList(section)
            firstWrongAnswer = [x for x in getWrongAnswers(section)][0]
            if firstWrongAnswer == lastWrongAnswer:
                section = section[1:] + [lastWrongAnswer]
            Clear()
            print('{1} of {2} {0}%'.format(100.0 * count / lengthOfSections, count, lengthOfSections))
            for question in section:
                q = question["question"]
                alternateAnswers = [] if 'alternates' not in question else question['alternates']
                if(correctWords[q] == True):
                    continue
                (result, newAlternates) = AskQuestion(q, question['answer'], alternateAnswers)
                if q not in session.keys():
                    session[q] = {'tried' : 0, 'failed' : 0}
                if result == None:
                    return (session, vocabWords)
                elif result == False:
                    question['failed'] += 1
                    session[q]['failed'] += 1
                    correctWords[q] = False
                    while result == False:
                        if result != "":
                            Clear()
                        (result, newAlternates) = AskQuestion(q,question['answer'], alternateAnswers)
                else:
                    correctWords[q] = True
                question['tried'] += 1
                session[q]['tried'] += 1
                question['lastAsked'] = GetTime()
                question['alternates'] = newAlternates
    return (session, vocabWords)
            
def StandardQuizFunction(vocabWords):
    """Randomize list and iterate through the entire thing"""
    vocabWords = ShuffleList(vocabWords)
    for word in vocabWords:
        question = word['question']
        answer = word['answer']
        word['tried'] += 1
        # Get any alternate answers, that is answers that are not exact but were considered acceptable
        alternateAnswers = [] if 'alternates' not in word else word['alternates'] 
        userAnswer = input("Question: {0} ".format(question))
        if(userAnswer.upper() in ['X', 'EXIT', 'Q', 'QUIT']):
            break
        if(userAnswer != answer and userAnswer not in alternateAnswers):
            check = input("Answer was: {0}\nYour answer was: {1}\nIs this correct? ".format(answer,userAnswer))
            if(check.upper() in ['Y','YES', 'T', 'TRUE']):
                try:
                    word['alternates'].append(userAnswer)
                except:
                    word['alternates'] = [userAnswer]
            else:
                word['failed'] += 1
    return (vocabWords, vocabWords)

def Quiz(quizObj, quizFunction):
    session, quizObj['vocab'] = quizFunction(quizObj['vocab'])
    #sortedQuestions = sorted(quizObj['vocab'], key=lambda x: x['question'])
    attempted = [x for x in session.keys() if session[x]['tried'] > 0]
    for question in attempted:
        tried = session[question]['tried']
        succeeded = tried - session[question]['failed']
        print('"{0}": {1} of {2} ({3:.2%})'.format(question, succeeded, tried, succeeded * 1.0 / tried))
    totalAttempted = sum([session[x]['tried'] for x in attempted])
    totalFailed = sum([session[x]['failed'] for x in attempted])
    totalSucceeded = 0.0
    successPercentage = 0.0
    if totalAttempted > 0.0:
        if totalFailed > 0.0:
            totalSucceeded = totalAttempted - totalFailed
        successPercentage = totalSucceeded / totalAttempted
    totalTried = sum([session[x]['tried'] for x in attempted])
    totalWords = len(quizObj['vocab'])
    print('Total tried: {0} of {2} Percentage Success: {1:.2%}'.format(totalAttempted, successPercentage, totalWords))
    return quizObj
