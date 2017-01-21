#!/usr/bin/env python3
from collections import defaultdict
import hashlib
from multiprocessing.dummy import Pool
from dictionary.baiCiZhanDictionary import BaiCiZhanDictionary
import sys

def dict2anki(d,fmt):
    d = defaultdict(lambda :"",d)
    img = d.get('img')
    mp3 = d.get('mp3')
    return fmt.format_map(d)

def vocabulary2anki(vocabulary,fmt):
    dictionary = BaiCiZhanDictionary()
    d = dictionary.search(vocabulary)
    return dict2anki(d,fmt)

if __name__ == "__main__":
    words = ("hello","world")
    keys = ('word','{mean}','{acc}','{sentence_en}','{sentence_cn}','{img}','{mp3}')
    fmt = "|".join(keys)
    pool = Pool(10)
    s = pool.map(lambda word:vocabulary2anki(word,fmt),words)
    print(s)
