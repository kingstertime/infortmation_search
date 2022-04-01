from datetime import datetime
import os
import validators
import urllib.request
from bs4 import BeautifulSoup
from print_dict import format_dict
from utils import write_index

READ_URL_TIMEOUT = 10
LIMIT_NODES_NUMBER = 100
LIMIT_PAGE_WORDS_COUNT = 1000
SUPPORT_ENCODINGS = ['utf-8', 'windows-1251']


def input_base_url() -> str:
    base_url = input('Enter base page url: ')
    base_url_validation_result = validators.url(base_url)
    assert base_url_validation_result, 'Invalid url'
    return base_url


def load_page_content(url: str) -> str:
    page_content = None
    try:
        page = urllib.request.urlopen(url, timeout=READ_URL_TIMEOUT).read()
        page_content = decode_page_content(page)
    except Exception as e:
        pass
    return page_content


def decode_page_content(content: bytes) -> str:
    decoded_content = None
    encoding_index = 0
    while decoded_content is None and encoding_index < len(SUPPORT_ENCODINGS):
        encoding = SUPPORT_ENCODINGS[encoding_index]
        try:
            decoded_content = content.decode(encoding)
        except UnicodeDecodeError as e:
            print('Unable to decode content using {}'.format(encoding))
        encoding_index += 1
    return decoded_content


def extract_links(soup: BeautifulSoup) -> list:
    links = []
    for link in soup.findAll('a'):
        url = link.get('href')
        if url is None:
            continue
        url_validation_result = validators.url(url)
        if not url_validation_result:
            continue
        links.append(url)
    return links


def extract_plain_text(soup: BeautifulSoup) -> str:
    return soup.get_text()


def extract_words(soup: BeautifulSoup) -> list:
    return ' '.join(soup.stripped_strings).replace('\n', ' ').strip().split(' ')


def save_page_content(path: str, content: str):
    with open(path, 'w') as output:
        output.write(content)


if __name__ == '__main__':
    print('Pages number limit: {}'.format(LIMIT_NODES_NUMBER))
    print('Pages content words count limit: {}'.format(LIMIT_PAGE_WORDS_COUNT))

    now = datetime.now()
    run_dir_path = './run ({})'.format(now.strftime('%d-%m-%Y'))
    print('All related to run files will be saved to {}'.format(run_dir_path))
    os.mkdir(run_dir_path)
    content_run_dir_path = '{}/content'.format(run_dir_path)
    os.mkdir(content_run_dir_path)

    base_url = input_base_url()
    scanned_nodes = []
    url_tree_nodes = [base_url]
    index_dict = dict()
    index = 0
    while index < LIMIT_NODES_NUMBER and len(url_tree_nodes) > 0:
        node_url = url_tree_nodes.pop(0)
        if node_url in scanned_nodes:
            print('Node {} is already scanned'.format(node_url))
            continue
        print('Node {} is scanning now...'.format(node_url))
        node_content = load_page_content(node_url)
        if node_content is None:
            continue
        soup = BeautifulSoup(node_content, features='html.parser')
        url_tree_nodes.extend(extract_links(soup))
        node_content_plain = extract_plain_text(soup)
        node_content_words = extract_words(soup)
        node_content_words_number = len(node_content_words)
        print('Node {} contains {} words'.format(node_url, node_content_words_number))
        if node_content_words_number >= LIMIT_PAGE_WORDS_COUNT:
            node_file_path = '{}/{}.txt'.format(content_run_dir_path, index)
            save_page_content(node_file_path, ' '.join(node_content_words))
            index_dict[index] = node_url
            print('Node {} is added to index {}'.format(node_url, index))
            index += 1
        scanned_nodes.append(node_url)
    assert index == LIMIT_NODES_NUMBER, 'Url tree contains less than 100 nodes'
    write_index(run_dir_path, index_dict)
    print('Built index:\n{}'.format(format_dict(index_dict)))