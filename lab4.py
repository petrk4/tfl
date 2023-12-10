class DFA:
    # Инициализация ДКА
    def __init__(self, states, alphabet, transition_function, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.final_states = final_states
class NFA:
    # Инициализация НКА
    def __init__(self, states, alphabet, transition_function, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.final_states = final_states

    # Метод преобразования в ДКА
    def to_dfa(self):
        # Определение начального состояния и инициализация структур данных
        initial_state = frozenset([self.initial_state])
        queue = [initial_state]
        dfa_states = set([initial_state])
        dfa_transition_function = {}
        dfa_final_states = set()

        # Основной цикл преобразования НКА в ДКА
        while queue:
            current_dfa_state = queue.pop(0)
            for symbol in self.alphabet:
                # Создание нового состояния ДКА
                next_state = set()
                for nfa_state in current_dfa_state:
                    # Объединение множества следующих состояний с возможными переходами из NFA
                    next_state |= self.transition_function.get((nfa_state, symbol), set())
                next_state = frozenset(next_state)
                dfa_transition_function[(current_dfa_state, symbol)] = next_state
                # Если следующее состояние ещё не обработано, то добавить в очередь и множество состояний DFA
                if next_state not in dfa_states:
                    queue.append(next_state)
                    dfa_states.add(next_state)
                # Если следующее состояние содержит конечное состояние NFA, добавить его в конечные состояния DFA
                if next_state.intersection(self.final_states):
                    dfa_final_states.add(next_state)

        # Возвращаем новый ДКА
        return DFA(
            states=list(dfa_states),
            alphabet=self.alphabet,
            transition_function={ (state, char): next_state
                                  for (state, char), next_state in dfa_transition_function.items() },
            initial_state=initial_state,
            final_states=list(dfa_final_states)
        )


def process_transitions(transitions_str):
    transitions = {}
    # Разделяем ввод на отдельные переходы
    for transition in transitions_str.strip().split(','):
        parts = transition.strip().split()
        if len(parts) == 3:
            state, symbol, next_state = parts
            # Если такой переход уже существует, добавляем новое состояние в множество
            if (state, symbol) in transitions:
                transitions[(state, symbol)].add(next_state)
            else:
                transitions[(state, symbol)] = {next_state}
    return transitions



# Ввод остальных компонентов НКА
states = set(input("Enter set of states: ").split())
alphabet = set(input("Enter the input alphabet: ").split())
transitions_input = input("Enter state-transitions function: ")
transitions = process_transitions(transitions_input)
initial_state = input("Enter a set of initial states: ")
final_states = set(input("Enter a set of final states: ").split())

nfa = NFA(states, alphabet, transitions, initial_state, final_states)
dfa = nfa.to_dfa()

# Сортируем состояния для консистентного вывода
sorted_states = sorted(map(lambda x: ''.join(sorted(x)), dfa.states))
sorted_final_states = sorted(map(lambda x: ''.join(sorted(x)), dfa.final_states))

# Вывод результатов преобразования НКА в ДКА
print("DFA:")
print("Set of states:", ', '.join(sorted_states))
print("Input alphabet:", ', '.join(sorted(dfa.alphabet)))
print("State-transitions function:")
sorted_transitions = sorted(dfa.transition_function.items(), key=lambda x: (''.join(sorted(x[0][0])), x[0][1]))
for (current_state, symbol), next_states in sorted_transitions:
    state_string = ''.join(sorted(current_state))
    next_state_string = ''.join(sorted(next_states))
    print(f"D({state_string}, {symbol}) = {next_state_string}")
print("Initial states:", ''.join(sorted(dfa.initial_state)))
print("Final states:", ', '.join(sorted_final_states))
