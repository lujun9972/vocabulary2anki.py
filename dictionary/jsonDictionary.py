from urllib import request
from urllib import parse
import json
import re
from .dictionary import Dictionary

class JsonDictionary(Dictionary):
    @staticmethod
    def extract_from_dict(d,path):
        try:
            keys = path.split('.')
        except Exception:
            keys = path
        try:
            for key in keys:
                if key.isdigit() and isinstance(d,list):
                    d = d[int(key)]
                else:
                    d = d.get(key,"")
        except Exception:
            d = ""
        return re.sub("[\n\r]+","<br>",d)

    def search(self,word):
        quoted_word = parse.quote(word,safe='')
        url = self.url.format(quoted_word)
        try:
            response = request.urlopen(url)
        except Exception:
            print("query:{}".format(url))
            raise
        explains = response.read().decode('utf8')
        explains = json.loads(explains)
        result = {}
        result['word'] = word
        means = self.extract_from_dict(explains,self.means)
        if self.mean_sep:
            result["mean"] = re.sub(self.mean_sep,'<br>',means)
        else:
            result["mean"] = means
        result["sentence_en"] = self.extract_from_dict(explains,self.sentence_en)
        result["sentence_en"] = re.sub(r'({})'.format(re.escape(word)),r'<b>\1</b>',result["sentence_en"],0,re.I)
        result["sentence_cn"] = self.extract_from_dict(explains,self.sentence_cn)
        result["accent"] = self.extract_from_dict(explains,self.accent)
        if parse.urlparse(self.mp3).scheme == '':
            result["mp3"] = self.extract_from_dict(explains,self.mp3)
        else:
            result["mp3"] = self.mp3.format(quoted_word)
        if parse.urlparse(self.img).scheme == '':
            result["img"] = self.extract_from_dict(explains,self.img)
        else:
            result["img"] = self.img.format(quoted_word)
        return self.clean_dict(result)
