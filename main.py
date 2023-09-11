def infix_to_postfix(expression):
    priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # Приоритеты команд

    def is_operator(token):  # Проверка является ли оператором
        return token in '+-*/^'

    def higher_precedence(op1, op2):  # Сравнение приоритетов двух операторов
        return priority[op1] > priority[op2]

    postfix = []
    stack = []

    for token in expression.split():
        if token.isalnum():
            postfix.append(token)  # Если токен - операнд, добавляем его в выходную строку
        elif is_operator(token):
            while (stack and is_operator(stack[-1]) and
                   higher_precedence(stack[-1], token)):
                postfix.append(stack.pop())  # Переносим операторы с более высоким приоритетом из стека
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())  # Выносим операторы из стека до открывающей скобки
            stack.pop()  # Удаляем открывающую скобку

    while stack:
        postfix.append(stack.pop())  # Выносим оставшиеся операторы из стека

    return ' '.join(postfix)


if __name__ == '__main__':
    expression = input()
    postfix_result = infix_to_postfix(expression)
    print(postfix_result)
