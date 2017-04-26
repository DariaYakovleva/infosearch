import codecs
import re
import sys
from collections import defaultdict
import simple9
import myParser
import struct 

myDict = dict()
urls = []

#dict_file = codecs.open('dict','r', 'utf-8')
#for line in dict_file.readlines():
#    s = line.split(':')
#    word, nums = s[0], s[1]
#    nums = list(map(int, nums.split(',')))
#    nums = simple9.simple9_decode_lst(nums)
#    myDict[word] = nums
#dict_file.close()

import cPickle as pickle
input = open('dict2.pkl', 'rb')
dict2 = pickle.load(input)
input.close()


#urls_file = codecs.open('urls','r', 'utf-8')
#for line in urls_file.readlines():
#    s = line.strip()
#    urls.append(s)
#urls_file.close()

input = open('urls.pkl', 'rb')
urls = pickle.load(input)
input.close()


ff = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

for line in ff.readlines():  
#    query = [q.strip().lower() for q in line.split("&")]    
    print line.strip()
    expr = myParser.parse(line.lower())
#    print expr.toStr()
    result = expr.getUrls(dict2, len(urls))
    print len(result)
    for r in result:
        print urls[r]



