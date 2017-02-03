#!/usr/bin/env python3
import os
import os.path
from collections import defaultdict
import hashlib
from multiprocessing.dummy import Pool
import sys
import argparse
from urllib import request
import fileinput
import configparser
import functools
from dictionary.jsonDictionary import JsonDictionary
from dictionary.xmlDictionary import XmlDictionary



def get_instance_by_conf(d):
    type = d['type']
    del d['type']
    if type == 'xml':
        return XmlDictionary(**d)
    elif type == 'json':
        return JsonDictionary(**d)
    else:
        raise RuntimeError('未实现的字典类型:{}'.format(type))

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
        if fileext in ('.jpg','.jpeg','.gif','.png','.svg'):
            filename =  '<img src="{}"></img>'.format(filename)
        elif fileext in ('.mp3','.mp4','.wav'):
            filename = '[sound:{}]'.format(filename)
    except Exception as e:
        print("fetch {} error:{}".format(url,e),file=sys.stderr)
        filename = ""
    return filename

def dict2AnkiRecord(d,fmt):
    d = defaultdict(lambda :"",d)
    if '{img}' in fmt:
        d['img'] = download_for_anki(d.get('img'))
        # d['img'] = img and '<img src="{}"></img>'.format(img)
    if '{mp3}' in fmt:
        d['mp3'] = download_for_anki(d.get('mp3'))
        # d['mp3'] = mp3 and '[sound:{}]'.format(mp3)
    return fmt.format_map(d)

def vocabulary2AnkiRecord(vocabulary,fmt):
    conf = configparser.ConfigParser()
    conf.read('vocabulary2anki.cfg')
    sections = conf.sections()
    dictionary_confs = map(lambda sec:dict(conf.items(sec)),sections)
    dictionaries = map(get_instance_by_conf,dictionary_confs)
    dicts = map(lambda dictionary:dictionary.search(vocabulary),dictionaries)
    d = {}
    for dic in dicts:
        d.update(dic)
    return dict2AnkiRecord(d,fmt)

def writeRecordsToFile(records,dest_file):
    if dest_file:
        dest_file = open(dest_file,'w')
    else:
        dest_file = sys.stdout
    for record in records:
        print(record,file=dest_file)
    dest_file.close()

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
    records = pool.map(lambda word:vocabulary2AnkiRecord(word,fmt),words)
    writeRecordsToFile(records,args.dest_file)
    source_file.close()
