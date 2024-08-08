def arrangeTransitions(state, completedStates, symbol_table, nfa):
    if state in completedStates:
        return
    completedStates.append(state)
    for symbol in list(state.next_state):
        if symbol not in nfa['letters']:
            nfa['letters'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "Q" + str(symbol_table[ns])
                nfa['states'].append(q_state)
            if len(ns.next_state) == 1 and 'λ' in ns.next_state:
                for next_ns in ns.next_state['λ']:
                    if next_ns not in symbol_table:
                        symbol_table[next_ns] = sorted(symbol_table.values())[-1] + 1
                        q_next_state = "Q" + str(symbol_table[next_ns])
                        nfa['states'].append(q_next_state)
                    nfa['transitionFunction'].append(
                        ["Q" + str(symbol_table[state]), symbol, "Q" + str(symbol_table[next_ns])])
            else:
                nfa['transitionFunction'].append(["Q" + str(symbol_table[state]), symbol, "Q" + str(symbol_table[ns])])
        for ns in state.next_state[symbol]:
            arrangeTransitions(ns, completedStates, symbol_table, nfa)


def reachableStates(start_state, transitionFunction):
    reachable = set()
    stack = [start_state]
    while stack:
        state = stack.pop()
        reachable.add(state)
        for transition in transitionFunction:
            if transition[0] == state and transition[2] not in reachable:
                stack.append(transition[2])
    return reachable


def calcFinalStates(nfa):
    for st in nfa["states"]:
        count = 0
        for val in nfa['transitionFunction']:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in nfa["finalStates"]:
            nfa["finalStates"].append(st)


def renameStates(states):
    return {state: "Q" + str(i) for i, state in enumerate(sorted(states, key=lambda x: int(x[1:])))}


def arrangeNFA(fa):
    NFA = {'states': [], 'letters': [], 'transitionFunction': [], 'start_state': None, 'finalStates': []}
    q0 = "Q" + str(0)
    NFA['states'].append(q0)
    arrangeTransitions(fa[0], [], {fa[0]: 0}, NFA)
    calcFinalStates(NFA)
    NFA["start_state"] = "Q0"
    reachable = reachableStates("Q0", NFA['transitionFunction'])

    NFA['states'] = [state for state in NFA['states'] if state in reachable]
    NFA['transitionFunction'] = [transition for transition in NFA['transitionFunction'] if
                                 transition[0] in reachable and transition[2] in reachable]
    NFA['finalStates'] = [state for state in NFA['finalStates'] if state in reachable]

    # NFA = removeLambdaStates(NFA)
    new_state_names = renameStates(NFA['states'])

    NFA['states'] = [new_state_names[state] for state in NFA['states']]
    NFA['transitionFunction'] = [[new_state_names[transition[0]], transition[1], new_state_names[transition[2]]] for
                                 transition in NFA['transitionFunction']]
    NFA['start_state'] = new_state_names[NFA['start_state']]
    NFA['finalStates'] = [new_state_names[state] for state in NFA['finalStates']]

    return NFA
