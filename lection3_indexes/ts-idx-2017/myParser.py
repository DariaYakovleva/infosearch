import re
import struct
import simple9

tokens = []
curT = 0    

def getArr(dict2, word):
    dictf = open('dict', 'rb')
    st, ll = dict2[word]
    dictf.seek(st)
    lst = []
    for i in range(ll):
        x = struct.unpack('L', dictf.read(struct.calcsize('L')))[0]
        lst.append(x)
    dictf.close()
    return simple9.simple9_decode_lst(lst)


def tokenize(expr):
    expr = re.sub('\s+', '', expr)
    tokens = []
    cur = ''
    for x in expr:
        if x not in '!&|()':
            cur += x
        else:
            if len(cur) > 0:
                tokens.append(cur)
                cur = ''
            tokens.append(x)
    if len(cur) > 0:
        tokens.append(cur)
    return tokens


class WordExpr:
    value = None
    def __init__(self, value=None):
        self.value = value
    def toStr(self):
         return unicode(self.value)
    def eval(self, myDict, cnt_url):
        return getArr(myDict, self.value)
    def getUrls(self, myDict, cnt_url):
        return self.eval(myDict, cnt_url)
    def getTree(self):
        global tokens, curT
        curT += 1
        return WordExpr(tokens[curT - 1])
        
class NOTExpr:
    TOKEN = '!'
    value = None
    def __init__(self, value=None):
        self.value = value
    def toStr(self):
        return self.TOKEN + '(' + unicode(self.value.toStr()) + ')'
    def eval(self, myDict, cnt_url):
        arr1 = self.value.eval(myDict, cnt_url)
        res = []
        prev = -1
        for x in arr1:
            for y in range(prev + 1, x):
                res.append(y)
            prev = x
        for y in range(prev + 1, cnt_url):
            res.append(y)
        return res
    def getUrls(self, myDict, cnt_url):
        return self.eval(myDict, cnt_url)
    def getTree(self):
        global tokens, curT
        if curT < len(tokens) and tokens[curT] == self.TOKEN:
            curT += 1
            return NOTExpr(ORExpr().getTree())
        if curT < len(tokens) and tokens[curT] == '(':
            curT += 1
            tmp = ORExpr().getTree()
            curT += 1
            return tmp
        return WordExpr().getTree()
        
        
class ANDExpr:
    TOKEN = '&'
    value = []
    def __init__(self, value=[]):
        self.value = value
    def toStr(self):
        return '(' + self.TOKEN.join([x.toStr() for x in self.value]) + ')'
    
    def getUrls(self, myDict, cnt_url):
        result = []
        words = [x.getUrls(myDict, cnt_url) for x in self.value]
        n = len(words)
        pointer = [0] * n    
        for url1 in words[0]:
            cnt = 1
            for i in range(1, n):
                curDict = words[i]
                while pointer[i] < len(curDict) and curDict[pointer[i]] < url1:
                    pointer[i] += 1
                if pointer[i] == len(curDict):
                    break
                if curDict[pointer[i]] == url1:
                    cnt += 1
            if cnt == n:
                result.append(url1)
        return result

    def eval(self, myDict, cnt_url):
        arr1 = self.value[0].eval(myDict, cnt_url)
        arr2 = self.value[1].eval(myDict, cnt_url)
        res = []
        j = 0
        for x in arr1:
            while j < len(arr2) and arr2[j] < x:
                j += 1
            if j < len(arr2) and arr2[j] == x:
                res.append(x)
                j += 1
        return res            

    def getTree(self):
        global tokens, curT
        res = NOTExpr().getTree()
        if not (curT < len(tokens) and tokens[curT] == self.TOKEN):
            return res
        res = ANDExpr([res])
        while curT < len(tokens) and tokens[curT] == self.TOKEN:
            curT += 1
            res.value.append(NOTExpr().getTree())
        return res

class ORExpr:
    TOKEN = '|'
    value = []
    def __init__(self, value=[]):
        self.value = value
    def toStr(self):
        return '(' + self.TOKEN.join([x.toStr() for x in self.value]) + ')'
    def eval(self, myDict, cnt_url):
        arr1 = self.value[0].eval(myDict, cnt_url)
        arr2 = self.value[1].eval(myDict, cnt_url)
        res = []
        j = 0
        for x in arr1:
            while j < len(arr2) and arr2[j] < x:
                res.append(arr2[j])
                j += 1
            while j < len(arr2) and arr2[j] == x:
                j += 1
            res.append(x)
        for x in arr2[j:]:
            res.append(x)
        return res 
           
    def getUrls(self, myDict, cnt_url):
        res = []
        words = [x.getUrls(myDict, cnt_url) for x in self.value]
        for w in words:
            res += w
        res.sort()
        result = []
        if len(res) == 0:
            return result
        result.append(res[0])
        for i in range(1, len(res)):
            if res[i] != res[i - 1]:
                result.append(res[i])         
        return result

    def getTree(self):
        global tokens, curT
        res = ANDExpr().getTree()
        if not (curT < len(tokens) and tokens[curT] == self.TOKEN):
            return res
        res = ORExpr([res])
        while curT < len(tokens) and tokens[curT] == self.TOKEN:
            curT += 1
            res.value.append(ANDExpr().getTree())
        return res
    
   
def parse(expr):
    global tokens, curT
    curT = 0   
    tokens = tokenize(expr)
#    print tokens
    cur = ORExpr().getTree()
    return cur



#print parse('a|b').toStr()
#print parse('a&b').toStr()
#print parse('( a & b)').toStr()
#print parse('!(a & b )').toStr()
#print parse(' a ').toStr()
#print parse('!(a & b ) | c | !s').toStr()
