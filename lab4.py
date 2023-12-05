def get_input(prompt): #ф-ция запрашивает ввод пользователя, выводя сообщение prompt
    return input(prompt) #Возвращает введенные данные

def get_states(): #Запрашивает у польз-теля ввод множ-ва сост-ий НКА, разделенных пробелами
    states = get_input("Enter set of states:\n").split()
    return set(states) #возвращает множество состояний

def get_input_alphabet(): #Запрашивает у пользователя ввод алфавита (множ-во входных символов), разделенных пробелами
    alphabet = get_input("Enter the input alphabet:\n").split()
    return set(alphabet) #Возвращает множество входных символов

#Данная часть кода предназначена для сбора информации о переходах между сост-ми в автомате
def get_transitions(states, alphabet): #Запрашивает у пользователя ввод ф-ции перехода для НКА
    transitions = {} #инициализируем пустой словарь transition, где будем хранить переходы между состояниями
    while True: #запускаем бесконечный цикл; (текущее состояние, входной символ, следующеесостояние) до тех пор, пока пользователь не нажмет Enter(что означает выход из цикла)
        transition = get_input("Enter state-transitions function (current state, input character, next state) orpress Enter to finish:\n")
        if not transition: #Если ввод пустой (пользователь нажал Enter)
            break #выходим из цикла
        parts = transition.split(',') #разбиваем введенную строку на части, используя запятые как разделители
        if len(parts) == 3: #если кол-во частей = 3, извлекаем текущее состояние, входной символ и следующее состояние
            current_state, input_char, next_state = parts
            if current_state in states and input_char in alphabet and next_state in states: #проверяем, что текущее состояние, входной символ и следующее состояние входят в заданные states и alphabet
                if (current_state, input_char) in transitions: #если переход для данной комбинации(текущее состояние, входной символ) уже сущ-ет, то добавляем следующее состояние в множество переходов
                    transitions[(current_state, input_char)].add(next_state)
                else: #иначе, создаем новую запись в словаре переходов
                    transitions[(current_state, input_char)] = {next_state}
            else: #если введенные сост-ия или символ не соответствуют заданным, выводим сообщение об ошибке
                print("Invalid input. Please enter valid transitions.")
        else: #если ввод не соответствует ожидаемому формату, выводим сообщение об ошибке ввода
            print("Invalid input format. Please use the format '(current state, input character, next state)'.")
    return transitions #возвращаем словарь transitions после завершения ввода переходов.

def get_initial_states(states): #запрашиваем у пользователя ввод множ-ва начальных сост-ий иразбиваем введенные знач-ия на отдельные элементы
    initial_states = get_input("Enter a set of initial states:\n").split()
    return set(initial_states) #возвращаем множ-во начальных состояний, полученных из ввода пользователя

def get_final_states(states): #запрашиваем у пользователя ввод множества конечных состояний и разбиваем введенные значения на отдельные элементы.
    final_states = get_input("Enter a set of final states:\n").split()
    return set(final_states) #возвращаем множ-во конечных состояний, полученных из ввода пользователя

def epsilon_closure(states, transitions, state): # Функция epsilon_closure вычисляет эпсилон-замыкание для данного состояния в НКА
    closure = set() #создаем пустое множество для хранения эпсилон-замыкания
    stack = list(state) #инициализируем стек начальным состоянием
    while stack: # Запускаем цикл, к-рый будет выполняться, пока стек не пуст 4
        current_states = stack.pop() #извлекаем состояние из стека.
        closure.update(current_states) #добавляем извлеченное состояние в эпсилон-замыкание
        for current_state in current_states: # Перебираем каждое текущее состояние из извлеченного множества
            if (current_state, '') in transitions: # Проверяем, есть ли переход по эпсилону из текущего состояния
                for next_state in transitions[(current_state, '')]:
                    if next_state not in closure:
                        stack.append({next_state}) #если следующее сост-ие не находится в замыкании, добавляем его в стек
    return closure # Возвращаем эпсилон-замыкание.

def move(states, transitions, state, symbol): # Функция move вычисляет множество состояний, в которые можно перейти из данного состояния по заданному символу.
    next_states = set() # Создаем пустое множество для хранения следующих состояний.
    for s in state: # Перебираем каждое состояние из переданного множества state.
        if (s, symbol) in transitions: # Проверяем, есть ли переход по заданному символу из текущего состояния.
            next_states.update(transitions[(s, symbol)]) #добавляем следующие сост-ия в множ-во next_states
    return next_states # Возвращаем множество следующих состояний.

def nfa_to_dfa(states, alphabet, transitions, initial_states, final_states): # Функция nfa_to_dfa выполняет конвертацию НКА в ДКА.
    dfa_states = set() # Создаем пустое множество для хранения состояний ДКА.
    dfa_transitions = {} # Создаем пустой словарь для хранения переходов ДКА.
    dfa_initial_states = set() # Создаем пустое множество для хранения начальных состояний ДКА
    dfa_final_states = set() # Создаем пустое множество для хранения конечных состояний ДКА
    initial_closure = epsilon_closure(states, transitions, initial_states) # Вычисляем эпсилон-замыкание для начальных состояний.
    unprocessed_states = [initial_closure] # Создаем список необработанных состояний, инициализируем начальным замыканием.
    processed_states = set() # Создаем множество уже обработанных состояний.
    while unprocessed_states: # Запускаем цикл, который будет выполняться, пока есть необработанные состояния.
        current_states = unprocessed_states.pop() # Извлекаем текущее состояние из списка необработанных.
        current_state = ''.join(sorted(current_states)) #формируем строку из сост-ий ДКА и сортируем ее dfa_states.add(current_state) #Добавляем текущее состояние в множество состояний ДКА
        if initial_closure == current_states:
            dfa_initial_states.add(current_state) # Если текущее состояние соответствует начальному замыканию, добавляем его в начальные состояния ДКА
        if current_states.intersection(final_states):
            dfa_final_states.add(current_state) # Если текущее состояние содержит конечные состояния НКА, добавляем его в конечные состояния ДКА.
        for symbol in alphabet:
            next_states = move(states, transitions, current_states, symbol)
            next_closure = set()
            for state in next_states:
                next_closure.update(epsilon_closure(states, transitions, state)) #вычисляем эпсилон-замыкание для следующих состояний
            next_state = ''.join(sorted(next_closure)) #формируем строку из следующих сост-ий ДКА и сортируем ее
            dfa_transitions[(current_state, symbol)] = next_state #добавляем переход в словарь переходов ДКА
            if next_state not in processed_states and next_state not in unprocessed_states:
                unprocessed_states.append(next_closure) #если следующее сост-ие не обработано, добавляем его в список необработанных
                processed_states.add(next_state) #добавляем следующее сост-ие в множ-во обработанных
    return dfa_states, alphabet, dfa_transitions, dfa_initial_states, dfa_final_states #возвращаем сост-ия, алфавит, переходы, начальные и конечные состояния ДКА

def epsilon_closure(states, transitions, state): # Функция epsilon_closure вычисляет эпсилон-замыкание для данного состояния в НКА.
    closure = set() # Создаем пустое множество для хранения эпсилон-замыкания.
    stack = list(state) # Инициализируем стек начальным состоянием.
    while stack: # Запускаем цикл, который будет выполняться, пока стек не пуст.
        current_states = stack.pop() # Извлекаем состояние из стека.
        closure.update(current_states) # Добавляем извлеченное состояние в эпсилон-замыкание.
        for current_state in current_states: # Перебираем каждое текущее состояние из извлеченного множества.
            if (current_state, '') in transitions: # Проверяем, есть ли переход по эпсилону из текущего состояния.
                for next_state in transitions[(current_state, '')]:
                    if next_state not in closure:
                        stack.append({next_state}) # Если следующее состояние не находится в замыкании, добавляем его в стек.
    return closure # Возвращаем эпсилон-замыкание.

def move(states, transitions, state, symbol): # Функция move вычисляет множество состояний, в которые можно перейти из данного состояния по заданному символу.
    next_states = set() # Создаем пустое множество для хранения следующих состояний.
    for s in state: # Перебираем каждое состояние из переданного множества state.
        if (s, symbol) in transitions: # Проверяем, есть ли переход по заданному символу из текущего состояния.
            next_states.update(transitions[(s, symbol)]) # Добавляем следующие состояния в множество next_states.
    return next_states # Возвращаем множество следующих состояний.

def nfa_to_dfa(states, alphabet, transitions, initial_states, final_states): # Функция nfa_to_dfa выполняет конвертацию НКА в ДКА.
    dfa_states = set() # Создаем пустое множество для хранения состояний ДКА.
    dfa_transitions = {} # Создаем пустой словарь для хранения переходов ДКА.
    dfa_initial_states = set() # Создаем пустое множество для хранения начальных состояний ДКА.
    dfa_final_states = set() # Создаем пустое множество для хранения конечных состояний ДКА.
    initial_closure = epsilon_closure(states, transitions, initial_states)
    # Вычисляем эпсилон-замыкание для начальных состояний.
    unprocessed_states = [initial_closure] # Создаем список необработанных состояний, инициализируем начальным замыканием.
    processed_states = set() # Создаем множество уже обработанных состояний.

    while unprocessed_states: #запускаем цикл, к-рый будет выполняться, пока есть необработанные состояния
        current_states = unprocessed_states.pop() #извлекаем текущее состояние из списка необработанных
        current_state = ''.join(sorted(current_states)) #формируем строку из сост-ий ДКА и сортируем ее
        dfa_states.add(current_state) # Добавляем текущее состояние в множество состояний ДКА.
        if initial_closure == current_states:
            dfa_initial_states.add(current_state) # Если текущее состояние соответствует начальному замыканию, добавляем его в начальные состояния ДКА.
        if current_states.intersection(final_states):
            dfa_final_states.add(current_state) #если текущее состояние содержит конечные состояния НКА, добавляем его в конечные состояния ДКА.
        for symbol in alphabet:
            next_states = move(states, transitions, current_states, symbol)
            next_closure = set()
            for state in next_states:
                next_closure.update(epsilon_closure(states, transitions, state)) #Вычисляем эпсилонзамыкание для следующих состояний
            next_state = ''.join(sorted(next_closure)) #формируем строку из следующих сост-ий ДКА и сортируем ее
            dfa_transitions[(current_state, symbol)] = next_state #добавляем переход в словарь переходов ДКА
            if next_state not in processed_states and next_state not in unprocessed_states:
                unprocessed_states.append(next_closure) # Если следующее состояние не обработано, добавляем его в список необработанных.
                processed_states.add(next_state) # Добавляем следующее состояние в множество обработанных.
    return dfa_states, alphabet, dfa_transitions, dfa_initial_states, dfa_final_states # Возвращаем состояния, алфавит, переходы, начальные и конечные состояния ДКА.

def main():
    states = get_states()
    alphabet = get_input_alphabet()
    transitions = get_transitions(states, alphabet)
    initial_states = get_initial_states(states)
    final_states = get_final_states(states)
    dfa_states, dfa_alphabet, dfa_transitions, dfa_initial_states, dfa_final_states = nfa_to_dfa(states,
    alphabet, transitions, initial_states, final_states)
    print("DFA:")
    print(f"Set of states: {', '.join(sorted(dfa_states))}")
    print(f"Input alphabet: {', '.join(sorted(dfa_alphabet))}")
    print("State-transitions function:")
    for (current_state, input_char), next_state in dfa_transitions.items():
        print(f"D({current_state}, {input_char}) = {next_state}")
    print(f"Initial states: {', '.join(sorted(dfa_initial_states))}")
    print(f"Final states: {', '.join(sorted(dfa_final_states))}")

if __name__ == "__main__":
    main()