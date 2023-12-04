# Списки ключевых слов, операторов и операции присваивания
KEYWORDS = ["for", "do"]
OPERATORS = ["(", ")", ";", "<", ">", "="]
ASSIGNMENT = [":="]

# Класс для представления токена
class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value

# Класс для представления таблицы лексем
class LexemeTable:
    def __init__(self):
        self.tok = None
        self.next = None

# Инициализация переменных
lt = None  # Текущая таблица лексем
lt_head = None  # Голова таблицы лексем

# Функция для проверки, является ли идентификатор ключевым словом
def is_kword(id):
    return id in KEYWORDS

# Функция для добавления токена в таблицу лексем
def add_token(tok):
    global lt, lt_head
    if not lt:
        lt = LexemeTable()
        lt.tok = tok
        lt_head = lt
    else:
        lt.next = LexemeTable()
        lt = lt.next
        lt.tok = tok


# Функция для лексического анализа файла
def lexer(filename):
    try:
        with open(filename, 'r') as fd:
            CS = 'H'  # Начальное состояние конечного автомата
            c = fd.read(1)  # Чтение символа из файла
            while c:
                if CS == 'H':
                    while c.isspace():
                        c = fd.read(1)
                    if (c.isalpha() or c == '_'):
                        CS = 'ID'  # Идентификатор
                    elif (c.isdigit() or (c in "+-")):
                        CS = 'NM'  # Число
                    elif c == ':':
                        CS = 'ASGN'  # Знак присваивания
                    else:
                        CS = 'DLM'  # Разделитель или оператор

                if CS == 'ASGN':
                    colon = c
                    c = fd.read(1)
                    if c == '=':
                        tok = Token("OPER", ":=")
                        add_token(tok)
                        print(f"Token Name: {tok.token_name}, Token Value: {tok.token_value}")
                        c = fd.read(1)
                        CS = 'H'
                    else:
                        err_symbol = colon
                        CS = 'ERR'

                if CS == 'DLM':
                    if c in "();":
                        tok = Token("DELIM", c)
                        add_token(tok)
                        print(f"Token Name: {tok.token_name}, Token Value: {tok.token_value}")
                        c = fd.read(1)
                        CS = 'H'
                    elif c in "<>=":
                        tok = Token("OPER", c)
                        add_token(tok)
                        print(f"Token Name: {tok.token_name}, Token Value: {tok.token_value}")
                        c = fd.read(1)
                        CS = 'H'
                    else:
                        err_symbol = c
                        c = fd.read(1)
                        CS = 'ERR'

                if CS == 'ERR':
                    print("Unknown character:", err_symbol)
                    CS = 'H'

                if CS == 'ID':
                    buf = c
                    c = fd.read(1)
                    while c.isalnum() or c == '_':
                        buf += c
                        c = fd.read(1)
                    if is_kword(buf):
                        tok = Token("KWORD", buf)
                    else:
                        tok = Token("IDENT", buf)
                    add_token(tok)
                    print(f"Token Name: {tok.token_name}, Token Value: {tok.token_value}")
                    CS = 'H'

                if CS == 'NM':
                    buf = c
                    c = fd.read(1)
                    while c.isdigit() or c in ".eE+-":
                        buf += c
                        c = fd.read(1)
                    tok = Token("NUM", buf)
                    add_token(tok)
                    print(f"Token Name: {tok.token_name}, Token Value: {tok.token_value}")
                    CS = 'H'

    except FileNotFoundError:
        print("Cannot open file", filename)

# Пример использования функции lexer
lexer("input.txt")


