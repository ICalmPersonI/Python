import math
import re
from collections import deque

class Calculator:
    def __init__(self):
        self.EXPRESSION_PATTERN = \
            re.compile(r'^((((-*\d+)|([A-Za-z]))\s*)|(([+\-^]+|[*/])\s*((-*\d+)|([A-Za-z]))\s*))+$')
        self.VARIABLE_PATTERN = re.compile(r'[A-Za-z]+\s*=+\s*\d*|[A-Za-z]*')
        self.OPERATORS = re.compile(r'[)(+*^\-/]')
        self.LETTERS = re.compile(r'^[A-Za-z]+$')
        self.COMMAND = re.compile(r'^/.+$')
        self.DIGITS = re.compile(r'^\d+$')
        self.replacements = (lambda x: re.sub(r'\s+', ' ', x),
                             lambda x: re.sub(r'\(', ' ( ', x),
                             lambda x: re.sub(r'\)', ' ) ', x),
                             lambda x: re.sub(r'-{2}', '+', x),
                             lambda x: re.sub(r'\++', '+', x),
                             lambda x: re.sub(r'(\+-)|(-\+)', '-', x),
                             lambda x: re.sub(r'\*+', '*', x),
                             lambda x: re.sub(r'/+', '/', x),
                             lambda x: re.sub(r'\^+', '^', x))
        self.variables = dict()
        self.exp = None

    def _calculate(self):
        stack = deque()
        for e in self.exp:
            if re.match(self.OPERATORS, e):
                a, b = (int(stack.pop()), int(stack.pop()))
                if e == '+':
                    stack.append(b + a)
                elif e == '-':
                    stack.append(b - a)
                elif e == '*':
                    stack.append(b * a)
                elif e == '/':
                    stack.append(b / a)
                elif e == '^':
                    stack.append(math.pow(b, a))
            else:
                stack.append(e)
        return stack.pop()

    def _to_postfix(self):
        priority = {'(': 1, '+': 2, '-': 2, '*': 3, '/': 3, '^': 4}
        stack = deque('(')
        postfix_exp = list()
        for e in self.exp.split():
            if re.match(self.OPERATORS, e):
                if e == ')':
                    while True:
                        temp = stack.pop()
                        if temp == '(':
                            break
                        postfix_exp.append(temp)
                elif e != '(' and stack and priority[stack[-1]] >= priority[e]:
                    postfix_exp.append(stack.pop())
                    stack.append(e)
                else:
                    stack.append(e)
            elif re.match(self.LETTERS, e):
                postfix_exp.append(self.variables[e])
            else:
                postfix_exp.append(e)

        while True:
            try:
                temp = stack.pop()
            except IndexError:
                return False
            if temp == '(':
                break
            postfix_exp.append(temp)

        if len(stack) > 1:
            return False

        self.exp = map(lambda x: str(x), postfix_exp)
        return True

    def _expression_parsing(self):
        for r in self.replacements:
            try:
                self.exp = r(self.exp)
            except re.error:
                pass
        return self._to_postfix()

    def _processing_of_variables(self, variable_declaration):
        declaration = list(map(lambda x: x.strip(), variable_declaration.split('=')))
        if re.match(self.LETTERS, declaration[0]):
            if len(declaration) == 1:
                if declaration[0] in self.variables.keys():
                    print(self.variables[declaration[0]])
                else:
                    print('Unknown variable')
            else:
                if re.match(self.LETTERS, declaration[1]):
                    if declaration[1] in self.variables.keys():
                        self.variables[declaration[0]] = self.variables[declaration[1]]
                    else:
                        print('Invalid identifier')
                elif re.match(self.DIGITS, declaration[1]):
                    self.variables[declaration[0]] = int(declaration[1])
                else:
                    print('Invalid assignment')
        else:
            print('Invalid identifier')

    def run(self):
        while True:
            __input = input().strip()
            if __input:
                if re.match(self.COMMAND, __input):
                    if __input == '/exit':
                        print('Bye!')
                        break
                    elif __input == '/help':
                        print('The program calculates the sum of numbers')
                    else:
                        print('Unknown command')
                elif not re.search(self.OPERATORS, __input):
                    self._processing_of_variables(__input)
                else:
                    if re.match(self.EXPRESSION_PATTERN, __input.replace('(', '').replace(')', '')):
                        self.exp = __input
                        if self._expression_parsing():
                            print(self._calculate())
                        else:
                            print('Invalid expression')
                    else:
                        print('Invalid expression')


if __name__ == '__main__':
    Calculator().run()
