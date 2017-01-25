from urllib import request
from urllib import parse
from xml.etree import ElementTree
import re
from .dictionary import Dictionary

class XmlDictionary(Dictionary):

    @staticmethod
    def extract_from_element_tree(tree,xpath):
        if not xpath:
            return ""
        nodes = tree.findall(xpath)
        texts = map(lambda node:node.text,nodes)
        texts = map(lambda text:re.sub("[\n\r]+","<br>",text),
                    texts)
        return "<p>".join(texts)

    def search(self,word):
        quoted_word = parse.quote(word,safe='')
        url = self.url.format(quoted_word)
        try:
            response = request.urlopen(url)
        except Exception:
            print("query:{}".format(url))
            raise
        # explains = response.read()
        explains = ElementTree.parse(response)
        result = {}
        result['word'] = word
        means = self.extract_from_element_tree(explains,self.means)
        if self.mean_sep :
            result["mean"] = re.sub(self.mean_sep,'<br>',means)
        else:
            result["mean"] = means

        result["sentence_en"] = self.extract_from_element_tree(explains,self.sentence_en)
        result["sentence_en"] = re.sub(r'({})'.format(re.escape(word)),r'<b>\1</b>',result["sentence_en"],0,re.I)
        result["sentence_cn"] = self.extract_from_element_tree(explains,self.sentence_cn)
        result["accent"] = self.extract_from_element_tree(explains,self.accent)
        if parse.urlparse(self.mp3).scheme == '':
            result["mp3"] = self.extract_from_element_tree(explains,self.mp3)
        else:
            result["mp3"] = self.mp3.format(quoted_word)
        if parse.urlparse(self.img).scheme == '':
            result["img"] = self.extract_from_element_tree(explains,self.img)
        else:
            result["img"] = self.img.format(quoted_word)
        return self.clean_dict(result)

if __name__ == "__main__":
    x = XmlDictionary('http://dict.youdao.com/fsearch?client=deskdict&keyfrom=chrome.extension&pos=-1&doctype=xml&xmlVersion=3.2&dogVersion=1.0&vendor=unknown&appVer=3.1.17.4208&le=eng&q={}','.//custom-translation/translation/content',accent='.//phonetic-symbol',mp3='http://dict.youdao.com/dictvoice?audio={}&type=2')
    print(x.search("hello"))
