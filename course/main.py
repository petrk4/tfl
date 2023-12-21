from Lexer import LexicalAnalyzer
from Syntax import SyntacticalAnalyzer
from Semantic import IdentifiersTable

PRINT_INFO = True
PATH_TO_PROGRAM = "input.txt"


def main():

    identifiersTable = IdentifiersTable()
    lexer = LexicalAnalyzer(PATH_TO_PROGRAM, identifiersTable)
    lexer.analysis()
    if lexer.current.state != lexer.states.ERR:
        if PRINT_INFO:
            print("Result of Lexical Analyzer:")
            for i in lexer.lexeme_table:
                print(f"{i.token_name} {i.token_value}")


        syntaxAnalyzer = SyntacticalAnalyzer(lexer.lexeme_table, identifiersTable)
        syntaxAnalyzer.PROGRAMM()
        print("COMPILED")




if __name__ == "__main__":
    main()