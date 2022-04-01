from utils import read_index, read_inverted_index, lemmatize, MAX_INDEX
from enum import Enum
import re

BOOLEAN_SEARCH_REGEX = re.compile('(\!?)([0-9a-zA-Zа-яА-Я_]+)(\s([\&|\|])\s(\!?)([0-9a-zA-Zа-яА-Я_]+))*')
BOOLEAN_SEARCH_OPERATORS_REGEX = re.compile('[\!|\&|\|]')


class BooleanOperator(Enum):
    NOT = '!'
    AND = '&'
    OR = '|'


def convert_char_to_boolean_operator(char: str) -> BooleanOperator:
    if char == BooleanOperator.NOT.value:
        return BooleanOperator.NOT
    elif char == BooleanOperator.AND.value:
        return BooleanOperator.AND
    elif char == BooleanOperator.OR.value:
        return BooleanOperator.OR
    else:
        raise Exception('Unknown operator {}'.format(char))


def is_boolean_search_query_valid(query: str) -> bool:
    return bool(BOOLEAN_SEARCH_REGEX.fullmatch(query))


def input_boolean_search_query() -> str:
    print('Boolean search:\n'
          '- !, &, | operation are supported\n'
          '- parentheses are not supported\n'
          '- separate input with 1 whitespace (except !)')
    query = input('Input query: ')
    if is_boolean_search_query_valid(query):
        return query
    else:
        raise Exception('Invalid boolean search query \'{}\''.format(query))


def parse_boolean_search_query(query: str) -> tuple:
    args = list(map(
        lambda arg: lemmatize(arg),
        re.sub(BOOLEAN_SEARCH_OPERATORS_REGEX, '', query).split('  ')
    ))
    operators = list(map(
        lambda x: convert_char_to_boolean_operator(x),
        re.findall(BOOLEAN_SEARCH_OPERATORS_REGEX, query)
    ))
    return args, operators


def generate_available_indexes() -> set:
    return set(range(0, MAX_INDEX + 1))


if __name__ == '__main__':
    # load index
    run_path = '../run (01-04-2022)'
    index = read_index(run_path)

    # load inverted index
    inverted_index = read_inverted_index(run_path)

    # parse search query
    # - lammatize input strings
    # - three operations supported: & | !
    query = input_boolean_search_query()
    query_args, query_operators = parse_boolean_search_query(query)

    # treat args as sets of doc ids
    for i, query_arg in enumerate(query_args):
        query_args[i] = set(inverted_index.get(query_arg, set()))

    # do boolean search:
    # - look for input lemmas in inverted index
    # - convert search results to sets
    # - apply boolean operations to sets
    boolean_search_result = set()

    # apply inversion
    query_arg_i = 0
    for query_operator in query_operators:
        if query_operator == BooleanOperator.NOT:
            query_args[query_arg_i] = generate_available_indexes().difference(query_args[query_arg_i])
            query_operators.remove(query_operator)
        elif query_operator == BooleanOperator.AND or query_operator == BooleanOperator.OR:
            query_arg_i += 1

    # apply remaining operators
    boolean_search_result = query_args.pop(0)
    while len(query_operators) > 0:
        query_operator = query_operators.pop(0)
        if query_operator == BooleanOperator.AND:
            query_arg_second = query_args.pop(0)
            boolean_search_result = boolean_search_result.intersection(query_arg_second)
        elif query_operator == BooleanOperator.OR:
            query_arg_second = query_args.pop(0)
            boolean_search_result = boolean_search_result.union(query_arg_second)

    # print doc ids
    print('Boolean search result for query \'{}\':\n{}'.format(query, boolean_search_result))