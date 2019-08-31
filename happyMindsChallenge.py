from flask import Flask, request
import string
import pyrebase
import json
from firebase.firebase import FirebaseApplication


'''
Database used : Firebase,
Reaseon : Firebase will not allow duplication of keys, so even if there are repeated words in 2 different
files there is no need to handle the exception that occurs due to the duplication of keys. The database
itself will handle these by over writing the old key word
'''

config = {
    "apiKey": "AIzaSyCNmP6Lva6TO0bLhW13jvK_zQ2REZWq5ww",
    "authDomain": "hiringchallenge.firebaseapp.com",
    "databaseURL": "https://hiringchallenge.firebaseio.com",
    "projectId": "hiringchallenge",
    "storageBucket": "",
}

firebase = pyrebase.initialize_app(config)
database = FirebaseApplication(config['databaseURL'])
app = Flask(__name__)

@app.route("/acceptfile", methods = ['POST'])
def acceptFile():
    """
    MethodName : acceptFile,
    url : http://server.com/acceptfile,
    methods : POST,
    data accepted : Multipart file,
    return value : A string which says the file is uploaded,
    Description : This method accepts a file and parses the file to get the contents of the file in the form of a string, 
    the punctuations in the text file is removed and the string is converted into a list. 
    To get only the unique words that are present in the file the property of sets is used.
    All the words are convereted to lower case so the case of the word doesn't make a difference.
    The list of all the unique words present in the file is converted into a dictonary and saved in firebase DB.
    """
    dictToUpload = {}
    fileData = request.files['file']
    listOfWords = fileData.read().decode('UTF-8').lower().translate(str.maketrans('', '', string.punctuation)).split()
    listOfUniqueWords = list(set(listOfWords))
    for words in listOfUniqueWords:
        dictToUpload[words] = "meaning"
    db = firebase.database()
    db.child("listOfWords").set(dictToUpload)
    return "File uploaded successfully"

@app.route("/getwordstatus", methods = ['GET', 'POST'])
def getwordstatus():
    '''
    MethodName : getwordstatus,
    url : http://server.com/getwordstatus,
    methods : GET, POST,
    data accepted : plain/text - a word to be searched,
    return value : bool (TRUE or FALSE),
    Description : This function accepts a word as an input. Pulls all the words that are present in the database.
    Checks if the given word is present in the database and returns true or false base on the result of the check.
    '''
    wordToBeFound = request.data.decode('UTF-8').lower()
    wordsInDb = database.get("/listOfWords", None)
    return str(wordToBeFound in wordsInDb)

if __name__ == "__main__":
    app.run(debug = True)