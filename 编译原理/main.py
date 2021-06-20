from Compiler.Tokenizer import Tokenizer
from Compiler import Parser
import argparse


def read_file(file):
    global text
    with open(file, 'r', encoding='utf-8') as f:
        text.append(f.read())


def write_token(file):
    global token
    with open(file[:-3] + '.t', 'w', encoding='utf-8') as f:
        for i in token:
            f.write("<{},{},{},{}> ".format(i[0], i[1], i[2], i[3]))
            if i[0] == ';':
                f.write('\n')


def match(parse: Parser.Parser):
    try:
        tokenizer.match()
        parse.match()
    except SyntaxError:
        pass


if __name__ == '__main__':

    text, token = [], []
    tokenizer = Tokenizer()
    tokenizer.txt = text
    tokenizer.token = token

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version', version='鸿蒙编译器    v1.0.2', help='show the version')
    parser.add_argument('files', nargs='+', type=str, help='files that need be compiled')
    parser.add_argument('-p', '--path', required=True, dest='path', type=str, help='预测分析表或者SLR分析表')
    parser.add_argument('-t', '--tokenizer', dest='token_switch', action='store_true', help='write token to file')
    parser.add_argument('-l', '--LL', dest='grammer_switch', action='store_true',
                        help="the parser's switch is LL(1) or SLR,default=SLR")
    args = parser.parse_args()
    args_write_tokenizer = args.token_switch
    args_grammer_type = args.grammer_switch

    if args_grammer_type:
        parse = Parser.ParserLL(args.path)
    else:
        parse = Parser.ParserSLR(args.path)

    parse.token = token

    for path in args.files:
        read_file(path)
        match(parse)
        if args_write_tokenizer:
            write_token(path)
