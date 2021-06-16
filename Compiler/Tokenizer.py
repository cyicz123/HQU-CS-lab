import re


class Tokenizer:
    def __init__(self):
        self.txt, self.token = [], []
        self.error = False
        self.key = ['PI', 'E', 'sin', 'cos', 'tg', 'ctg', 'log', 'lg', 'ln']
        ###########################################
        #   匹配注释
        ###########################################
        self.annotation = re.compile(r"'''[\s\S]*?'''|#.*\n|#.*$")

        ###########################################
        #   id为变量，最多32位由_字母和数字组成
        ###########################################
        self.id = re.compile(r'[_a-zA-Z]{1}[_a-zA-Z0-9]{0,31}')

        ###########################################
        #   num为常量，非负实数或者PI和E
        ###########################################
        self.num = re.compile(r'([1-9]\d*\.\d*[1-9]|[1-9]+\d*|0\.\d*[1-9]|PI|E)\b')

        ###########################################
        #   K为关键字
        ###########################################
        self.K = re.compile(r'(sin|cos|tan|tg|ctg|lg|ln)\b')

        ###########################################
        #   单独识别log,因为log需要做终结符
        ###########################################
        self.log = re.compile(r'log\b')

        ###########################################
        #   O为运算符或;
        ###########################################
        self.O = re.compile(r'[+\-*/=^();?,]')

        ###########################################
        #   S为空格、回车或换行
        ###########################################
        self.S = re.compile(r'[\t\n ]+')

    def match(self):
        for text in self.txt:
            ###########################################
            #   匹配注释，变为空格
            ###########################################
            text = self.annotation.sub(' ', text)
            for row, s in enumerate(text.split('\n')):
                i = 0
                while i < len(s):
                    m = self.num.match(s, i)
                    if m is not None:
                        i = m.end()
                        self.token.append(('num', m.group(), row, i))
                        continue

                    m = self.K.match(s, i)
                    if m is not None:
                        i = m.end()
                        self.token.append(('k', m.group(), row, i))
                        continue

                    m = self.log.match(s, i)
                    if m is not None:
                        i = m.end()
                        self.token.append((m.group(), m.group(), row, i))
                        continue

                    m = self.id.match(s, i)
                    if m is not None:
                        i = m.end()
                        self.token.append(('id', m.group(), row, i))
                        continue

                    m = self.O.match(s, i)
                    if m is not None:
                        i = m.end()
                        self.token.append((m.group(), m.group(), row, i))
                        continue

                    m = self.S.match(s, i)
                    if m is not None:
                        i = m.end()
                        continue
                    i += 1
                    print('LexerError: index:{} {}<-'.format((row, i), s[:i]))
                    self.error = True
        if self.error:
            raise SyntaxError
