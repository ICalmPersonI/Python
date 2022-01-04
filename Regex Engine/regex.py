class Regex:

    def _parsing_text(self, exp, text):
        e_index = 0
        t_index = 0
        while True:
            if e_index > len(exp) - 1:
                return True
            if exp[e_index] == '$' and len(text[t_index:]) != 0:
                return False
            elif exp[e_index] == '$':
                return True
            if exp[e_index] == '\\':
                e_index += 1
                continue

            if (exp[e_index] != text[t_index]
                    and ((e_index - 1 > 0 and exp[e_index - 1] != '\\' and exp[e_index] != '.')
                         or exp[e_index] != '.')):
                if exp[e_index] not in ('?', '*', '+'):
                    if e_index + 1 < len(exp) and exp[e_index + 1] in ('?', '*', '+'):
                        e_index += 1
                if exp[e_index] in ('?', '*', '+') and exp[e_index - 1] != '\\':
                    count = 0
                    if exp[e_index] == '?':
                        pass
                    elif exp[e_index] == '*':
                        for c in text[t_index:]:
                            if c != exp[e_index - 1] and exp[e_index - 1] != '.':
                                break
                            count += 1
                    elif exp[e_index] == '+':
                        if exp[e_index - 1] != text[t_index - 1] and exp[e_index - 1] != '.':
                            return False
                        for c in text[t_index:]:
                            if c != exp[e_index - 1] and exp[e_index - 1] != '.':
                                break
                            if e_index + 1 < len(exp) - 1 and c == exp[e_index + 1]:
                                break
                            count += 1
                    t_index += count
                else:
                    return False
            else:
                t_index += 1
            e_index += 1

    def match(self, exp, text):
        if not exp:
            return True
        if not text:
            return False
        if exp == text:
            return True

        if exp[0] == '^' and exp[-1] == '$':
            return self._parsing_text(exp.replace('^', ''), text)
        elif exp[0] == '^' and not exp[-1] == '$':
            return self._parsing_text(exp.replace('^', ''), text)
        elif not exp[0] == '^' and exp[-1] == '$':
            return self._parsing_text(exp, text[::-1][:len(exp.replace('\\', '')) - 1][::-1])

        start = 0
        for i in range(0, len(text)):
            if text[i] == exp[0 if exp[0] != '\\' else 1] or exp[0] == '.':
                start = i
                break
        return self._parsing_text(exp, text[start:])


if __name__ == '__main__':
    expression, text = input().split('|')
    regex = Regex()
    print(regex.match(expression, text))
