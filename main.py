from Compiler.Tokenizer import Tokenizer
from Compiler.Parser import Parser
import argparse

text, token = [], []
tokenizer = Tokenizer()
tokenizer.txt = text
tokenizer.token = token


def read_file(file):
    global text
    with open(file, 'r', encoding='utf-8') as f:
        text.append(f.read())
        try:
            tokenizer.match()
            parse.match()
        except SyntaxError:
            pass
        if args_write_tokenizer:
            write_token(path)



def write_token(file):
    global token
    with open(file[:-3] + '.t', 'w', encoding='utf-8') as f:
        for i in token:
            f.write("<{},{},{},{}> ".format(i[0], i[1], i[2], i[3]))
            if i[0] == ';':
                f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version', version='鸿蒙编译器    v0.5.0', help='show the version')
    parser.add_argument('files', nargs='+', type=str, help='files that need be compiled')
    parser.add_argument('-p', required=True, dest='path', type=str, help='预测分析表.csv')
    parser.add_argument('-t', '--tokenizer', dest='token_switch', action='store_true', help='write token to file')
    args = parser.parse_args()
    args_write_tokenizer = False
    args_write_tokenizer = args.token_switch

    parse = Parser(args.path)
    parse.token = token

    for path in args.files:
        read_file(path)