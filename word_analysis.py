"""This module provides the means to analyze plenty of useful information about a given word.

Functions:
analyze_word(word)


"""

from progress_reporter import progress_wrapper
from semantic_relations import get_semantic_fields, get_semantic_relations
from etymology_scraper import get_etymology
from wordnet_utils import (
    get_alternative_words,
    get_associated_nouns_verbs,
    get_domain_words,
    get_idiomatic_expressions,
    get_meanings,
    get_phrasal_verbs,
    get_pos_and_transitivity,
    get_related_phrases_and_expressions,
    get_synonyms_antonyms,
)
from nltk_helpers import (
    get_collocations,
    get_morphological_variations,
    get_word_frequencies,
)


def analyze_word(word):
    """Delegates analyzing many aspects of the passed word, and returns the analyses as a dictionary.
    Args:
        word (str): The word to analyze

    """
    analysis_results = {}

    analysis_results["meanings"] = get_meanings(word)
    analysis_results["synonyms"], analysis_results["antonyms"] = get_synonyms_antonyms(
        word
    )
    analysis_results["domain_words"] = get_domain_words(word)
    (
        analysis_results["associated_nouns"],
        analysis_results["associated_verbs"],
    ) = get_associated_nouns_verbs(word)
    analysis_results["semantic_fields"] = get_semantic_fields(word)
    (
        analysis_results["hyponyms"],
        analysis_results["hypernyms"],
        analysis_results["meronyms"],
    ) = get_semantic_relations(word)

    # Get word frequencies for the original word and its synonyms
    analysis_results["word_frequencies"] = get_word_frequencies(
        analysis_results["synonyms"]
    )

    analysis_results["phrasal_verbs"] = get_phrasal_verbs(word)
    analysis_results["collocations"] = get_collocations(analysis_results["synonyms"])
    analysis_results["morphological_variations"] = get_morphological_variations(word)

    analysis_results["etymology"] = get_etymology(word)
    analysis_results["alternative_words"] = get_alternative_words(word)
    analysis_results["idiomatic_expressions"] = get_idiomatic_expressions(word)
    analysis_results["pos_and_transitivity"] = get_pos_and_transitivity(word)
    analysis_results[
        "related_phrases_and_expressions"
    ] = get_related_phrases_and_expressions(word)

    return analysis_results
