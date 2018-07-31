
def par_check(expression):
    mapping = dict(zip('({[', ')}]'))
    queue = []
    for letter in expression:
        if letter in mapping:
            queue.append(mapping[letter])
        elif letter not in mapping.values():
            continue
        elif not (queue and letter == queue.pop()):
            return False
    return not queue
