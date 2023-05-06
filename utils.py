import functools

from nltk.corpus import wordnet as wn
from nltk.metrics.distance import edit_distance

from progress_reporter import progress_wrapper


class WordNotFoundError(Exception):
    pass

@progress_wrapper
def get_closest_words(word, num_suggestions=3):
    words = set(lemma.name() for synset in wn.all_synsets() for lemma in synset.lemmas())
    distances = sorted([(w, edit_distance(word, w, transpositions=True)) for w in words], key=lambda x: x[1])
    closest_words = [word for word, _ in distances[:num_suggestions]]
    return closest_words

def check_word_exists(func):
    @functools.wraps(func)
    def wrapper(word, *args, **kwargs):
        handle_word_not_found(word)
        return func(word, *args, **kwargs)
    return wrapper

def handle_word_not_found(word):
    if not wn.synsets(word):
        closest_words = get_closest_words(word)
        suggestions = ", ".join(closest_words)
        raise WordNotFoundError(f"The word '{word}' was not found in the WordNet database. Did you mean: {suggestions}?")


def replace_underscore_with_space(s):
    return s.replace('_', ' ')

            








    





















