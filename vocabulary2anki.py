from dictionary.baiCiZhanDictionary import BaiCiZhanDictionary

class safesub(dict):
    def __missing__(self,key):
        return ""

def dict2anki(d,fmt):
    return fmt.format_map(safesub(d))

def vocabulary2anki(vocabulary,fmt):
    dictionary = BaiCiZhanDictionary()
    d = dictionary.search(vocabulary)
    return dict2anki(d,fmt)

if __name__ == "__main__":
    word = "hello"
    keys = ('{mean}','{acc}','{sentence_en}','{sentence_cn}','{img}','{mp3}')
    fmt = "|".join(keys)
    print(vocabulary2anki(word,fmt))
