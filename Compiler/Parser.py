import pandas as pd
import re
from queue import LifoQueue as stack
from queue import Queue as queue


class Parser:
    def __init__(self, csv_path):
        try:
            self.db = pd.read_csv(csv_path, header=0, index_col=0)
        except:
            raise IOError
        ###########################################
        #   获取token
        ###########################################
        self.token = []
        self.q = queue()
        self.s = stack()

        self.error = False


class ParserLL(Parser):
    def __init__(self, csv_path='Data/预测分析表.CSV'):
        super(ParserLL, self).__init__(csv_path)
        self.db = self.db.fillna(value=' ')
        ###########################################
        #   获取终结符和非终结符集合
        ###########################################
        self.db_col_name = self.db.columns.values.tolist()
        self.db_row_name = self.db._stat_axis.values.tolist()

        self.id = re.compile(r"(L|E'|E|T'|T|F'|F|G|R|\(|\)|\+|-|\*|/|\^|;|\?|=|id|num|k|\$|,|log)")

    ###########################################
    #   将每句以分号结尾的token加入栈和队列
    ###########################################
    def _match_init_(self, i):
        self.s.queue.clear()
        self.q.queue.clear()
        self.s.put('#')
        self.s.put('L')
        while i < len(self.token):
            self.q.put(self.token[i])
            i += 1
            if self.q.queue[-1][0] == ';':
                self.q.put(('#', '', self.token[i-1][-2], self.token[i-1][-1]))
                return i
        self.q.put(('#', '', self.token[-1][-2], self.token[-1][-1]))
        return i

    ###########################################
    #   用预测分析表里面的展开式来替换非终结符
    #   a代表终结符，b为非终结符
    ###########################################
    def _expand(self, a, b):
        s = self.id.findall(self.db[a][b])
        self.s.get()
        for i in s[::-1]:
            if i == '$':
                continue
            self.s.put(i)

    ###########################################
    #   语法分析
    ###########################################
    def match(self):
        i = 0
        while i < len(self.token):
            i = self._match_init_(i)
            x = self.s.queue[-1]  # 表示栈顶
            a = self.q.queue[0]  # 表示队列头
            while x != '#':
                if x in self.db_col_name:
                    if x == a[0]:
                        self.s.get()
                        self.q.get()
                    else:
                        print("SyntaxError: index:{} expected token is {} ,but it's {}({})".format(
                            (a[-2], a[-1]), x, a[0], a[1]))
                        self.error = True
                        break
                else:
                    if self.db[a[0]][x] != ' ':
                        self._expand(a[0], x)
                    else:
                        print("SyntaxError: index:{} production mismatch".format((a[-2], a[-1])))
                        self.error = True
                        break
                x = self.s.queue[-1]
                a = self.q.queue[0]
        if self.error:
            raise SyntaxError
        else:
            print('Success')


class ParserSLR(Parser):
    def __init__(self, csv_path='Data/slr.CSV'):
        super(ParserSLR, self).__init__(csv_path)
        self.db = self.db.fillna(value=0)
        self.db = self.db.astype(dtype=int)
        self.grammer = []
        self._read_grammer_('Data/SLRgrammer.txt')

    def _read_grammer_(self, grammer_path: str):
        pattern = re.compile(r"L|E|T|F|G|R|\(|\)|\+|->|-|\*|/|\^|;|\?|=|id|num|k|\$|,|log|\|")
        N = 'L'
        try:
            with open(grammer_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    g = pattern.findall(line)
                    if g[0] != '|':
                        N = g[0]
                        del (g[1])
                        self.grammer.append(g)
                    else:
                        g[0] = N
                        self.grammer.append(g)
        except:
            raise IOError

    def _match_init_(self, i):
        self.s.queue.clear()
        self.q.queue.clear()
        self.s.put('#')
        self.s.put(0)
        while i < len(self.token):
            self.q.put(self.token[i])
            i += 1
            if self.q.queue[-1][0] == ';':
                self.q.put(('#', '', self.token[i-1][-2], self.token[i-1][-1]))
                return i
        self.q.put(('#', '', self.token[-1][-2], self.token[-1][-1]))
        return i

    def match(self):
        i = 0
        while i < len(self.token):
            i = self._match_init_(i)
            x = self.s.queue[-1]  # 表示栈顶
            a = self.q.queue[0]  # 表示队列头
            while not self.q.empty():
                num = self.db[a[0]][x]
                if num >= 100 and num <= 200:
                    num -= 100
                    self.s.put(a[0])
                    self.s.put(num)
                    self.q.get()
                elif num > 200:
                    num -= 200
                    if self.grammer[num-1][-1]!='$':
                        for j in range(2 * len(self.grammer[num-1][1:])):
                            self.s.get()
                    x = self.s.queue[-1]
                    self.s.put(self.grammer[num-1][0])

                    self.s.put(self.db[self.grammer[num-1][0]][x])
                elif num == -1:
                    break
                else:
                    print("SyntaxError: index:{} production mismatch".format((a[-2], a[-1])))
                    self.error = True
                    break
                x = self.s.queue[-1]  # 表示栈顶
                a = self.q.queue[0]  # 表示队列头
        if self.error:
            raise SyntaxError
        else:
            print('Success')
