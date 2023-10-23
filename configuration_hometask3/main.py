from sly import Lexer, Parser
import json


class Object:
    def __init__(self, data):
        self.data = data
        self.root = None
        self.children = []

    def __str__(self):
        return str(self.data)

    def serialize(self):
        result = []
        for child in self.children:
            result.append(child.serialize())
        result.reverse()

        if len(result) > 0:
            json = dict()
            if len(result) == 1:
                result = result[0]
            else:
                final = []
                main_dict = dict()
                for child in result:
                    if isinstance(child, list):
                        for j in child:
                            final.append(j)
                    elif isinstance(child, dict):
                        for k, v in child.items():
                            main_dict[k] = v
                    else:
                        final.append(child)
                if len(main_dict) > 0:
                    final.append(main_dict)
                result = final
            json[str(self.data)] = result
        else:
            json = self.data
        return json


class ObjectsList:

    def __init__(self):
        self.list = []

    def serialize(self):
        result = []
        for item in self.list:
            result.append(item.serialize())
        if len(result) == 1:
            result = result[0]
        else:
            final = []
            main_dict = dict()
            for item in result:
                if isinstance(item, dict):
                    for k, v in item.items():
                        main_dict[k] = v
                elif isinstance(item, list):
                    for j in item:
                        final.append(j)
                else:
                    final.append(item)
            if len(main_dict) > 0:
                final.append(main_dict)
            result = final
        return result


class CalcLexer(Lexer):
    tokens = {STRING, NUMBER, LPAREN, RPAREN}
    ignore = ' \t'

    STRING = r'("[a-zа-яА-ЯA-Z.0-9_\- \/\*]*"|[а-яА-Я-a-zA-Z_.]+[.а-яА-Я0-9-a-zA-Z_]*)'
    NUMBER = r'\d+'

    LPAREN = r'\('
    RPAREN = r'\)'

    ignore_newline = r'\n+'
    ignore_comments = r'\/\*.*\*\/'
    ignore_come = r','

    def error(self, t):
        print('Line %d: Недопустимый символ: %r' % (self.lineno, t.value[0]))
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', STRING),
    )

    def __init__(self):
        self.root = None
        self.errors = False

    def error(self, token):
        if not self.errors:
            print('Fatal: невозможно прочитать файл')
        self.errors = True

    @_('term')
    def expr(self, p):
        return p[0]

    @_('term expr')
    def expr(self, p):
        obj = ObjectsList()
        if isinstance(p[1], ObjectsList):
            for i in p[1].list:
                obj.list.append(i)
        else:
            obj.list.append(p[1])

        if isinstance(p[0], ObjectsList):
            for i in p[0].list:
                obj.list.append(i)
        else:
            obj.list.append(p[0])
        return obj

    @_('NUMBER')
    def term(self, p):
        obj = Object(int(p.NUMBER))
        return obj

    @_('STRING')
    def term(self, p):
        obj = Object(str(p.STRING).replace('"', ''))
        return obj

    @_('LPAREN expr RPAREN')
    def term(self, p):
        if isinstance(p[1], Object):
            return p[1]
        obj = p[1].list.pop()
        for item in p[1].list:
            obj.children.append(item)
        self.root = obj
        return obj


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    file_name = input('Введите имя файла: ')

    if file_name:
        # Открытие файла
        try:
            with open(file_name, 'r') as file:
                text = file.read()
        except FileNotFoundError:
            print('Файла с таким именем не существует')
        # Парсинг файла
        parser.parse(lexer.tokenize(text))
        if not parser.errors:
            # Создание JSON
            root = parser.root
            serializable = root.serialize()
            print('Вывод в JSON:')
            print(json.dumps(serializable, indent=1, ensure_ascii=False))
        else:
            print('В файле обнаружены синтаксические ошибки')