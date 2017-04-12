import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def read_poem(path, remove_stop_words=False, keep_punct=False):
    """
    read all poems the given path and return an array of the verses
    :param keep_punct: set to True to keep punctuation in the list of words
    :param path: path to the root dir of the poems
    :param remove_stop_words: set to True to remove all stopwords, default False
    :return: array of all verses
    """
    verses = []
    for poet in os.listdir(path):
        poet_path = path + poet + '/'
        for poem in os.listdir(poet_path):
            poem_path = poet_path + poem
            with open(poem_path, 'r') as f:
                poem_in_verses = f.readlines()
                poem_in_verses = [v.lower() for v in poem_in_verses if not re.search('^\s*$', v)]
                poem_in_verses = [word_tokenize(v) for v in poem_in_verses]

                if remove_stop_words:
                    stops = set(stopwords.words('english'))
                    poem_in_verses = [[w for w in v if w not in stops] for v in poem_in_verses]

                if not keep_punct:
                    poem_in_verses = [[w for w in v if re.search('\w+', w)] for v in poem_in_verses]

                verses += poem_in_verses

    return verses
