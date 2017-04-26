import codecs
import docreader
import re
import sys
from collections import defaultdict
import simple9
import cPickle as pickle
import struct

SPLIT_RGX = re.compile(r'\w+', re.U)

def extract_words(text):
    words = re.findall(SPLIT_RGX, text)
    return map(lambda s: s.lower(), words)

myDict = dict()
urls = []
reader = docreader.DocumentStreamReader(docreader.parse_command_line().files)
# reader = docreader.DocumentStreamReader(['dataset/lenta.ru_159b9f4b-972b-48b1-8ec3-44fbd6be33c4_01.gz'])
for doc in reader:
#     print "%s\t%d bytes" % (doc.url, len(doc.text))
    urls.append(doc.url)
    for word in extract_words(doc.text):
        if myDict.get(word) != None:
            prev = myDict[word][-1]
            if prev != len(urls) - 1:
                myDict[word].append(len(urls) - 1)
        else:
            myDict[word] = [len(urls) - 1]


dict_file = open('dict', 'wb')
dict2 = dict()
pos = 0
for word in myDict:
    lst = simple9.simple9_encode_lst(myDict[word])
#    ss = word + ':' + ','.join(list(map(str, lst))) + '\n'
    ss = 0
    for x in lst:
        xx = struct.pack('L', x)
        dict_file.write(xx)
        ss += 1
#    print word, pos, ss, lst
    dict2[word] = (pos, ss)
    pos += ss * struct.calcsize('L')
#    dict_file.write(blst)
dict_file.close()

output = open('dict2.pkl', 'wb')
pickle.dump(dict2, output, 2)
output.close()

#urls_file = codecs.open('urls', 'w', 'utf-8')
#for url in urls:
#    ss = url + '\n'
#    urls_file.write(ss)
#urls_file.close()

output = open('urls.pkl', 'wb')
pickle.dump(urls, output, 2)
output.close()


# VARBYTE

def num_to_bytes(x):
    # x < 128
    res = ''
    for i in range(7):
        if x & (1 << i) > 0:
            res += '1'
        else:
            res += '0'
    res += '0'
    res = res[::-1]
    return res

def bytes_to_num(x):
    res = 0
    x = x[::-1]
    for i in range(len(x)):
        res += int(x[i]) * (1 << i)
    return res

def varbyte_encode(x):
    res = []
    while x > 0:
        cur = x % 128
        res.append(num_to_bytes(x))
        x /= 128
    res.reverse()
    res[0] = '1' + res[0][1:]    
    return ''.join(res)

def varbyte_decode(x):
    res = 0
    blocks = []
    for i in range(len(x) // 8):
        blocks.append(x[(i * 8):((i + 1) * 8)])
    blocks[0] = '0' + blocks[0][1:8]
    blocks.reverse()
    for i in range(len(blocks)):
        res += 128 ** i * bytes_to_num(blocks[i])
    return res

# print varbyte_encode(5)
# print varbyte_encode(128)
# print varbyte_encode(133)
# print varbyte_decode(varbyte_encode(5))
# print varbyte_decode(varbyte_encode(128))
# print varbyte_decode(varbyte_encode(133))


