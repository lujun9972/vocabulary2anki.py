#! env python3
from abc import ABCMeta
from abc import abstractmethod
class Dictionary(metaclass=ABCMeta):
    def __init__(self,url,means,mean_sep=r'',accent='',sentence_en='',sentence_cn='',mp3='',img=''):
        self.url = url
        self.img = img
        self.means = means
        self.mean_sep = mean_sep
        self.sentence_en = sentence_en
        self.sentence_cn = sentence_cn
        self.accent = accent
        self.mp3 = mp3
    @abstractmethod
    def search(self,word):
        raise RuntmeError("Not a real Dictionary")
