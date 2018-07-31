import re
import object_types
from function_parser import FunctionParser
from par_checker import par_check

tpl = r'^[0-9]*[.,]?[0-9]+$'
letter_reg = r'[A-Za-z]'
spaces_reg = '\s+'
print(re.match(tpl, '9'))
operation_points = {
    '+': object_types.Plus,
    '-': object_types.Minus,
    '/': object_types.Divide,
    '*': object_types.Multiply,
    '^': object_types.Pow,
    ',': object_types.Comma,
    'func': object_types.Function,
}

priority_dict = {
    ',': (4, 1),
    '+': (3, 1),
    '-': (3, 1),
    '*': (2, 1),
    '/': (2, 1),
    '^': (1, 2),
}


class Error(Exception):
    pass


def pre_tokinaze(str):
    str.lower()
    print(par_check(str))
    if par_check(str):
        normalize_str = normalize_string(str)
        valid_string = validate_string(normalize_str).replace(" ", "")
        return valid_string
    else:
        raise Error('Brackets not balanced')


def normalize_string(str):
    return re.sub(spaces_reg, ' ', str).strip()


def validate_string(str):
    indecis = enumerate(str)
    arr = ['<', '>', '=']
    for i, char in indecis:
        # print(char)
        if char in arr:
            print(char)
            if str[i + 1] == ' ' and str[i + 2] == '=':
                raise Error('invalid syntax')
        elif char.isdigit() and i != len(str) - 1:
            if str[i + 1] == ' ' and str[i + 2].isdigit():
                raise Error('invalid syntax')

    return str


def add_multiply_sign(arr_lex):
    i = 0
    while i != len(arr_lex) - 1:
        if re.match(tpl, arr_lex[i]) and arr_lex[i + 1] == '(':
            arr_lex.insert(i + 1, '*')
        elif re.match(tpl, arr_lex[i]) and re.match(letter_reg, arr_lex[i + 1]):
            arr_lex.insert(i + 1, '*')
        elif arr_lex[i] == ')' and re.match(tpl, arr_lex[i + 1]):
            arr_lex.insert(i + 1, '*')
        elif re.match(letter_reg, arr_lex[i]) and re.match(tpl, arr_lex[i + 1]):
            arr_lex.insert(i + 1, '*')
        elif arr_lex[i] == ')' and arr_lex[i + 1] == '(':
            print('shit' * 100)
            # left_lex = remove_brackets(arr_lex[0:i+1])
            # right_lex = remove_brackets(arr_lex[i+1:])
            arr_lex.insert(i + 1, '*')
            print(arr_lex)
            # if len(left_lex + right_lex) != len(arr_lex):
            #     i -= 2
            # arr_lex = left_lex + right_lex
        i += 1

    return arr_lex


def get_lexem_array(str):
    new_str = pre_tokinaze(str)
    if new_str is None:
        return '0'
    n = len(new_str)
    j = 0
    ar_lec = []
    accum = new_str[0]

    for i in range(1, n + 1):
        if i == n:
            ar_lec.insert(j, accum)
            break

        if (accum == '-' or accum == '+') and i == 1:
            ar_lec.append('0')
            ar_lec.append(accum)
            j += 2
            accum = new_str[i]
            continue

        if re.match(tpl, accum[0]) and (re.match(tpl, new_str[i]) or new_str[i] == '.'):
            accum += new_str[i]
            continue

        if new_str[i].isalpha() and re.match(letter_reg, accum):
            accum += new_str[i]
        else:
            ar_lec.insert(j, accum)
            j += 1
            accum = new_str[i]
    ar_lec = remove_unary_minus(ar_lec)
    lexem_array = add_multiply_sign(ar_lec)
    # end_string = what_a_fuck(lexem_array)
    # print(f'end_string {end_string}')
    return lexem_array


def remove_unary_minus(ar_lec):
    sign_arr = []
    i = len(ar_lec) - 1
    start_index = None
    while i != -1:
        if ar_lec[i] != '-' and ar_lec[i] != '+':
            start_index = i
            i -= 1
            continue
        if ar_lec[i] == '-' or ar_lec[i] == '+':
            sign_arr.append(ar_lec[i])
            i -= 1

        if ar_lec[i] != '-' and ar_lec[i] != '+' and ar_lec[i] != '(' and len(sign_arr) >= 0:
            end_index = i
            sign_arr = list(filter(lambda a: a == '-', sign_arr))
            if start_index is None:
                raise Error('not valid')
            if len(sign_arr) % 2 == 0:
                ar_lec[end_index + 1:start_index] = ['+']
                sign_arr.clear()
            else:
                ar_lec[end_index + 1:start_index] = ['-']
                sign_arr.clear()

        if ar_lec[i] == '(' and len(sign_arr) >= 0:
            end_index = i
            sign_arr = list(filter(lambda a: a == '-', sign_arr))
            if len(sign_arr) % 2 != 0:
                ar_lec[end_index + 1:start_index] = ['-']
                ar_lec.insert(end_index + 1, '0')
                sign_arr.clear()
    # print(ar_lec)
    return ar_lec


def validation_brackets(objects_array):
    i = 0
    stack = []
    if len(objects_array) == 1:
        return objects_array
    while i != len(objects_array):

        if i in range(2,len(objects_array)-1):
            condition_array = [isinstance(objects_array[i - 2], object_types.CloseBracket),
                               isinstance(objects_array[i - 2], object_types.Number), \
                               isinstance(objects_array[i - 2], object_types.Function)]
            operators_conditions = [isinstance(objects_array[i - 1], object_types.Pow),
                                    isinstance(objects_array[i - 1], object_types.Multiply), \
                                    isinstance(objects_array[i - 1], object_types.Divide)]

        if isinstance(objects_array[i], object_types.OpenBracket):
            if isinstance(objects_array[i + 1], object_types.OpenBracket):
                stack.append(-i)

            else:
                stack.append(i)
            if i >= 2 and any(condition_array) and any(operators_conditions) and isinstance(objects_array[i + 1], object_types.OpenBracket):
                stack.pop()
            i += 1
        elif isinstance(objects_array[i], object_types.CloseBracket):
            if len(stack) > 0:
                top = stack[-1]
            else:
                i += 1
                continue
            if (isinstance(objects_array[i - 1], object_types.CloseBracket) or i == len(
                    objects_array) - 1) and top <= 0:
                objects_array.pop(-top)
                objects_array.pop(i - 1)
                i -= 2
                stack.pop()
            elif isinstance(objects_array[i - 1], object_types.CloseBracket) and top >= 0:
                objects_array.pop(top)
                objects_array.pop(i - 1)
                i -= 2
                stack.pop()
            elif not isinstance(objects_array[i - 1], object_types.CloseBracket) and top != 0:
                stack.pop()
        else:
            i += 1
        i += 1
    if len(objects_array) == 3 and isinstance(objects_array[0], object_types.OpenBracket) and isinstance(objects_array[2], object_types.CloseBracket):
        objects_array = [objects_array[1]]
    elif len(objects_array) == 2 and isinstance(objects_array[0], object_types.OpenBracket) and isinstance(objects_array[1], object_types.CloseBracket):
        objects_array = []
    return objects_array


def get_objects_array(lexem_array):
    object_array = []
    for lexe in lexem_array:
        if re.match(tpl, lexe):
            object_type = object_types.Number
            node = object_type(0, 1)
            node.number = float(lexe)

        elif lexe in FunctionParser.functions_dict:
            func = FunctionParser.functions_dict.get(lexe, None)
            object_type = operation_points['func']
            node = object_type(1, 1)
            node.function = func

        elif lexe in FunctionParser.constants_dict:
            const = FunctionParser.constants_dict[lexe]
            object_type = object_types.Const
            node = object_type(0, 1)
            node.const = const

        elif lexe == '(' or lexe == ')':
            object_type = object_types.OpenBracket if lexe == '(' else object_types.CloseBracket
            node = object_type()
        elif lexe in operation_points:
            if lexem_array[len(object_array) - 1] in operation_points:
                object_type = object_types.UnaryMinus
                node = object_type(1, 1)
            else:
                object_type = operation_points[lexe]
                priority, associativity = priority_dict[lexe]
                node = object_type(priority, associativity)
        else:
            raise Error(f"unknown type '{lexe}' ")

        object_array.append(node)
    return object_array


def remove_brackets(str):
    while len(str) != 0:
        if str[0] == '(' and str[len(str) - 1] == ')':
            string = str[1:len(str) - 1]
            return string
        else:
            return str


def validate_expression(lex_arr):
    raise Error(f"unknown type '' ")
    i = 0
    stack = []
    print(f'stack {i} === {stack}')
    while i != len(lex_arr):
        print(f'stack {i} === {stack}')
        if lex_arr[i] == '(':
            raise Error(f"unknown type '' ")
            if lex_arr[i + 1] == '(':
                stack.append(-i)
            else:
                stack.append(i)
            i += 1
        elif lex_arr[i] != '(' and lex_arr[i] != ')':
            i += 1
        elif lex_arr[i] == ')':
            top = lex_arr[-1]
            if lex_arr[i - 1] == ')' and top < 0:
                lex_arr[-top] = '$'
                lex_arr[i] = '$'
                stack.pop()
            elif lex_arr[i - 1] == ')' and top > 0:
                raise Error('error with brackets')
            elif lex_arr[i - 1] != ')' and top > 0:
                stack.pop()
            i += 1
    arr = remove_brackets(lex_arr)
    return arr


def validate(obj_arr):
    if isinstance(obj_arr[0], object_types.OpenBracket) and  isinstance(obj_arr[len(obj_arr)-1], object_types.CloseBracket):
        obj_arr = obj_arr[1:len(obj_arr)-1]
    return obj_arr
