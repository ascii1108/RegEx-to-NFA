from char_type import charType


class ExpressionTree:
    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None


def createExpressionTree(regEx):
    stack = []
    for char in regEx:
        if char == "+":
            z = ExpressionTree(charType.UNION)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)

        elif char == "^":
            z = ExpressionTree(charType.POSITIVE)
            z.left = stack.pop()
            stack.append(z)

        elif char == "?":
            z = ExpressionTree(charType.OPTIONAL)
            z.left = stack.pop()
            stack.append(z)

        elif char == ".":
            z = ExpressionTree(charType.CONCAT)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif char == "*":
            z = ExpressionTree(charType.KLEENE)
            z.left = stack.pop()
            stack.append(z)
        elif char == "(" or char == ")":
            continue
        else:
            stack.append(ExpressionTree(charType.SYMBOL, char))
    return stack[0]
