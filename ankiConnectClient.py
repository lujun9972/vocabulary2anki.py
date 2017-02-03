import json
from urllib import request,parse

class AnkiConnectClient:
    def __init__(self,url="http://127.0.0.1:8765"):
        self.url = url
    def _request(self,action,params):
        "Commuicate with AnkiConnect. PARAMS should be a dict"
        data = {"action":action,"params":params}
        querystring = json.dumps(data)
        resp = request.urlopen(self.url,querystring.encode('ascii'))
        return json.loads(resp.read())
    def getDecks(self):
        "list decks"
        return self._request("deckNames",{})
    def getModels(self):
        "list models"
        return self._request("modelNames",{})
    def getModelFields(self,model):
        "list fields in MODEL"
        return self._request("modelFieldNames",{"modelName":model})
    def addNote(self,deck,model,fields):
        '''add a note to DECK
        MODEL specify the format of the note.
        FIELD-ALIST specify the content of the note. '''
        return self._request("addNote",{"note":{"deckName":deck,
                                                "modelName":model,
                                                "fields":fields,
                                                "tags":[]}})

if __name__ == "__main__":
    anki = AnkiConnectClient()
    decks = anki.getDecks()
    print(decks)
    models = anki.getModels()
    print(models)
    model = models[-1]
    fields = anki.getModelFields(model)
    print(fields)
