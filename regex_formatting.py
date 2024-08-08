import re

operators = ['+', '*', '^', '.', '?', '(', ')']


def validateRegex(regex):
    if not regex:
        raise ValueError("Empty regex")
    stack = []
    for char in regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                raise ValueError("Unbalanced parentheses in regex")
            stack.pop()
    if stack:
        raise ValueError("Unbalanced parentheses in regex")

    # Check syntax of {min, max} and [start - end]
    min_max_pattern = re.compile(r"\{(?P<min>\d*),(?P<max>\d*)\}")
    range_pattern = re.compile(r"\[(?P<start>.+)-(?P<end>.+)\]")
    for match in min_max_pattern.finditer(regex):
        min_val = match.group('min')
        max_val = match.group('max')
        if min_val and max_val and int(min_val) > int(max_val):
            raise ValueError(f"Invalid min-max values in regex: '{min_val}' is greater than '{max_val}'")
    for match in range_pattern.finditer(regex):
        start_val = match.group('start')
        end_val = match.group('end')
        if start_val and end_val and ord(start_val) > ord(end_val):
            raise ValueError(f"Invalid range values in regex: '{start_val}' comes after '{end_val}' in ASCII")

    return True


def formatRange(RE):
    pattern = re.compile(r"\[(?P<start>.+)-(?P<end>.+)\]")
    while True:
        match = pattern.search(RE)
        if not match:
            break
        start = match.group('start')
        end = match.group('end')

        if not start.isascii() or not end.isascii():
            raise ValueError(f"Invalid range values in regex: '{start}' or '{end}' is not a valid ASCII character")

        if ord(start) > ord(end):
            raise ValueError(f"Invalid range values in regex: '{start}' comes after '{end}' in ASCII")

        replacement = '+'.join(f"{chr(i)}" for i in range(ord(start), ord(end) + 1))
        replacement = f"({replacement})"
        RE = RE[:match.start()] + replacement + RE[match.end():]
    return RE


def formatMinMax(regex):
    pattern = re.compile(r"(?P<block>\(.*\)|\w[^{]*)\{(?P<min>\d*),(?P<max>\d*)\}")
    while True:
        match = pattern.search(regex)
        if not match:
            break
        block = match.group('block')
        if block[-1] in operators and block[-1]not in ['(', ')']:
            raise ValueError(f"Invalid regex: '{block[-1]}' is an operator and cannot precede '{{}}'")
        min_val = match.group('min')
        max_val = match.group('max')
        if min_val == '':
            min_val = 0
        else:
            min_val = int(min_val)

        if max_val == '':
            max_val = None
        else:
            max_val = int(max_val)

        if max_val is not None and min_val > max_val:
            raise ValueError(f"Invalid min-max values in regex: '{min_val}' is greater than '{max_val}'")

        replacement = block * min_val
        if max_val is None:
            replacement += f"({block})*"
        else:
            replacement += ''.join(f"{block}?" for _ in range(min_val, max_val))
        replacement = f"({replacement})"
        regex = regex[:match.start()] + replacement + regex[match.end():]
    return regex

def addConcatenation(RE):
    length = len(RE)
    res = []
    for i in range(length - 1):
        res.append(RE[i])
        if RE[i] not in operators:
            if RE[i + 1] not in operators or RE[i + 1] == '(':
                res += '.'
        if RE[i] == ')' and RE[i + 1] == '(':
            res += '.'
        if RE[i] in ['*', '^', '?'] and RE[i + 1] == '(':
            res += '.'
        if RE[i] in ['*', '^', '?'] and RE[i + 1] not in operators:
            res += '.'
        if RE[i] == ')' and RE[i + 1] not in operators:
            res += '.'
    res += RE[length - 1]
    return "".join(res)


def infixToPostfix(RE):
    stk = []
    formattedRegEx = ""
    for char in RE:
        if char not in operators or char in ['*', '^', '?']:
            formattedRegEx += char
        elif char == ")":
            while len(stk) > 0 and stk[-1] != "(":
                formattedRegEx += stk.pop()
            stk.pop()
        elif char == "(":
            stk.append(char)
        elif len(stk) == 0 or stk[-1] == "(" or operators.index(char) > operators.index(stk[-1]):
            stk.append(char)
        else:
            while len(stk) > 0 and stk[-1] != "(" and operators.index(char) <= operators.index(stk[-1]):
                formattedRegEx += stk.pop()
            stk.append(char)
    while len(stk) > 0:
        formattedRegEx += stk.pop()

    return formattedRegEx


def formatRegex(RE):
    RE = RE.replace(" ", "")
    RE = formatRange(RE)
    RE = formatMinMax(RE)
    RE = addConcatenation(RE)
    RE = infixToPostfix(RE)
    return RE

