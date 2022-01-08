import ast

class Parser(ast.NodeVisitor):
    def __init__(self):
        self.functions = dict()
        self.args = dict()
        self.classes = dict()

    def visit_ClassDef(self, node):
        self.classes[node.lineno] = node.name
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions[node.lineno] = node.name
        if node.args.args:
            defaults = list()
            if node.args.defaults:
                _args = list()
                for a in node.args.args:
                    if a.arg != 'self':
                        _args.append(a)

                for n, t in zip(_args, node.args.defaults):
                    _type = ast.dump(t)
                    if 'Constant' not in _type:
                        defaults.append(n.arg)

            self.args.setdefault(node.lineno, list())
            for n in node.args.args:
                self.args[node.lineno].append({'name': n.arg, 'mutable': True if n.arg in defaults else False})
        self.generic_visit(node)
