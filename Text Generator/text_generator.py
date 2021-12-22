import random
import re

from nltk import trigrams, regexp_tokenize
from collections import Counter


class Application:
    def __init__(self):
        self._trigrams = None
        self._markov_chain_model = dict()
        self._punctuation_marks = re.compile('[.!?]')

    def _assembling_trigrams(self, file_name):
        tokens = regexp_tokenize(open(file_name, 'r', encoding="utf-8").read(), r"[^\s]+")
        self._trigrams = list(trigrams(tokens))

    def _create_MCM(self):
        for t1, t2, t3 in self._trigrams:
            head = f'{t1} {t2}'
            self._markov_chain_model.setdefault(head, []).append(t3)
        for t in self._markov_chain_model:
            self._markov_chain_model[t] = Counter(self._markov_chain_model[t])

    def _generate_sentence(self):
        while True:
            head = random.choice(list(self._markov_chain_model.keys()))
            if str(head)[0].isupper() and not re.search(self._punctuation_marks, str(head)):
                sentence = head.split()
                break

        while True:
            word = random.choices(list(self._markov_chain_model[head].keys()),
                                  weights=list(self._markov_chain_model[head].values()))[0]
            sentence.append(word)
            head = ' '.join(sentence[-2:])

            if len(sentence) > 4 and re.search(self._punctuation_marks, word):
                break

        return " ".join(elem for elem in sentence)

    def run(self):
        print("Enter the path to the corpus:")
        self._assembling_trigrams(input())
        self._create_MCM()
        print(str("\n".join(self._generate_sentence() for _ in range(0, 10))))


if __name__ == "__main__":
    Application().run()
