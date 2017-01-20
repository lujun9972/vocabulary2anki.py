import json
from urllib import request
from dictionary import Dictionary

class BaiCiZhanDictionary(Dictionary):
    def search(self,word):
        url = "http://mall.baicizhan.com/ws/search?w={}".format(word)
        response = request.urlopen(url)
        explains = response.read()
        explains = json.loads(explains)
        result = {}
        result["img"]= explains.get('img')
        result["mean"] = explains.get('mean_cn')
        result["sentence_en"] = explains.get('st')
        result["sentence_cn"] = explains.get('sttr')
        result["accent "]= explains.get('accent')
        result["mp3 "]= "http://baicizhan.qiniucdn.com/word_audios/{}.mp3".format(word)
        return result
