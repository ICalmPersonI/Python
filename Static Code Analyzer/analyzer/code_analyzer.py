import os
import re
import sys
import ast
from code_parser import Parser


class CodeAnalyzer:

    def __init__(self, dir_or_file):
        self.dir_or_file = dir_or_file
        self.parser = None

        self.line_number = 0
        self.line = None

        self.blank_lines = 0

        self.SNAKE_CASE = re.compile('^(_*[a-z]*_*[a-z]*[0-9]*_*)+$')
        self.CAMEL_CASE = re.compile('^[A-Z].*([A-Z].*)*$')
        self.S003_PATTERN = re.compile('^[^#]+;[^\';].*$')
        self.S004_PATTERN = re.compile('\s\s#')
        self.S005_PATTERN = re.compile('#.*TODO')
        self.S007_PATTERN_CLASS = re.compile(' *class( {2,}).+:')
        self.S007_PATTERN_DEF = re.compile(' *def( {2,}).+:')

    def _s001(self):
        if len(self.line) > 79:
            return f'Line {self.line_number}: S001 Too long'

    def _s002(self):
        indentation = 0
        for c in self.line:
            if c == ' ':
                indentation += 1
            else:
                break
        if indentation % 4 != 0:
            return f'Line {self.line_number}: S002 Indentation is not a multiple of four'

    def _s003(self):
        if re.match(self.S003_PATTERN, self.line):
            return f'Line {self.line_number}: S003 Unnecessary semicolon'

    def _s004(self):
        for i in range(len(self.line)):
            if self.line[i] == '#':
                if i != 0 and (i == 1 or not re.search(self.S004_PATTERN, self.line)):
                    return f'Line {self.line_number}: S004 At least two spaces required before inline comments'

    def _s005(self):
        if re.search(self.S005_PATTERN, self.line.upper()):
            return f'Line {self.line_number}: S005 TODO found'

    def _s006(self):
        if len(self.line) != 0 and self.blank_lines > 2:
            self.blank_lines = 0
            return f'Line {self.line_number}: S006 More than two blank lines used before this line'
        if re.match('^\n', self.line):
            self.blank_lines += 1
        else:
            self.blank_lines = 0

    def _s007(self):
        if re.match(self.S007_PATTERN_CLASS, self.line):
            return f"Line {self.line_number}: S007 Too many spaces after 'class'"
        if re.match(self.S007_PATTERN_DEF, self.line):
            return f"Line {self.line_number}: S007 Too many spaces after 'def'"

    def _s008(self):
        if self.line_number in self.parser.classes.keys():
            name = self.parser.classes[self.line_number]
            if not re.match(self.CAMEL_CASE, name):
                return f"Line {self.line_number}: S008 Class name '{name}' should use CamelCase"

    def _s009(self):
        if self.line_number in self.parser.functions.keys():
            name = self.parser.functions[self.line_number]
            if not re.match(self.SNAKE_CASE, name):
                return f"Line {self.line_number}: S009 Function name '{name}' should use snake_case"

    def _s010(self):
        if self.line_number in self.parser.args.keys():
            for arg in self.parser.args[self.line_number]:
                if not re.match(self.SNAKE_CASE, arg['name']):
                    name = arg['name']
                    return f"Line {self.line_number}: S010 Argument name '{name}' should be snake_case"

    def _s011(self):
        self.line = self.line.replace('self.', '')
        if re.match('.+ = .+.*', self.line) and not re.match(self.SNAKE_CASE, self.line.split()[0]):
            return f"Line {self.line_number}: S011 Variable '{self.line.split()[0]}' in function should be snake_case"

    def _s012(self):
        if self.line_number in self.parser.args.keys():
            for arg in self.parser.args[self.line_number]:
                if arg['mutable']:
                    return f'Line {self.line_number}: S012 Default argument value is mutable'

    def _check_line(self, print_path):
        rules = (lambda: self._s001(), lambda: self._s002(), lambda: self._s003(), lambda: self._s004(),
                 lambda: self._s005(), lambda: self._s006(), lambda: self._s007(), lambda: self._s008(),
                 lambda: self._s009(), lambda: self._s010(), lambda: self._s011(), lambda: self._s012())
        for r in rules:
            message = r()
            if message:
                print(f'{print_path}: {message}')

    def _read_file(self, path, print_path):
        with open(path, 'r', encoding='utf-8') as f:
            file_content = f.readlines()
            tree = ast.parse(''.join(line for line in file_content))
            self.parser = Parser()
            self.parser.visit(tree)
            for number, line in enumerate(file_content):
                self.line_number = number + 1
                self.line = line
                self._check_line(print_path)
            f.close()

    def run(self):
        try:
            for entry in os.listdir(self.dir_or_file):
                path = self.dir_or_file + os.sep + entry
                if entry.split('.')[-1] == 'py':
                    self._read_file(path, path)
        except (FileNotFoundError, NotADirectoryError):
            path = sys.path[1] + os.sep + self.dir_or_file
            self._read_file(path, self.dir_or_file)


if __name__ == '__main__':
    args = sys.argv
    CodeAnalyzer(args[-1]).run()
