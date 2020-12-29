import pickle
from string import ascii_lowercase, digits
from bs4 import BeautifulSoup, NavigableString
from collections import Counter

# Loading and saving files

def read_txt(path):
    return open(path, 'r', encoding='utf-8').read()

def save_txt(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

def load_pickle(path):
  with open(path, 'rb') as handle:
    return pickle.load(handle)

def save_pickle(variable, path):
    with open(path, 'wb') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Web scraper functions

def exclude_black_list(content, black_list):
    return False if content.lower() in black_list else True

def between(start, end, exclude=[]):
    while start != end:
        if isinstance(start, NavigableString):
            yield start
        elif start.name in exclude:
            start = start.next_element
        start = start.next_element

def format_file_name(title, titles):
    allowed_letters = ascii_lowercase + digits + '_'

    title = title.split('\n')
    title = title[0] if len(title[0]) > 0 else title[1]
    title = title.strip().replace(' ', '_').lower()
    title = ''.join([letter for letter in title if letter in allowed_letters])
    titles.append(title)

    if title in titles:
        title = title + str(titles.count(title))

    return title + '.txt', titles

def format_text(start, end, exclude, num_words):
    text = ' '.join(t for t in between(start, end, exclude))
    text = '\n'.join(text.split("\n")[1:]).strip()
    num_words.append(len(text.split(' ')))
    return text, num_words

def words_summary(num_words):
    print('Number of unique files with fairy tales:', len(num_words))
    print('Total number of words in all fairy tales:', sum(num_words))
    print('Average number of words in a fairy tale: %d' % (sum(num_words)/len(num_words)))
    print('Number of words in the shortest story: %d, in the longest story: %d' % (min(num_words), max(num_words)))

def text_summary(text, exclude_words=[]):
    text = text.replace('\n', ' ').strip().split(' ')
    words_counter = Counter(text).most_common()
    unique_words = len(words_counter) - len(exclude_words)
    total_words = sum([occ for word, occ in words_counter if word not in exclude_words])

    print('Number of unique words:', unique_words)
    print('Total number of words:', total_words)