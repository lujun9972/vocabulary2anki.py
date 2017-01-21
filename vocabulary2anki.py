from dictionary.baiCiZhanDictionary import BaiCiZhanDictionary

def dict2anki(d,keys,sep='|'):
    vals = map(lambda key:d.get(key,""),keys)
    return sep.join(vals)

def vocabulary2anki(vocabulary,keys,sep='|'):
    dictionary = BaiCiZhanDictionary()
    d = dictionary.search(vocabulary)
    return dict2anki(d,keys,sep)

if __name__ == "__main__":
    word = "hello"
    keys = ('mean','accent','sentence_en','sentence_cn','img','mp3')
    print(vocabulary2anki(word,keys))
