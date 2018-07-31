from main import get_lexem_array, get_objects_array, validation_brackets, validate
from object_builder import ObjectBuilder
from function_parser import FunctionParser
import object_types

tpl = r'^[0-9]*[.,]?[0-9]+$'
letter_reg = r'[A-Za-z]'


class TreeBuilder:

    def __init__(self):
        self.arr_node = []

    def infl_point(self, lec_str):
        infl_point = 0
        self.max_prior = 0
        br = 0
        lec_arr = enumerate(lec_str)
        for index, lec in lec_arr:

            if isinstance(lec, object_types.Number) or isinstance(lec, object_types.Const):
                continue

            if isinstance(lec, object_types.OpenBracket):
                br += 1
                continue
            elif isinstance(lec, object_types.CloseBracket):
                br -= 1
                continue

            prior = lec.priority - 3 * br

            if lec.associativity == 1:
                if prior > self.max_prior and isinstance(lec_str[infl_point], object_types.Function):
                    self.max_prior = prior
                    infl_point = index
                    continue
                elif prior > self.max_prior:
                    self.max_prior = prior
                    infl_point = index
            else:
                if prior > self.max_prior:
                    self.max_prior = prior
                    infl_point = index
                elif prior >= self.max_prior and isinstance(lec_str[infl_point], object_types.Function):
                    self.max_prior = prior
                    infl_point = index
                    continue

        return infl_point

    def build_ar_node(self, lec, left_lec, right_lec, top_element, top_obj):
        left_element = None
        object_builder = ObjectBuilder()
        if left_lec:
            left_lec = validate(left_lec)
            left_index = self.infl_point(left_lec)
            left_element = left_lec[left_index]
        right_lec = validate(right_lec)

        right_index = self.infl_point(right_lec)
        right_element = right_lec[right_index]
        trio = object_builder.trio_builder(lec, left_lec, right_lec, top_element, left_element, right_element, top_obj)

        return trio

    def build_tree(self, str):
        lec1 = get_lexem_array(str)
        lec = get_objects_array(lec1)
        if len(lec) == 1 and isinstance(lec[0], object_types.Number):
            return lec[0].number
        elif len(lec) == 0:
            return 0

        top_index = self.infl_point(lec)
        top_element = lec[top_index]
        object_builder = ObjectBuilder()
        if isinstance(top_element, object_types.Function) or isinstance(top_element, object_types.UnaryMinus):
            print(lec)
            left_lec = None
            right_lec = lec[1:]
        else:
            left_lec = lec[0:top_index]
            right_lec = lec[top_index + 1:]

        ar_node = self.build_ar_node(lec, left_lec, right_lec, top_element, None)
        while object_builder.stop_build(ar_node) is False:
            top_trio = object_builder.search_top(ar_node)
            print(top_trio)
            lec = top_trio.lec
            top_index = self.infl_point(lec)
            if isinstance(lec[top_index], object_types.Function) or isinstance(top_element, object_types.UnaryMinus):
                left_lec = None
                right_lec = lec[1:]
            else:
                left_lec = lec[0:top_index]
                right_lec = lec[top_index + 1:]

            duo = self.build_ar_node(None, left_lec, right_lec, None, top_trio)
            ar_node = ar_node + duo
        for node in ar_node:
            if node:
                if node.parent is None:
                    result = node.calc()
                    print(f'result{result}')
        return result


if __name__ == '__main__':
    obj = FunctionParser(['math'])
    builder = TreeBuilder()
    string1 = '5*(3+3*(5*5))'
    arr_node = builder.build_tree(string1)
    print(f'result {arr_node}')
