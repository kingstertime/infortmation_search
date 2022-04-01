import os
import nltk
import re

from nltk.tokenize import word_tokenize
from utils import read_text, lemmatize, pos


nltk.download('punkt')


def is_russian(text: str) -> bool:
    return bool(re.match('^[а-яА-Я]+$', text))

def tokenize(text: str) -> set:
    print('Tokenize text...')
    tokens = word_tokenize(text, language='russian')
    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}
    russian_tokens = set([token for token in tokens if ((pos(token) not in functors_pos) & is_russian(token))])
    return russian_tokens


def lemmatize_tokens(tokens: set, dict: dict):
    print('Lemmatize tokens...')
    tokens_set: set[str]
    for token in tokens:
        lemma = lemmatize(token)
        if lemma in dict:
            tokens_set = dict[lemma]
        else:
            tokens_set = set()
        tokens_set.add(token)
        dict[lemma] = tokens_set


def save_tokens(root_path: str, tokens: set):
    tokens_dir_path = '{}/tokens'.format(root_path)
    if not os.path.isdir(tokens_dir_path):
        os.mkdir(tokens_dir_path)
    tokens_file_path = '{}/tokens.txt'.format(tokens_dir_path)
    print('Save tokens to file {}...'.format(tokens_file_path))
    with open(tokens_file_path, 'a') as output:
        output.write('\n'.join(tokens))


def save_lemmas(root_path: str, lemmas: dict):
    lemmas_dir_path = '{}/lemmas'.format(root_path)
    if not os.path.isdir(lemmas_dir_path):
        os.mkdir(lemmas_dir_path)
    lemmas_file_path = '{}/lemmas.txt'.format(lemmas_dir_path)
    print('Save lemmas to file {}...'.format(lemmas_file_path))
    with open(lemmas_file_path, 'a') as output:
        for key, value in lemmas.items():
            output.write('{}: {}\n'.format(key, ' '.join(value)))


if __name__ == '__main__':
    run_path = '../run (01-04-2022)'
    content_run_path = '{}/content'.format(run_path)
    tokens = set()
    lemmas = dict()
    for file_name in sorted(os.listdir(content_run_path)):
        text = read_text(content_run_path, file_name)
        tokens.update(tokenize(text))
        lemmatize_tokens(tokens, lemmas)
        print()
    print(lemmas)
    save_tokens(run_path, tokens)
    save_lemmas(run_path, lemmas)