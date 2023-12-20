class SyntacticalAnalyzer:
    def __init__(self, lexeme_table, identifiersTable):
        self.identifiersTable = identifiersTable
        self.lex_get = self.lexeme_generator(lexeme_table)
        self.id_stack = []
        self.current_lex = next(self.lex_get)
        self.relation_operations = {"!=", "==", "<", "<=", ">", ">="}
        self.term_operations = {"+", "-", "||"}
        self.factor_operations = {"*", "/", "&&"}
        self.keywords = {"or": 1, "and": 2, "~": 3, ":=": 4, "if": 5,
                         "then": 6, "else": 7, "for": 8, "to": 9, "step": 10, "while": 11, "readln": 12, "writeln": 13,
                         "true": 14, "false": 15, "begin": 16, "end": 17, "next": 18, "dim": 19}

    def equal_token_value(self, word):
        try:
            if self.current_lex.token_value != word:
                self.throw_error()
            self.current_lex = next(self.lex_get)
        except StopIteration:
            pass

    def equal_token_name(self, word):
        if self.current_lex.token_name != word:
            self.throw_error()
        self.current_lex = next(self.lex_get)

    def throw_error(self):
        raise Exception(
            f"\nError in lexeme: '{self.current_lex.token_value}'")

    def lexeme_generator(self, lexeme_table):
        for token in lexeme_table:
            yield token

    def PROGRAMM(self):
        self.equal_token_value("{")  # Проверяем открывающую фигурную скобку
        self.DESCRIPTION()
        self.OPERATOR()
        while self.current_lex.token_value != '}':
            self.current_lex = next(self.lex_get)
            self.OPERATOR()
        if self.current_lex.token_value != "}":
            self.throw_error()

    def DESCRIPTION(self):
        self.equal_token_value("dim")
        self.IDENTIFIER(from_description=True)
        while self.current_lex.token_value == ",":
            self.current_lex = next(self.lex_get)
            self.IDENTIFIER(from_description=True)
        self.TYPE(from_description=True)




    def IDENTIFIER(self, from_description=False):
        if from_description:
            if self.current_lex.token_name != "IDENT":
                 self.throw_error()
            self.id_stack.append(self.current_lex.token_value)

            self.current_lex = next(self.lex_get)
        else:
            self.equal_token_name("IDENT")

    def TYPE(self, from_description=False):
        if from_description:
            if self.current_lex.token_name != "TYPE":
                self.throw_error()
            for item in self.id_stack:
                if item not in self.keywords:
                    self.identifiersTable.put(item, True, self.current_lex.token_value)
            self.id_stack = []
            self.current_lex = next(self.lex_get)
        else:
            self.equal_token_name("TYPE")

    def OPERATOR(self):
        if self.current_lex.token_value == 'if':
            self.CONDITIONAL_OPERATOR()
        elif self.current_lex.token_value == 'for':
            self.FIXED_CYCLE_OPERATOR()
        elif self.current_lex.token_value == 'while':
            self.CONDITIONAL_CYCLE_OPERATOR()
        elif self.current_lex.token_value == 'readln':
            self.INPUT_OPERATOR()
        elif self.current_lex.token_value == 'writeln':
            self.OUTPUT_OPERATOR()
        elif self.current_lex.token_name == 'IDENT':
            self.ASSIGNMENT_OPERATOR()
        elif self.current_lex.token_value == 'begin':
            self.COMPOSITE_OPERATOR()
        else:
            self.throw_error()


    def COMPOSITE_OPERATOR(self):
        self.expect_token_value("begin")
        self.operator()

        while self.current_lex.token_value == ";":
            self.current_lex = next(self.lex_get)
            self.operator()

        self.expect_token_value("end")

    def CONDITIONAL_OPERATOR(self):
        self.equal_token_value("if")
        self.equal_token_value("(")
        self.EXPRESSION()
        self.equal_token_value(")")
        self.OPERATOR()

        if self.current_lex.token_value == "else":
            self.current_lex = next(self.lex_get)
            self.OPERATOR()


    def FIXED_CYCLE_OPERATOR(self):
        self.equal_token_value("for")
        self.ASSIGNMENT_OPERATOR()
        self.equal_token_value("to")
        self.EXPRESSION()

        if self.current_lex.token_value == "step":
            self.current_lex = next(self.lex_get)
            self.EXPRESSION()

        self.OPERATOR()
        self.equal_token_value("next")

    def CONDITIONAL_CYCLE_OPERATOR(self):
        self.equal_token_value("while")
        self.equal_token_value("(")
        self.EXPRESSION()
        self.equal_token_value(")")
        self.OPERATOR()

    def INPUT_OPERATOR(self):
        self.equal_token_value("readln")
        self.IDENTIFIER()
        while self.current_lex.token_value == ",":
            self.current_lex = next(self.lex_get)
            self.IDENTIFIER()

    def OUTPUT_OPERATOR(self):
        self.equal_token_value("writeln")
        self.EXPRESSION()
        while self.current_lex.token_value == ",":
            self.current_lex = next(self.lex_get)
            self.EXPRESSION()

    def ASSIGNMENT_OPERATOR(self):
        if self.current_lex.token_value == '}':
            return

        self.IDENTIFIER()
        self.equal_token_value(":=")
        self.EXPRESSION()

    def EXPRESSION(self):
        self.OPERAND()
        while self.current_lex.token_value in self.relation_operations:
            self.current_lex = next(self.lex_get)
            self.OPERAND()

    def OPERAND(self):
        self.TERM()
        while self.current_lex.token_value in self.term_operations:
            self.current_lex = next(self.lex_get)
            self.TERM()

    def TERM(self):
        self.FACTOR()
        while self.current_lex.token_value in self.factor_operations:
            self.current_lex = next(self.lex_get)
            self.FACTOR()

    def FACTOR(self):
        if self.current_lex.token_name in {"IDENT", "NUM", "NUM2", "NUM8", "NUM10", "NUM16", "REAL"}:
            self.current_lex = next(self.lex_get)
        elif self.current_lex.token_value in {"true", "false"}:
            self.current_lex = next(self.lex_get)
        elif self.current_lex.token_value == "!":
            self.equal_token_value("!")
            self.FACTOR()
        elif self.current_lex.token_value == "(":
            self.equal_token_value("(")
            self.EXPRESSION()
            self.equal_token_value(")")
        else:
            self.throw_error()