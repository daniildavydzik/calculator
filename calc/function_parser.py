import importlib


class FunctionParser:
    functions_dict = {}
    constants_dict = {}

    def __init__(self, modules):
        for module in modules:
            modul = importlib.import_module(module)
            for object in vars(modul):
                if object[0:2] != '__':
                    if isinstance(vars(modul)[object], (int, float, complex)):
                       self.constants_dict[object] = vars(modul)[object]
                    else:
                        self.functions_dict[object] = vars(modul)[object]



