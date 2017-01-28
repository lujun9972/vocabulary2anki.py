import json
from urllib import request,parse

url = "http://127.0.0.1:8765"

def _request(action,params):
    "Commuicate with AnkiConnect. PARAMS should be a dict"
    data = {"action":action,"params":params}
    querystring = json.dumps(data)
    resp = request.urlopen(url,querystring.encode('ascii'))
    return json.loads(resp.read())

def getDecks():
    "list decks"
    return _request("deckNames",{})

def getModels():
    "list models"
    return _request("modelNames",{})

def getModelFields(model):
    "list fields in MODEL"
    return _request("modelFieldNames",{"modelName":model})

def addNote(deck,model,fields):
    '''add a note to DECK

MODEL specify the format of the note.
FIELD-ALIST specify the content of the note. '''

    return _request("addNote",{"note":{"deckName":deck,
                                       "modelName":model,
                                       "fields":fields,
                                       "tags":[]}})
