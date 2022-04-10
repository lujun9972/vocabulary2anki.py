TMPFILE=`mktemp -t 1.2anki.sh.XXXXXX`
trap "rm $TMPFILE 2>/dev/null" 0
WORDS_FILE="words.txt"
WORDS_HISTORY_FILE="words.history"
function uniqFile()
{
    FILE="$1"
    sort ${FILE}|uniq >${TMPFILE}
    mv ${TMPFILE} ${FILE}
}
function editConfig()
{
    vim *.cfg
}
function fileMinus()
{
    diff $1 $2 |grep '<'|sed 's/^< //'
}
function inputWords()
{
    vim ${WORDS_FILE}
    uniqFile ${WORDS_FILE}
    fileMinus ${WORDS_FILE} ${WORDS_HISTORY_FILE} >${TMPFILE}
    mv ${TMPFILE} ${WORDS_FILE} 
}
uniqFile ${WORDS_HISTORY_FILE}
inputWords
editConfig
./vocabulary2anki.py ${WORDS_FILE} |tee /tmp/vocabulary.txt
echo 分离错误的记录
grep '.json$' /tmp/vocabulary.txt|sed 's/.json$//' |sed 's?.*/??'|sed 's/%20/ /g' |tee -a /tmp/vocabulary.fail
echo 分离正确的记录
grep -v '.json$' /tmp/vocabulary.txt |tee  /tmp/vocabulary.succ
# 已经完成的单词加入到 words.history 中
cut /tmp/vocabulary.succ -d'|' -f1 >>words.history
# 把成功和失败的从 words.txt 中去掉
cut /tmp/vocabulary.succ -d'|' -f1 >/tmp/vocabulary.txt
cat /tmp/vocabulary.fail >>/tmp/vocabulary.txt
uniqFile /tmp/vocabulary.txt
fileMinus ${WORDS_FILE} /tmp/vocabulary.txt >${TMPFILE}
mv ${TMPFILE} ${WORDS_FILE}
