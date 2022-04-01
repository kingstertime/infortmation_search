import os
from utils import read_text, extract_doc_id, save_df_as_csv, \
    read_inverted_index, read_index
from pandas import DataFrame
from numpy import zeros
from math import log10


def get_lemmas(run_path: str) -> list:
    return list(sorted(read_inverted_index(run_path).keys()))


def get_docs_number(run_path: str) -> int:
    return len(read_index(run_path).keys())


if __name__ == '__main__':
    run_path = '../run (01-04-2022)'
    lemmas = get_lemmas(run_path)
    lemmas_number = len(lemmas)
    docs_number = get_docs_number(run_path)
    units_run_path = '{}/lemmas/list'.format(run_path)

    # 1. Calculate TF
    # - For each document
    # - For each unit calculate appearance frequency
    # - Save it as table (unit, docId) = tf
    tf = DataFrame(
        zeros((lemmas_number, docs_number)),
        index=lemmas,
        columns=list(range(0, docs_number))
    )
    for doc_name in sorted(os.listdir(units_run_path)):
        units = read_text(units_run_path, doc_name).split()
        doc_id = extract_doc_id(doc_name)
        # Calculate units appearance number
        for unit in units:
            if unit in tf.index:
                tf.at[unit, doc_id] += 1
            # else:
            #     raise Exception('Unknown unit {}'.format(unit))
        # Calculate units appearance frequency
        units_number = len(units)
        print('Doc {} contains {} units'.format(doc_id, units_number))
        # ! Sum of all terms frequencies in doc may not be equal to 1
        # - Because frequency is round
        if units_number > 0:
            tf[doc_id] = tf[doc_id].map(lambda counter: round(counter / units_number, 5))
        else:
            continue
    save_df_as_csv('{}/tf.csv'.format(run_path), tf)

    # 2. Calculate IDF
    # - For each unit
    # - For each document calculate unit appearance frequency
    # - Save it as table (unit, docId) = tf
    inverted_index = read_inverted_index(run_path)
    idf = {unit: round(log10(docs_number / len(doc_ids)), 5) for unit, doc_ids in inverted_index.items()}
    idf = DataFrame.from_dict(idf, orient='index', columns=['idf'])
    save_df_as_csv('{}/idf.csv'.format(run_path), idf)

    # 3. Calculate TF-IDF
    tf_idf = tf.copy()
    for unit in idf.index:
        unit_idf = idf.at[unit, 'idf']
        tf_idf.loc[unit] = tf_idf.loc[unit].apply(lambda unit_tf: round(unit_tf * unit_idf, 3))
    save_df_as_csv('{}/tf-idf.csv'.format(run_path), tf_idf)