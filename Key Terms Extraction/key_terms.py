import string
import xml.etree.cElementTree as etree

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import pos_tag, tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

'''
Structure xml:
<?xml version='1.0' encoding='UTF8'?>
<data>
  <corpus>
    <news>
      <value name="head">Some title</value>
      <value name="text">Some text</value>
    </news>
  </corpus>
</data>
'''

xml = 'news.xml'  # path
root = etree.parse(xml).getroot()

result = dict()
dataset = dict()
lemmatizer = WordNetLemmatizer()
excluded_characters = stopwords.words('english') + list(string.punctuation) + ['ha', 'wa', 'u', 'a']
for head, text in zip(root.iterfind('./corpus/news/value[@name="head"]'),
                      root.iterfind('./corpus/news/value[@name="text"]')):
    tokens = tokenize.word_tokenize(text.text.lower())
    lematizer_word_list = map(lambda x: lemmatizer.lemmatize(x), tokens)
    filtered_word_list = tuple(filter(lambda x: x not in excluded_characters, lematizer_word_list))
    dataset[head.text] = ' '.join(filter(lambda x: pos_tag([x])[0][1] == 'NN', filtered_word_list))

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(list(dataset.values()))
terms = vectorizer.get_feature_names()

for n, (head, _) in enumerate(dataset.items()):
    df = pd.DataFrame(tfidf_matrix[n].T.todense(), index=terms, columns=["score"])
    data_for_sort = {'word': list(df['score'].to_dict().keys()), 'score': list(df['score'].to_dict().values())}
    df = pd.DataFrame(data_for_sort, index=terms, columns=["word", "score"])
    df = df.sort_values(by=["score", "word"], ascending=False)
    result[f'{head}:'] = list(df.to_dict()['word'].keys())[:5]

for key, value in result.items():
    print(key)
    for e in value:
        print(e, end=' ')
    print('\n')

