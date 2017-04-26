#!/usr/bin/env python

"""
This just a draft for homework 'near-duplicates'
Use MinshinglesCounter to make result closer to checker
"""

import sys
import re
#import mmh3
from docreader import DocumentStreamReader


class MinshinglesCounter:
    SPLIT_RGX = re.compile(r'\w+', re.U)

    def __init__(self, window=5, n=20):
        self.window = window
        self.n = n

    def count(self, text):
        words = MinshinglesCounter._extract_words(text)
        shs = self._count_shingles(words)
        mshs = self._select_minshingles(shs)

        if len(mshs) == self.n:
            return mshs

        if len(shs) >= self.n:
            return sorted(shs)[0:self.n]

        return None

    def _select_minshingles(self, shs):
        buckets = [None] * self.n
        for x in shs:
            bkt = x % self.n
            buckets[bkt] = x if buckets[bkt] is None else min(buckets[bkt], x)

        return filter(lambda a: a is not None, buckets)

    def _count_shingles(self, words):
        shingles = []
        for i in xrange(len(words) - self.window):
#            h = mmh3.hash(' '.join(words[i:i+self.window]).encode('utf-8'))
            h = hash(' '.join(words[i:i+self.window]).encode('utf-8'))
            shingles.append(h)
        return sorted(shingles)

    @staticmethod
    def _extract_words(text):
        words = re.findall(MinshinglesCounter.SPLIT_RGX, text)
        return words


def main():
    mhc = MinshinglesCounter()

    ids = []
    for path in sys.argv[1:]:
        for doc in DocumentStreamReader(path):
#            print "%s (text length: %d, minhashes: %s)" % (doc.url, len(doc.text), mhc.count(doc.text))
            lst = mhc.count(doc.text)
            if lst != None:
                for x in lst:
                    ids.append((x, doc.url))
#    print(len(ids))  
    ids = list(set(ids))
    ids.sort()
#    print(len(ids))  
    ids2 = []

    mm = []
    for i in range(len(ids)):
        cur_sh = ids[i][0]
        cnt = 1
        while i + cnt < len(ids) and ids[i + cnt][0] == cur_sh:
            cnt += 1
        mm.append(cnt)

    mm.append(0)
    mm.sort()

    bb = max(mm[-2], 1900)

    i = 0
    while i < len(ids):
        cur_sh = ids[i][0]
        cur_id = ids[i][1]
        cnt = 1
        while i + cnt < len(ids) and ids[i + cnt][0] == cur_sh:
            cnt += 1
        if cnt >= bb:
            i += cnt
            continue
        j = i + 1
        while j < len(ids) and ids[j][0] == cur_sh:
            ids2.append((cur_id, ids[j][1]))            
            j += 1
        i += 1

#    print('\n'.join(list(map(str, ids2[:5]))))
    ids2.sort()
#    print(len(ids2))
    i = 0
    while i < len(ids2):
        pos = i + 1
        while pos < len(ids2) and ids2[pos] == ids2[i]:
            pos += 1        
        (u1, u2, cnt) = (ids2[i][0], ids2[i][1], pos - i)
        if cnt > 17:
            print "%s %s %f" % (u1, u2, cnt / (cnt + 2 * (20 - cnt) + 0.0) )    
        i = pos


if __name__ == '__main__':
    main()
