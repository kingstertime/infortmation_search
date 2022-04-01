import os
from collections import OrderedDict

from utils import read_text, extract_doc_id, write_inverted_index, lemmatize as lemmatize_unit, INDEX_ENTRY_SEPARATOR


if __name__ == '__main__':
    run_path = '../run (01-04-2022)'
    units_run_path = '{}/content'.format(run_path)
    lines = read_text(run_path, 'lemmas/lemmas.txt').split('\n')
    lemmas = []
    for line in lines:
        lemmas.append(line.split(INDEX_ENTRY_SEPARATOR)[0])
    inverted_index = dict()
    for file_name in sorted(os.listdir(units_run_path)):
        units = read_text(units_run_path, file_name).split()
        file_id = extract_doc_id(file_name)
        for unit in units:
            lemmatized_unit = lemmatize_unit(unit)
            if lemmatized_unit in lemmas:
                if lemmatized_unit not in inverted_index:
                    inverted_index[lemmatized_unit] = []
                if file_id in inverted_index[lemmatized_unit]:
                    continue
                else:
                    inverted_index[lemmatized_unit].append(file_id)
    inverted_index = OrderedDict(sorted(inverted_index.items()))
    write_inverted_index(run_path, inverted_index)