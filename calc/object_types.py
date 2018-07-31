from abc import ABC, abstractclassmethod, abstractmethod

class Term(ABC):

    def __init__(self, priority, associativity):
        self.number = None
        self.childrenLeft = None
        self.childrenRight = None
        self.parent = None
        self.lec = None
        self.const = None
        self.function = None
        self.priority = priority
        self.associativity = associativity

    @abstractmethod
    def calc(self):
        pass


class Plus(Term):
    def calc(self):
        return self.childrenLeft.calc() + self.childrenRight.calc()


class Minus(Term):
    def calc(self):
        return self.childrenLeft.calc() - self.childrenRight.calc()


class Multiply(Term):
    def calc(self):
        return self.childrenLeft.calc() * self.childrenRight.calc()


class Pow(Term):
    def calc(self):
        return self.childrenLeft.calc() ** self.childrenRight.calc()


class Divide(Term):
    def calc(self):
        return self.childrenLeft.calc() / self.childrenRight.calc()


class Const(Term):
    def calc(self):
        return self.const


class Number(Term):
    def calc(self):
        return self.number


class Function(Term):
    def calc(self):
        value = self.childrenRight.calc()
        return self.function(*value) if type(value) is list else self.function(*[value])


class Comma(Term):
    def calc(self):
        arguments = [self.childrenLeft.calc(), self.childrenRight.calc()]
        print(type(arguments))
        return arguments


class Bracket():
    def __init__(self, name):
        self.name = name


class OpenBracket():
    pass


class CloseBracket():
    pass


class UnaryMinus(Term):
    def calc(self):
        return 0 - self.childrenRight.calc()