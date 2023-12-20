import re
from Utils import *

class LexicalAnalyzer:
    def __init__(self, filename: str, identifiersTable):
        self.identifiersTable = identifiersTable
        self.states = States("H", "COMM", "ID", "ERR", "NM", "DLM")
        self.token_names = Tokens("KWORD", "IDENT", "NUM", "OPER", "DELIM", "NUM2", "NUM8", "NUM10", "NUM16", "REAL",
                                  "TYPE", "ARITH")
        self.keywords = {"or": 1, "and": 2, "!": 3, ":=": 4, "if": 5,
                         "then": 6, "else": 7, "for": 8, "to": 9, "step": 10, "while": 11, "readln": 12, "writeln": 13,
                         "true": 14, "false": 15, "begin": 16, "end": 17, "next": 18, "dim": 19}
        self.types = {"%", "!", "$"}
        self.arith = {"+", '-', '*', '/'}
        self.operators = {"!=", "==", "<", "<=", ">", ">="}
        self.delimiters = {";", ",", ":", "[", "]", "(", ")", "{", "}"}
        self.fgetc = fgetc_generator(filename)
        self.current = Current(state=self.states.H)
        self.error = Error(filename)
        self.lexeme_table = []

    def analysis(self):
        self.current.state = self.states.H
        self.current.re_assign(*next(self.fgetc))
        while not self.current.eof_state:
            if self.current.state == self.states.H:
                self.h_state_processing()
            elif self.current.state == self.states.COMM:
                self.comm_state_processing()
            elif self.current.state == self.states.ID:
                self.id_state_processing()
            elif self.current.state == self.states.ERR:
                self.err_state_processing()
            elif self.current.state == self.states.NM:
                self.nm_state_processing()
            elif self.current.state == self.states.DLM:
                self.dlm_state_processing()

    def h_state_processing(self):
        while not self.current.eof_state and self.current.symbol in {" ", "\n", "\t"}:
            self.current.re_assign(*next(self.fgetc))

        if self.current.eof_state:
            return

        if self.current.symbol.isalpha():
            self.current.state = self.states.ID
        elif self.current.symbol == '!':
            temp_symbol = self.current.symbol
            self.current.re_assign(*next(self.fgetc))
            if temp_symbol + self.current.symbol in self.operators:
                self.add_token(self.token_names.OPER, temp_symbol + self.current.symbol)
                self.current.re_assign(*next(self.fgetc))
            else:
                if self.current.symbol != "\n":
                    self.add_token(self.token_names.KWORD, temp_symbol)
                else:
                    self.add_token(self.token_names.TYPE, temp_symbol)



        elif self.current.symbol.isdigit() or self.current.symbol == '.':
            self.current.state = self.states.NM
        elif self.current.symbol in (self.delimiters | self.operators | self.types | self.arith):
            self.current.state = self.states.DLM
        elif self.current.symbol == "/":
            self.current.re_assign(*next(self.fgetc))
            if self.current.symbol == "/":
                self.current.state = self.states.COMM
            else:
                self.current.state = self.states.ERR
        elif self.current.symbol == "=":
            temp_symbol = self.current.symbol
            self.current.re_assign(*next(self.fgetc))
            if self.current.symbol == '=':
                self.add_token(self.token_names.OPER, temp_symbol + self.current.symbol)
        elif self.current.symbol == "|":
            temp_symbol = self.current.symbol
            self.current.re_assign(*next(self.fgetc))
            if temp_symbol + self.current.symbol == "||":
                self.add_token(self.token_names.ARITH, temp_symbol + self.current.symbol)
                self.current.re_assign(*next(self.fgetc))
            else:
                self.current.state = self.states.ERR
        elif self.current.symbol == "&":
            temp_symbol = self.current.symbol
            self.current.re_assign(*next(self.fgetc))
            if temp_symbol + self.current.symbol == "&&":
                self.add_token(self.token_names.ARITH, temp_symbol + self.current.symbol)
                self.current.re_assign(*next(self.fgetc))
            else:
                self.current.state = self.states.ERR
        else:
            self.current.state = self.states.ERR
            self.error.symbol = self.current.symbol




    def comm_state_processing(self):
        while not self.current.eof_state and self.current.symbol != "//":
            self.current.re_assign(*next(self.fgetc))
        if self.current.symbol == "//":
            self.current.state = self.states.H
            if not self.current.eof_state:
                self.current.re_assign(*next(self.fgetc))
        else:
            self.error.symbol = self.current.symbol
            self.current.state = self.states.ERR

    def dlm_state_processing(self):
        if self.current.symbol == ':':
            temp_symbol = self.current.symbol
            self.current.re_assign(*next(self.fgetc))
            if self.current.symbol == '=':
                self.add_token(self.token_names.KWORD, temp_symbol + self.current.symbol)
                self.current.re_assign(*next(self.fgetc))
            elif self.current.symbol == ' ':
                self.add_token(self.token_names.DELIM, temp_symbol)
            else:
                self.error.symbol = temp_symbol
                self.current.state = self.states.ERR
        elif self.current.symbol in self.delimiters | self.arith | self.types:
            if self.current.symbol in self.delimiters:
                self.add_token(self.token_names.DELIM, self.current.symbol)
            elif self.current.symbol in self.types:
                self.add_token(self.token_names.TYPE, self.current.symbol)
            else:
                self.add_token(self.token_names.ARITH, self.current.symbol)
            if not self.current.eof_state:
                self.current.re_assign(*next(self.fgetc))
        elif self.current.symbol == '}':
            self.add_token(self.token_names.DELIM, self.current.symbol)
            self.current.re_assign(*next(self.fgetc))

        else:
            temp_symbol = self.current.symbol
            self.current.re_assign(*next(self.fgetc))
            if temp_symbol + self.current.symbol in self.operators:
                self.add_token(self.token_names.OPER, temp_symbol + self.current.symbol)
                self.current.re_assign(*next(self.fgetc))
            else:
                self.add_token(self.token_names.OPER, temp_symbol)

        self.current.state = self.states.H

    def err_state_processing(self):
        raise Exception(
            f"\nUnknown: '{self.error.symbol}' in file {self.error.filename} \nline: {self.current.line_number} and pos: {self.current.pos_number}")

    def id_state_processing(self):
        buf = [self.current.symbol]
        if not self.current.eof_state:
            self.current.re_assign(*next(self.fgetc))
        while not self.current.eof_state and (self.current.symbol.isalpha() or self.current.symbol.isdigit()):
            buf.append(self.current.symbol)
            self.current.re_assign(*next(self.fgetc))
        buf = ''.join(buf)

        if buf in self.arith:
            self.add_token(self.token_names.ARITH, buf)
        elif buf in self.operators:
            self.add_token(self.token_names.OPER, buf)
        elif buf in self.keywords:
            self.add_token(self.token_names.KWORD, buf)
        else:
            self.add_token(self.token_names.IDENT, buf)
            if buf not in self.keywords:
                self.identifiersTable.put(buf)

        self.current.state = self.states.H
    def nm_state_processing(self):
        buf = []
        buf.append(self.current.symbol)
        if not self.current.eof_state:
            self.current.re_assign(*next(self.fgetc))
        while not self.current.eof_state and (self.current.symbol in set(list("ABCDEFabcdefoOdDhH0123456789.eE+-"))):
            buf.append(self.current.symbol)
            self.current.re_assign(*next(self.fgetc))

        buf = ''.join(buf)
        is_n, token_num = self.is_num(buf)
        # Проверяем, является ли строка числом, и определяем тип токена
        if is_n:
            self.add_token(token_num, buf)
            self.current.state = self.states.H
        else:
            self.error.symbol = buf

            self.current.state = self.states.ERR

    def is_num(self, digit):
        if re.match(r"(^\d+[Ee][+-]?\d+$|^\d*\.\d+([Ee][+-]?\d+)?$)", digit):
            return True, self.token_names.REAL
        elif re.match(r"^[01]+[Bb]$", digit):
            return True, self.token_names.NUM2
        elif re.match(r"^[01234567]+[Oo]$", digit):
            return True, self.token_names.NUM8
        elif re.match(r"^\d+[dD]?$", digit):
            return True, self.token_names.NUM10
        elif re.match(r"^\d[0-9ABCDEFabcdef]*[Hh]$", digit):
            return True, self.token_names.NUM16

        return False, False

    def is_keyword(self, word):
        if word in self.keywords:
            return True
        return False

    def add_token(self, token_name, token_value):
        self.lexeme_table.append(Token(token_name, token_value))