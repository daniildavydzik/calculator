class ObjectBuilder:
    letter_reg = r'[A-Za-z]'

    def trio_builder(self, top_lec, left_lec, right_lec, top, left, right, top_object):
        if top_object is None:
            top_trio = top
            top_trio.lec = top_lec
        else:
            top_trio = top_object

        if left_lec and left:
            left_trio = left
            left_trio.lec = left_lec
            right_trio = right
            right_trio.lec = right_lec

            top_trio.childrenLeft = left_trio
            top_trio.childrenRight = right_trio
            left_trio.parent = top_trio
            right_trio.parent = top_trio
        else:
            left_trio = None
            right_trio = right
            right_trio.lec = right_lec
            top_trio.childrenRight = right_trio
            right_trio.parent = top_trio

        if top_object is None:
            trio = [top_trio, left_trio, right_trio]
        else:
            trio = [left_trio, right_trio]
        return trio

    def stop_build(self, node_array):
        for node in node_array:
            if node:
                if len(node.lec) > 1 and node.childrenLeft is None and node.childrenRight is None:
                    return False
        return True

    def search_top(self, ar_node):
        for node in ar_node:
            if node:
                if len(node.lec) > 1 and node.childrenLeft is None and node.childrenRight is None:
                    return node
