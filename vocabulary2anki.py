#!/usr/bin/env python3
import os
import os.path
from collections import defaultdict
import hashlib
from multiprocessing.dummy import Pool
import sys
import argparse
from urllib import request
from dictionary.jsonDictionary import JsonDictionary
import fileinput

def download_for_anki(url):
    if not url:
        return ""
    try:
        fileext = os.path.splitext(url)[1]
        filename = hashlib.md5(url.encode()).hexdigest() + fileext
        filepath = os.path.join("collection.media",filename)
        if not os.path.exists("collection.media"):
            os.makedirs("collection.media")
        request.urlretrieve(url,filepath)
        if fileext in ('jpg','jpeg','gif','png','svg'):
            filename =  '<img src="{}"></img>'.format(filename)
        elif fileext in ('mp3','mp4','wav'):
            filename = '[sound:{}]'.format(filename)
    except Exception as e:
        print("fetch {} error:{}".format(url,e),file=sys.stderr)
        filename = ""
    return filename

def dict2anki(d,fmt):
    d = defaultdict(lambda :"",d)
    d['img'] = download_for_anki(d.get('img'))
    # d['img'] = img and '<img src="{}"></img>'.format(img)
    d['mp3'] = download_for_anki(d.get('mp3'))
    # d['mp3'] = mp3 and '[sound:{}]'.format(mp3)
    return fmt.format_map(d)

def vocabulary2anki(vocabulary,fmt):
    dictionary = JsonDictionary('http://mall.baicizhan.com/ws/search?w={}','mean_cn',r'；\s+','accent','st','sttr','http://baicizhan.qiniucdn.com/word_audios/{}.mp3','img')
    d = dictionary.search(vocabulary)
    return dict2anki(d,fmt)

if __name__ == "__main__":
    # 解析参数
    parser = argparse.ArgumentParser(description='查询单词意义,并以anki可以导入的方式输出')
    parser.add_argument(dest='source_file',metavar='source_file',nargs='*',help='存放单词的源文件,每行一个词,如果不填,则会从标准输入读取单词')
    parser.add_argument('-o',dest='dest_file',metavar='dest_file',action='store',help='存放结果的目标文件,如果省略,则会写入到标准输出中')
    parser.add_argument('--fmt',dest='fmt',action='store',metavar='format',help='指定输出的格式,其中{word},{mean},{accent},{sentence_en},{sentence_cn},{img},{mp3}会被替换,默认值为"{word}|{mean}|{accent}|{sentence_en}|{sentence_cn}|{img}|{mp3}"')
    args = parser.parse_args()

    if len(args.source_file) == 0:
        source_file = sys.stdin
    else:
        source_file = fileinput.input(args.source_file)

    if args.dest_file:
        dest_file = open(args.dest_file,'w')
    else:
        dest_file = sys.stdout

    if args.fmt:
        fmt = args.fmt
    else:
        keys = ('{word}','{mean}','{accent}','{sentence_en}','{sentence_cn}','{img}','{mp3}')
        fmt = "|".join(keys)

    words = []
    for line in source_file:
        words.append(line)
    words = map(lambda word:word.strip(),words)
    pool = Pool(10)
    records = pool.map(lambda word:vocabulary2anki(word,fmt),words)
    for record in records:
        print(record,file=dest_file)
    source_file.close()
    dest_file.close
