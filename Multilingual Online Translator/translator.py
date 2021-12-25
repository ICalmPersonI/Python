import sys

import requests
from bs4 import BeautifulSoup
import re


def make_first_letter_uppercase(word):
    return str(word[0]).upper() + word[1:]


class Application:
    def __init__(self, from_language, into_language, word):
        self._languages = ['all', 'arabic', 'german', 'english', 'spanish',
                           'french', 'hebrew', 'japanese', 'dutch',
                           'polish', 'portuguese', 'romanian',
                           'russian', 'turkish']

        self._from = from_language if self._languages.__contains__(from_language) else None
        self._into = into_language if self._languages.__contains__(into_language) else None
        self._word = word
        self._page = None

        if self._from is None:
            print(f"Sorry, the program doesn't support {from_language}")
            sys.exit(0)
        if self._into is None:
            print(f"Sorry, the program doesn't support {into_language}")
            sys.exit(0)

    def _create_URL(self, from_language, into_language):
        return f'https://context.reverso.net/translation/{from_language}-{into_language}/{self._word}'

    def _connect(self, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(url, headers=headers)
        if page.status_code == 404:
            print(f'Sorry, unable to find {self._word}')
            return False

        if page.status_code == 200:
            self._page = page
            return True
        else:
            print('Something wrong with your internet connection')
            return False

    def _translate(self):
        translation_result = list()
        soup = BeautifulSoup(self._page.content, 'html.parser')

        translation_result.append(f'\n{make_first_letter_uppercase(self._into)} Translations:')
        translation_result.append(
            '\n'.join(word for word in soup.find('div', {'id': 'translations-content'}).text.split()))
        translation_result.append(f'\n{make_first_letter_uppercase(self._into)} Examples:')

        examples = soup.find('div', {'id': 'wrapper'}) \
            .find('section', {'id': 'examples-content'}) \
            .find_all('div', {'class': 'example'})

        for example in examples:
            translation_result.append(
                ' '.join(e for e in example.find('div', {'class': re.compile('src.*')}).text.split()))
            translation_result.append(
                ' '.join(e for e in example.find('div', {'class': re.compile('trg.*')}).text.split()))
            translation_result.append('')

        self._save_to_file(translation_result)
        print('\n'.join(line for line in translation_result))

    def _translate_into_all(self):
        translation_result = list()
        for language in self._languages[1:]:
            if language == self._from:
                continue
            if self._connect(self._create_URL(self._from, language)):
                soup = BeautifulSoup(self._page.content, 'html.parser')

                translation_result.append(f'\n{make_first_letter_uppercase(language)} Translation:')
                translation_result.append(soup.find('div', {'id': 'translations-content'}).text.split()[1])
                translation_result.append(f'\n{make_first_letter_uppercase(language)} Examples:')

                example = soup.find('div', {'id': 'wrapper'}) \
                    .find('section', {'id': 'examples-content'}) \
                    .find('div', {'class': 'example'})

                translation_result.append(
                    ' '.join(e for e in example.find('div', {'class': re.compile('src.*')}).text.split()))
                translation_result.append(
                    ' '.join(e for e in example.find('div', {'class': re.compile('trg.*')}).text.split()))
                translation_result.append('')
            else:
                sys.exit(0)

        self._save_to_file(translation_result)
        print('\n'.join(line for line in translation_result))

    def _save_to_file(self, text):
        with open(f'{self._word}.txt', 'w') as f:
            for line in text:
                f.write(f'{line}\n')
        f.close()

    def run(self):
        if self._into == 'all':
            self._translate_into_all()
        else:
            if self._connect(self._create_URL(self._from, self._into)):
                self._translate()


if __name__ == "__main__":
    args = sys.argv
    Application(args[-3], args[-2], args[-1]).run()
