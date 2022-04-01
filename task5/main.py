import re
import numpy as np
from print_dict import format_dict
from utils import lemmatize, read_idf, read_tf_idf, read_index
from pandas import DataFrame, Series


def input_search_query() -> str:
    return input('Type search query:')


def split_search_query(query: str) -> list:
    return re.sub(r'[^\w\s]', '', query).split(' ')


def lemmatize_terms(terms: list) -> list:
    return [lemmatize(term) for term in terms]


def calculate_terms_tf(terms: list) -> DataFrame:
    tf_dict = dict()
    for term in terms:
        if term in tf_dict:
            tf_dict[term] = tf_dict[term] + 1
        else:
            tf_dict[term] = 1
    terms_number = len(terms)
    tf_dict = {term: round(counter / terms_number, 5) for term, counter in tf_dict.items()}
    tf = DataFrame.from_dict(tf_dict, orient='index', columns=['tf'])
    return tf


def calculate_terms_tf_idf(tf: DataFrame, idf: DataFrame) -> DataFrame:
    terms_tf_idf = idf.copy()
    terms_tf_idf.columns = ['tf-idf']
    for term, row in idf.iterrows():
        if term in tf.index:
            terms_tf_idf.at[term, 'tf-idf'] = terms_tf_idf.at[term, 'tf-idf'] * row['idf']
        else:
            terms_tf_idf.at[term, 'tf-idf'] = 0
    return terms_tf_idf


def calculate_doc_vectors_length(tf_idf: DataFrame) -> DataFrame:
    doc_vectors_length = DataFrame(np.zeros((1, len(tf_idf.columns))), columns=tf_idf.columns)
    for doc_id in tf_idf:
        terms_tf_ids = tf_idf[doc_id]
        for key, value in terms_tf_ids.items():
            if value != 0:
                doc_vectors_length.at[0, doc_id] += (value * value)
        doc_vectors_length.at[0, doc_id] = np.sqrt(doc_vectors_length.at[0, doc_id])
    return doc_vectors_length


def calculate_vector_length(vector: Series) -> float:
    vector_length = 0
    for index, value in vector.items():
        if value != 0:
            vector_length += (value * value)
    return np.sqrt(vector_length)


def calculate_doc_vectors_similarity(
        query_lemmas_tf_idf: DataFrame,
        tf_idf: DataFrame
) -> DataFrame:
    query_vector_length = calculate_vector_length(query_lemmas_tf_idf['tf-idf'])
    doc_vectors_similarity = DataFrame(np.zeros((1, len(tf_idf.columns))), columns=tf_idf.columns)
    for doc_id in tf_idf:
        terms_tf_ids = tf_idf[doc_id]
        for key, all_term_tf_idf in terms_tf_ids.items():
            query_term_tf_idf = query_lemmas_tf_idf.at[key, 'tf-idf']
            if all_term_tf_idf != 0 and query_term_tf_idf != 0:
                doc_vectors_similarity.at[0, doc_id] += (all_term_tf_idf * query_term_tf_idf)
        if doc_vectors_similarity.at[0, doc_id] != 0:
            doc_vectors_similarity.at[0, doc_id] /= (doc_vectors_length.at[0, doc_id] * query_vector_length)
    return doc_vectors_similarity


# prepare data
run_path = '../run (01-04-2022)'
idf = read_idf(run_path)
tf_idf = read_tf_idf(run_path)
doc_vectors_length = calculate_doc_vectors_length(tf_idf)

if __name__ == '__main__':
    # 1. input query
    # 1.1. extract & lemmatize terms
    query = input_search_query()
    query_terms = split_search_query(query)
    query_lemmas = lemmatize_terms(query_terms)
    print('Lemmatized query: {}'.format(query_lemmas))

    # 2. weight query
    # 2.1. calculate tf for each lemma
    print('Weight query vector...')
    query_lemmas_tf = calculate_terms_tf(query_lemmas)
    # 2.2. calculate tf-idf for each lemma using collection idf
    query_lemmas_tf_idf = calculate_terms_tf_idf(query_lemmas_tf, idf)

    # 3. for each collection vector (tf-idf of lemma) calculate cosine similarity
    print('Calculate query vector - docs vector cosine similarity...')
    docs_similarity = calculate_doc_vectors_similarity(query_lemmas_tf_idf, tf_idf)

    # 4. print docs urls ordered by cosine similarity (descendant)
    docs_similarity = docs_similarity.loc[0].to_dict()
    docs_similarity = dict(sorted(docs_similarity.items(), key=lambda kv: kv[1], reverse=True))
    index = read_index(run_path)
    new_dict = dict()
    for key, value in docs_similarity.items():
        new_dict[index[key]] = value
    print('Search result: {}'.format(format_dict(new_dict)))