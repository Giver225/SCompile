from sly import Lexer, Parser
import sys

"""
<program> ::= <s-exp-list>
<s-exp-list> ::= <s-exp> , <s-exp-list> | <s-exp>
<s-exp> ::= { <s-exp-list> } | <var>
<var> ::= <string> : <info>
<info> :: <string> | <int> | [<s-exp-list>]
"""


class ExpLexer(Lexer):
    tokens = {STRING, DOT2, LSQR, RSQR, INT, COMMA, LFIG, RFIG}

    # igonre = r'#.*'  # igonre comments
    ignore_spaces = r'\ '
    # ignore_newln = r'\n'
    STRING = r'\".*\"'
    DOT2 = r'\:'
    LSQR = r'\['
    RSQR = r'\]'
    LFIG = r'\{'
    RFIG = r'\}'
    INT = r'\d+'
    COMMA = r'\,'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)


def addTabs(n):
    ans = ''
    for i in range(n):
        ans += '\t'
    return ans


class ExpParser(Parser):

    tokens = ExpLexer.tokens


    @_('s_exp_list')
    def program(self, p):
        return str(p.s_exp_list)

    @_('s_exp COMMA s_exp_list')
    def s_exp_list(self, p):
        return str(p.s_exp) + ',\n' + str(p.s_exp_list)

    @_('s_exp')
    def s_exp_list(self, p):
        return str(p.s_exp)

    # @_('')
    # def empty(self,p):
    #     pass

    @_('LFIG s_exp_list RFIG')
    def s_exp(self, p):

        ans = '{\n' + str(p.s_exp_list) + '\n}'

        return ans

    @_('var')
    def s_exp(self, p):
        return str(p.var)

    @_('STRING')
    def s_exp(self, p):
        return str(p.STRING)

    @_('INT')
    def s_exp(self, p):
        return str(p.INT)

    @_('STRING DOT2 info')
    def var(self, p):

        return str(p.STRING) + ':' + str(p.info)

    @_('STRING')
    def info(self, p):
        return str(p.STRING)

    @_('INT')
    def info(self, p):
        return str(p.INT)

    @_('LSQR arr_comp_list RSQR')
    def info(self, p):

        ans = '[\n' + str(p.arr_comp_list) + '\n]'

        return ans

    @_('arr_comp COMMA arr_comp_list')
    def arr_comp_list(self, p):

        return str(p.arr_comp) + ',\n' + str(p.arr_comp_list)

    @_('arr_comp')
    def arr_comp_list(self, p):

        return str(p.arr_comp)

    @_('STRING')
    def arr_comp(self, p):
        return str(p.STRING)

    @_('INT')
    def arr_comp(self, p):
        return str(p.INT)

    @_('s_exp')
    def arr_comp(self, p):
        return str(p.s_exp)


text = """
{
  "groups": [
    "????????-1-20",
    "????????-2-20",
    "????????-3-20",
    "????????-4-20",
    "????????-5-20",
    "????????-6-20",
    "????????-7-20",
    "????????-8-20",
    "????????-9-20",
    "????????-10-20",
    "????????-11-20",
    "????????-12-20",
    "????????-13-20",
    "????????-14-20",
    "????????-15-20",
    "????????-16-20",
    "????????-17-20",
    "????????-18-20",
    "????????-19-20",
    "????????-20-20",
    "????????-21-20",
    "????????-22-20",
    "????????-23-20",
    "????????-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "????????-4-20",
      "name": "???????????? ??.??."
    },
    {
      "age": 18,
      "group": "????????-5-20",
      "name": "???????????? ??.??."
    },
    {
      "age": 18,
      "group": "????????-5-20",
      "name": "?????????????? ??.??."
    }
   
  ],
  "subject": "???????????????????????????????? ????????????????????"
} 
"""

if __name__ == '__main__':
    f = open(str(sys.argv[1]), 'r')
    lexer = ExpLexer()
    parser = ExpParser()
    print(parser.parse(lexer.tokenize(f.read())))
