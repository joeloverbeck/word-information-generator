import os

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import reuters
from nltk.corpus import wordnet as wn
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.util import bigrams

NLTK_DOWNLOAD_FLAG_FILE = "nltk_downloads_complete.flag"


def download_nltk_datasets():
    if not os.path.exists(NLTK_DOWNLOAD_FLAG_FILE):
        nltk.download("wordnet")
        nltk.download("maxent_ne_chunker")
        nltk.download("words")
        nltk.download("stopwords")
        nltk.download("reuters")
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("omw")
        nltk.download("webtext")

        with open(NLTK_DOWNLOAD_FLAG_FILE, "w") as flag_file:
            flag_file.write("Downloads complete.")

    else:
        print("NLTK datasets already downloaded.")


def get_word_frequencies(words_list):
    # Check if words_list contains only strings
    if not all(isinstance(word, str) for word in words_list):
        raise ValueError(
            f"The function 'get_word_frequencies' received a list of words that didn't contain only strings: {words_list}"
        )

    reuters_words = [w.lower() for w in reuters.words() if w.isalnum()]

    # Calculate the frequency distribution for words
    freq_dist = FreqDist(reuters_words)

    # Return the frequencies of the words in words_list
    return {word: freq_dist[word] for word in words_list}


def get_collocations(words_list):
    reuters_words = [w.lower() for w in reuters.words() if w.isalnum()]
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(reuters_words)

    # Apply the word filter only once
    finder.apply_word_filter(lambda w: w not in words_list)

    # Get the top collocations without any filtering
    top_collocations = finder.nbest(bigram_measures.raw_freq, 100)

    # Filter the collocations to keep only those that contain words from words_list
    collocations = [
        bigram
        for bigram in top_collocations
        if any(word in bigram for word in words_list)
    ]

    # Calculate the frequency distribution for bigrams
    freq_dist = FreqDist(bigrams(reuters_words))

    # Return collocations along with their frequencies
    return [(bigram, freq_dist[bigram]) for bigram in collocations]


def get_morphological_variations(word):
    lemmatizer = WordNetLemmatizer()
    morphological_variations = []

    for pos in ["a", "s", "r", "n", "v"]:
        lemma = lemmatizer.lemmatize(word, pos)
        if lemma != word:
            morphological_variations.append(lemma)

    return morphological_variations
