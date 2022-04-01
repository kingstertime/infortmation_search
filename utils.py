import pymorphy2
import os
import ast

from pandas import DataFrame, read_csv

INDEX_ENTRY_SEPARATOR = ': '
INDEX_FILE_NAME = 'index.txt'
MAX_INDEX = 99


def write_index(run_path: str, index: dict):
    with open('{}/index.txt'.format(run_path), 'w') as file:
        for i, item in enumerate(sorted(index.items())):
            entry = '{}{}{}'.format(item[0], INDEX_ENTRY_SEPARATOR, item[1])
            file.write(entry)
            if i != len(index) - 1:
                file.write('\n')


def read_text(dir_path: str, file_name: str) -> str:
    file_path = '{}/{}'.format(dir_path, file_name)
    print('Read text from file {}...'.format(file_path))
    return open(file_path, 'r').read()


morph = pymorphy2.MorphAnalyzer()


def lemmatize(text: str) -> str:
    return morph.parse(text)[0].normal_form


def pos(word):
    return morph.parse(word)[0].tag.POS


def input_run_path() -> str:
    # 1. Type directory to work with
    run_path = input('Input run path: ')

    # 2. Check if index was built
    if not os.path.isdir(run_path):
        raise FileNotFoundError('{} does not found')
    is_indexed = False
    for file_name in os.listdir(run_path):
        if file_name == INDEX_FILE_NAME:
            is_indexed = True
            break
    if not is_indexed:
        raise FileNotFoundError('index is not built for run {}'.format(run_path))
    return run_path


def extract_doc_id(file_name: str) -> int:
    return int(file_name.split('.')[0])


def write_inverted_index(run_path: str, inverted_index: dict):
    with open('{}/inverted_index.txt'.format(run_path), 'w') as output:
        for i, item in enumerate(sorted(inverted_index.items())):
            entry = '{}{}{}'.format(item[0], INDEX_ENTRY_SEPARATOR, str(item[1]))
            output.write(entry)
            if i != len(inverted_index) - 1:
                output.write('\n')
    print('Inverted index has been saved')


def read_index(run_path: str) -> dict:
    index = dict()
    with open('{}/index.txt'.format(run_path), 'r') as file:
        for line_number, line in enumerate(file):
            entry = line.split(INDEX_ENTRY_SEPARATOR)
            index[entry[0]] = entry[1].replace('\n', '')
    return index


def read_inverted_index(run_path: str) -> dict:
    inverted_index = dict()
    with open('{}/inverted_index.txt'.format(run_path), 'r') as file:
        for line_number, line in enumerate(file):
            entry = line.split(INDEX_ENTRY_SEPARATOR)
            inverted_index[entry[0]] = ast.literal_eval(entry[1])
    return inverted_index


def write_units(dir_path: str, file_name: str, words: list):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    units_file_path = '{}/{}'.format(dir_path, file_name)
    print('Write to file {}...'.format(units_file_path))
    with open(units_file_path, 'w') as output:
        output.write(' '.join(words))


def write_tf_idf(dir_path: str, file_id: int, tf_idf_list: list):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    file_path = '{}/{}.txt'.format(dir_path, file_id)
    print('Save to file {}...'.format(file_path))
    with open(file_path, 'w') as file:
        for tf_idf in tf_idf_list:
            file.write(tf_idf)
            if tf_idf != len(tf_idf_list) - 1:
                file.write('\n')


def save_df_as_csv(csv_file_path: str, df: DataFrame):
    df.to_csv(csv_file_path)
    print('Saved DataFrame to csv file {}'.format(csv_file_path))


def read_idf(run_path: str) -> DataFrame:
    idf_path = '{}/idf.csv'.format(run_path)
    return read_csv(idf_path, index_col=0)


def read_tf_idf(run_path: str) -> DataFrame:
    tf_idf_path = '{}/tf-idf.csv'.format(run_path)
    return read_csv(tf_idf_path, index_col=0)