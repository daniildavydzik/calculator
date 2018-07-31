OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y) , 'sin' : (3, lambda x, y: x / y ), ',': (0, lambda x, y: x / y)}


def shunting_yard(parsed_formula):
    stack = []
    for token in parsed_formula:
        if token in OPERATORS:
            while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            stack.append(token)
        else:
            yield token
    while stack:
        yield stack.pop()
    print(stack)


def postfix_to_infix(formula):
    stack = []
    prev_op = None
    for ch in formula:
        if not ch in OPERATORS:
            stack.append(ch)
        elif len(stack) > 1:

            b = stack.pop()
            a = stack.pop()
            if prev_op and len(a) > 1 and OPERATORS[ch][0] > OPERATORS[prev_op][0]:
                expr = '('+a+')' + ch + b
            else:
                expr = a + ch + b
            stack.append(expr)
            prev_op = ch
    print(stack[-1])
    return stack[-1]

