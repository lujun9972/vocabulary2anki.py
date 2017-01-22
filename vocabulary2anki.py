#!/usr/bin/env python3
from collections import defaultdict
import hashlib
from multiprocessing.dummy import Pool
from dictionary.baiCiZhanDictionary import BaiCiZhanDictionary
import sys
import argparse
import fileinput

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
    # 解析参数
    parser = argparse.ArgumentParser(description='查询单词意义,并以anki可以导入的方式输出')
    parser.add_argument(dest='source_file',metavar='存放单词的源文件',nargs='*',help='每行一个词,如果不填,则会从标准输入读取单词')
    parser.add_argument('-o',dest='dest_file',metavar='存放结果的目标文件',action='store',help='如果省略,则会写入到标准输出中')
    parser.add_argument('--fmt',dest='fmt',action='store',metavar='指定格式',help='其中{word},{mean},{accent},{sentence_en},{sentence_cn},{img},{mp3}会被替换"')
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
        keys = ('{word}','{mean}','{acc}','{sentence_en}','{sentence_cn}','{img}','{mp3}')
        fmt = "|".join(keys)

    words = source_file.readlines()
    words = map(lambda word:word.strip(),words)
    pool = Pool(10)
    records = pool.map(lambda word:vocabulary2anki(word,fmt),words)
    for record in records:
        print(record,file=dest_file)
    source_file.close()
    dest_file.close
