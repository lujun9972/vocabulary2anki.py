#! env python3
from abc import ABCMeta
from abc import abstractmethod
class Dictionary(metaclass=ABCMeta):
    @abstractmethod
    def search(self,word):
        raise RuntmeError("Not a real Dictionary")
