import os
from utils import read_text, read_inverted_index, read_index, \
    INDEX_FILE_NAME, lemmatize, write_units, extract_doc_id, write_tf_idf
from task2.main import tokenize
from math import log10


def lemmatize_tokens(tokens: list) -> list:
    print('Lemmatize tokens...')
    lemmas = []
    for token in tokens:
        lemmas.append(lemmatize(token))
    return lemmas


def get_docs_number(run_path: str) -> int:
    return len(read_index(run_path).keys())


def write_tokens_and_lemmas_lists():
    run_path = '../run (01-04-2022)'
    content_run_path = '{}/content'.format(run_path)
    for file_name in sorted(os.listdir(content_run_path)):
        if file_name == INDEX_FILE_NAME:
            continue
        text = read_text(content_run_path, file_name)
        tokens = tokenize(text)
        lemmas = lemmatize_tokens(tokens)
        write_units('{}/tokens/list'.format(run_path), file_name, tokens)
        write_units('{}/lemmas/list'.format(run_path), file_name, lemmas)
        print()


def calc_lemmas_tf_ids():
    run_path = '../run (01-04-2022)'
    docs_number = get_docs_number(run_path)
    units_run_path = '{}/lemmas/list'.format(run_path)

    inverted_index = read_inverted_index(run_path)
    idfs = {unit: round(log10(docs_number / len(doc_ids)), 5) for unit, doc_ids in inverted_index.items()}

    for doc_name in sorted(os.listdir(units_run_path)):
        tf_idf_list = []
        counts = dict()
        units = read_text(units_run_path, doc_name).split()
        units_number = len(units)
        for unit in units:
            if unit in counts.keys():
                counts[unit] += 1
            else:
                counts[unit] = 1
        for unit, count in counts.items():
            if unit in idfs.keys():
                tf = round(count / units_number, 5)
                idf = idfs[unit]
                tf_idf = round(tf * idf, 3)
                tf_idf_list.append("{} {} {}".format(unit, idf, tf_idf))

        write_tf_idf('{}/lemmas/tf_idf'.format(run_path), extract_doc_id(doc_name), tf_idf_list)


def calc_tokens_tf_ids():
    run_path = '../run (01-04-2022)'
    docs_number = get_docs_number(run_path)
    units_run_path = '{}/tokens/list'.format(run_path)

    count_of_files_in_which_exists = dict()
    for doc_name in sorted(os.listdir(units_run_path)):
        units = read_text(units_run_path, doc_name).split()
        for unit in units:
            if unit in count_of_files_in_which_exists.keys():
                count_of_files_in_which_exists[unit] += 1
            else:
                count_of_files_in_which_exists[unit] = 1

    for doc_name in sorted(os.listdir(units_run_path)):
        tf_idf_list = []
        counts = dict()
        units = read_text(units_run_path, doc_name).split()
        units_number = len(units)
        for unit in units:
            if unit in counts.keys():
                counts[unit] += 1
            else:
                counts[unit] = 1
        for unit, count in counts.items():
            if unit in count_of_files_in_which_exists.keys():
                tf = round(count / units_number, 5)
                idf = round(log10(docs_number / count_of_files_in_which_exists[unit]), 5)
                tf_idf = round(tf * idf, 3)
                tf_idf_list.append("{} {} {}".format(unit, idf, tf_idf))

        write_tf_idf('{}/tokens/tf_idf'.format(run_path), extract_doc_id(doc_name), tf_idf_list)


if __name__ == '__main__':
    write_tokens_and_lemmas_lists()

    calc_tokens_tf_ids()

    calc_lemmas_tf_ids()