from urllib import request
import json
import re
from .dictionary import Dictionary

class BaiCiZhanDictionary(Dictionary):
    def search(self,word):
        url = "http://mall.baicizhan.com/ws/search?w={}".format(word)
        response = request.urlopen(url)
        explains = response.read()
        explains = json.loads(explains)
        result = {}
        result["img"]= explains.get('img')
        means = explains.get('mean_cn')
        result["mean"] = re.sub(r'；\s+','<br>',means)
        result["sentence_en"] = explains.get('st')
        result["sentence_cn"] = explains.get('sttr')
        result["accent"]= explains.get('accent')
        result["mp3"]= "http://baicizhan.qiniucdn.com/word_audios/{}.mp3".format(word)
        return result
