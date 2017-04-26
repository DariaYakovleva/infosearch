#!/usr/bin/env python

"""
This just a draft for homework 'near-duplicates'
Use MinshinglesCounter to make result closer to checker
"""

import sys
import re
import mmh3
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
            h = mmh3.hash(' '.join(words[i:i+self.window]).encode('utf-8'))
#            h = hash(' '.join(words[i:i+self.window]).encode('utf-8'))
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
            lst = mhc.count(doc.text)
            if lst != None:
                ids.append((doc.url, lst))
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                sh1 = ids[i][1]
                sh2 = ids[j][1]
                u1 = ids[i][0]
                u2 = ids[j][0]
                if u1 == u2:
                    continue
                cnt = 0
                for x in sh1:
                    if x in sh2:
                        cnt += 1                                              
                if cnt > 17:
                    print "%s %s %f" % (u1, u2, cnt / (cnt + 2 * (20 - cnt) + 0.0) )    

if __name__ == '__main__':
    main()
