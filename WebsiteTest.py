from FileManagement import OpenJsonFile, ProcessJsonObj, OutputJsonFile
from Vocab import Quiz, EightsQuizFunction
from bottle import get, post, run, template, request, view

filename = './Genki2/Chapter15.json'
testData = ProcessJsonObj(OpenJsonFile(filename))
questions = testData['vocab']
vocabularyIndex = 0
question = questions[vocabularyIndex]

def OutputQuestion(question):
    return '''
       <b>{0}</b>
       <form method="POST" action="/test">
          <input name="answer" type="text" />
          <input type="submit" />
       </form>'''.format(question)

@get('/test')
@view('ask_question')
def index():
    return {'title' : 'Testing...',
            'question' : question['question']}
    #return OutputQuestion(question['question'])

@post('/test')
def SubmitLogin():
    global question
    correctAnswer = question['answer']
    print("correctAnswer: " + correctAnswer)
    answer = request.forms.answer
    if(answer != None and answer.strip() != ""):
        if(answer == correctAnswer):
            return '<h1>Correct!</h1>'
        else:
            return '''The correct answer was "<b>{0}</b>".<br/>
                      Your answer was: "<b>{1}</b>"</b>
                      <form method="POST" action="/test">
                      The answer was:
                          <input name="CorrectButton" type="submit" value="Correct" />
                          <input name="IncorrectButton" type="submit" value="Incorrect" />
                          <input name="QuitButton" type="submit" value="Quit" />
                      </form>'''.format(correctAnswer,answer)
    else:
        global vocabularyIndex
        global question
        correctButton = request.forms.get('CorrectButton')
        incorrectButton = request.forms.get('IncorrectButton')
        quitButton = request.forms.get('QuitButton')
        if correctButton != None:
            vocabularyIndex += 1
            question = questions[vocabularyIndex]
            return '<h1>Correct!</h1><br/>' + OutputQuestion(question['question'])
        elif quitButton != None:
            return 'quit'
        else:
            return '''<h1>Incorrect</h1>
       <b>{0}</b>
       <form method="POST" action="/test">
          <input name="answer" type="text" />
          <input type="submit" />
       </form>'''.format(question['question']) 
        
run(host='localhost', port=8383)
