import MeCab
import sys
import re
from collections import Counter

infile = "/home/ymaki/Investigation-workspace/Phycho/res/discourse/UGM007-1_2Kana.txt"
with open(infile, encoding="utf-8") as f:
    data = f.read()

texts = data.split('\n')
for text in texts:
    text = text.split("(")[0][3:] if  text.startswith("○") else text.split("(")[0]
    if(len(text) < 1):
        continue

    print(text)
    parse = MeCab.Tagger().parse(text)
    print(parse)
    print("=======================")



    parse1 = MeCab.Tagger("-Ochasen").parse(text)
    print(parse1)
    print("*************************")
    # lines = parse.split("\n")
    # items = (re.split('[\t,]', line) for line in lines)

    # for item in items:
    #     print("i"+str(item))