import sys


class Application:
    def __init__(self, import_from, export_to):
        self.cards = dict()
        self.mistakes = dict()
        self.log = list()

        self.export_to = export_to
        if import_from:
            self._import(import_from)

    def _add(self):
        self.__print(f'The card:')
        while True:
            term = input()
            if term in self.cards.keys():
                self.__print(f'The term "{term}" already exists. Try again:')
            else:
                break
        self.__print(f'The definition of the card:')
        while True:
            definition = input()
            if definition in self.cards.values():
                self.__print(f'The definition "{definition}" already exists. Try again:')
            else:
                break
        self.cards[term] = definition
        self.mistakes[term] = 0
        self.__print(f'The pair ("{term}":"{definition}") has been added.')

    def _remove(self):
        self.__print('Which card?')
        term = input()
        if term in self.cards.keys():
            self.cards.pop(term)
            self.__print('The card has been removed.')
        else:
            self.__print(f'Can\'t remove "{term}": there is no such card.')

    def _import(self, file_name):
        try:
            self.cards = dict()
            self.mistakes = dict()
            for line in open(file_name, 'r', encoding='utf-8').readlines():
                t, d, m = line.split('$$')
                self.cards[t] = d
                self.mistakes[t] = int(m.replace('\n', ''))
            self.__print(f'{len(self.cards)} cards have been loaded.')
        except FileNotFoundError:
            self.__print('File not found.')

    def _export(self, file_name):
        try:
            open(file_name, 'w', encoding='utf-8') \
                .write('\n'.join(f'{t}$${d}$${self.mistakes[t]}' for t, d in self.cards.items()))
            self.__print(f'{len(self.cards)} cards have been saved.')
        except FileNotFoundError as e:
            self.__print(e)

    def _ask(self):
        self.__print('How many times to ask?')
        limit = int(input())
        count = 0
        while True:
            for term, definition in self.cards.items():
                self.__print(f'Print the definition of "{term}":')
                answer = input()
                if answer != definition:
                    self.mistakes[term] += 1
                    if answer in self.cards.values():
                        self.__print(f'Wrong. The right answer is "{definition}",'
                              f' but your definition is correct for "{self._get_term_by_definition(answer)}".')
                    else:
                        self.__print(f'Wrong. The right answer is "{definition}".')
                else:
                    self.__print('Correct!')

                count += 1
                if count == limit:
                    return

    def _get_term_by_definition(self, definition):
        for t, d in self.cards.items():
            if definition == d:
                return t

    def _log(self):
        try:
            self.__print('File name:')
            open(input(), 'w', encoding='utf-8').write('\n'.join(line for line in self.log))
            self.__print('The log has been saved.')
        except FileNotFoundError as e:
            self.__print(e)

    def _hardest_card(self):
        if sum(self.mistakes.values()) > 0:
            max_value = max(self.mistakes.values())
            hardest_card = next(t for t, d in self.mistakes.items() if d == max_value)
            self.__print(f'The hardest card is "{hardest_card}". You have {max_value} errors answering it.')
        else:
            self.__print('There are no cards with errors.')

    def _reset_stats(self):
        self.mistakes = self.mistakes.fromkeys(self.mistakes, 0)
        self.__print('Card statistics have been reset.')
    
    def __print(self, text):
        self.log.append(text)
        print(text)

    def _menu(self):
        while True:
            self.__print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
            choice = input()
            if choice == 'add':
                self._add()
            elif choice == 'remove':
                self._remove()
            elif choice == 'import':
                self.__print('File name:')
                self._import(input())
            elif choice == 'export':
                self.__print('File name:')
                self._export(input())
            elif choice == 'ask':
                self._ask()
            elif choice == 'log':
                self._log()
            elif choice == 'hardest card':
                self._hardest_card()
            elif choice == 'reset stats':
                self._reset_stats()
            elif choice == 'exit':
                if export_to:
                    self._export(self.export_to)
                self.__print('Bye bye!')
                sys.exit(0)

    def run(self):
        self._menu()


if __name__ == '__main__':
    import_from = None
    export_to = None
    for arg in sys.argv:
        try:
            name, value = arg.split('=')
            if name == '--import_from':
                import_from = value
            elif name == '--export_to':
                export_to = value
        except ValueError:
            pass
    Application(import_from, export_to).run()
