from sly import Lexer, Parser
from pathlib import Path


class CalcLexer(Lexer):
    tokens = {BEGIN, END, NAME, STRING, DIGIT, GROUPS_IND, STUDENT_IND, AGE_IND, GROUP_IND, SURNAME_IND, DISCIPLINE_IND}

    # Tokens
    BEGIN = r'\('
    END = r'\)'
    ignore = r' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'\#.*'
    NAME = r'(?!groups|students|age|group|surname|discipline)[^ \t\#();\'\@\^]+'
    DIGIT = r'[0-9]+'
    GROUPS_IND = r'groups'
    STUDENT_IND = r'students'
    AGE_IND = r'age'
    GROUP_IND = r'group'
    SURNAME_IND = r'surname'
    DISCIPLINE_IND = r'discipline'


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    @_("BEGIN GROUPS_IND name names END")
    def groups(self, p):
        return [p.name] + p.names

    @_("BEGIN age group surname END")
    def student(self, p):
        return

    @_("BEGIN AGE_IND name END")
    def age(self, p):
        return [p.name]

    @_("BEGIN SURNAME_IND name END")
    def surname(self, p):
        return [p.name]

    @_("BEGIN GROUP_IND name END")
    def group(self, p):
        return [p.name]




    @_("BEGIN DISCIPLINE_IND name END")
    def discipline(self, p):
        return [p.name]

    @_('name names')
    def names(self, p):
        return [p.name] + p.names

    @_('empty')
    def names(self, p):
        return []

    @_('NAME')
    def name(self, p):
        return p[0]

    @_('')
    def empty(self, p):
        pass


a = "test.conf"
text = Path(a).read_text(encoding='utf-8', errors=None)
lexer = CalcLexer()
parser = CalcParser()

data = lexer.tokenize(text)

parsed = parser.parse(data)

for tok in parsed:
    print(tok)
