from char_type import charType
from nfa_state import NFAState


def computeRegEx(ExpTree):
    if ExpTree.charType == charType.CONCAT:
        return concat(ExpTree)
    elif ExpTree.charType == charType.UNION:
        return union(ExpTree)
    elif ExpTree.charType == charType.KLEENE:
        return kleeneClosure(ExpTree)
    elif ExpTree.charType == charType.POSITIVE:
        return positiveClosure(ExpTree)
    elif ExpTree.charType == charType.OPTIONAL:
        return optional(ExpTree)
    else:
        return evaluateOperation(ExpTree)


def evaluateOperation(ExpTree):
    start = NFAState()
    end = NFAState()

    start.next_state[ExpTree.value] = [end]
    return start, end


def concat(ExpTree):
    left_nfa = computeRegEx(ExpTree.left)
    right_nfa = computeRegEx(ExpTree.right)

    left_nfa[1].next_state['λ'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]


def union(ExpTree):
    start = NFAState()
    end = NFAState()

    first_nfa = computeRegEx(ExpTree.left)
    second_nfa = computeRegEx(ExpTree.right)

    start.next_state['λ'] = [first_nfa[0], second_nfa[0]]
    first_nfa[1].next_state['λ'] = [end]
    second_nfa[1].next_state['λ'] = [end]

    return start, end


def kleeneClosure(ExpTree):
    start = NFAState()
    end = NFAState()

    starred_nfa = computeRegEx(ExpTree.left)

    start.next_state['λ'] = [starred_nfa[0], end]
    starred_nfa[1].next_state['λ'] = [starred_nfa[0], end]

    return start, end


def positiveClosure(ExpTree):
    start = NFAState()
    end = NFAState()

    starred_nfa = computeRegEx(ExpTree.left)

    start.next_state['λ'] = [starred_nfa[0]]
    starred_nfa[1].next_state['λ'] = [starred_nfa[0], end]

    return start, end


def optional(ExpTree):
    start = NFAState()
    end = NFAState()

    optional_nfa = computeRegEx(ExpTree.left)

    start.next_state['λ'] = [optional_nfa[0], end]
    optional_nfa[1].next_state['λ'] = [end]

    return start, end