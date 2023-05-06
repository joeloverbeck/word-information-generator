import argparse
import os
import traceback

from etymology_scraper import get_etymology
from nltk_helpers import (
    download_nltk_datasets,
    get_collocations,
    get_morphological_variations,
    get_word_frequencies,
)
from progress_reporter import progress_wrapper
from semantic_relations import get_semantic_fields, get_semantic_relations
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


def write_section_to_file(f, title, items, use_table=False):
    if items:
        f.write(f"<h2>{title}</h2>\n")
        if use_table:
            f.write("<table>\n<tr>\n")
            for i, item in enumerate(items):
                f.write(f"<td>{item}</td>\n")
                if (i + 1) % 4 == 0:
                    f.write("</tr>\n<tr>\n")
            f.write("</tr>\n</table>\n\n")
        else:
            f.write("<ul>\n")
            for item in items:
                f.write(f"<li>{item}</li>\n")
            f.write("</ul>\n\n")


def get_word_info(word):
    if not word:
        raise ValueError("Word cannot be empty or None")

    download_nltk_datasets()

    try:
        meanings = get_meanings(word)
        synonyms, antonyms = get_synonyms_antonyms(word)
        domain_words = get_domain_words(word)
        associated_nouns, associated_verbs = get_associated_nouns_verbs(word)
        semantic_fields = get_semantic_fields(word)
        hyponyms, hypernyms, meronyms = get_semantic_relations(word)

        # Get word frequencies for the original word and its synonyms
        word_frequencies = get_word_frequencies(synonyms)

        phrasal_verbs = get_phrasal_verbs(word)
        collocations = get_collocations(synonyms)
        morphological_variations = get_morphological_variations(word)

        etymology_result = get_etymology(word)
        alternative_words = get_alternative_words(word)
        idiomatic_expressions = get_idiomatic_expressions(word)
        pos_and_transitivity_results = get_pos_and_transitivity(word)
        related_phrases_and_expressions = get_related_phrases_and_expressions(word)

        parts_of_speech_strings = set()
        for pos, transitivity in pos_and_transitivity_results:
            pos_string = pos
            if transitivity:
                pos_string += f" ({transitivity})"

            parts_of_speech_strings.add(pos_string)

        synonyms.add(word)

        # Create the output directory if it doesn't exist
        output_directory = "output"
        os.makedirs(output_directory, exist_ok=True)

        # Write information to an HTML file
        html_filename = f"{word}_info.html"
        output_filepath = os.path.join(output_directory, html_filename)

        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(
                f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>Information about {word}</title>\n<link rel='stylesheet' href='styles.css'>\n</head>\n<body>\n"
            )
            f.write(f"<h1>Information about {word}</h1>\n")

            write_section_to_file(f, f"Meaning of {word}", meanings)
            write_section_to_file(
                f, f"Part of speech for {word}", parts_of_speech_strings
            )
            write_section_to_file(
                f,
                f"Etymology of {word}",
                [etymology_result] if etymology_result else [],
            )
            write_section_to_file(f, f"Synonyms of {word}", synonyms, use_table=True)
            write_section_to_file(f, f"Antonyms of {word}", antonyms, use_table=True)
            write_section_to_file(
                f,
                f"Word frequencies",
                [f"{w}: {freq}" for w, freq in word_frequencies.items()],
                use_table=True,
            )
            write_section_to_file(
                f,
                f"Collocations for {word} and its synonyms",
                [
                    f"{' '.join(bigram)} (Frequency: {freq})"
                    for bigram, freq in collocations
                ],
            )
            write_section_to_file(f, f"Phrasal verbs of {word}", phrasal_verbs)
            write_section_to_file(
                f, f"Idiomatic expressions with {word}", idiomatic_expressions
            )
            write_section_to_file(
                f,
                f"Related phrases and expressions with {word}",
                related_phrases_and_expressions,
            )
            write_section_to_file(f, f"Semantic field(s) of {word}", semantic_fields)
            write_section_to_file(
                f,
                f"Hyponyms of {word}",
                [synset.split(".")[0] for synset in hyponyms],
                use_table=True,
            )
            write_section_to_file(
                f,
                f"Hypernyms of {word}",
                [synset.split(".")[0] for synset in hypernyms],
                use_table=True,
            )
            write_section_to_file(
                f,
                f"Meronyms of {word}",
                [synset.split(".")[0] for synset in meronyms],
                use_table=True,
            )
            write_section_to_file(
                f,
                f"Domain-specific words related to {word}",
                [word for word in domain_words],
            )
            write_section_to_file(f, f"Alternative words for {word}", alternative_words)
            write_section_to_file(
                f, f"Associated nouns with {word}", associated_nouns, use_table=True
            )
            write_section_to_file(
                f, f"Associated verbs with {word}", associated_verbs, use_table=True
            )
            write_section_to_file(
                f, f"Morphological variations of {word}", morphological_variations
            )

            f.write("</body>\n</html>")
            print(f"Information about {word} has been saved to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


def main():
    # Use argparse for handling command-line arguments
    parser = argparse.ArgumentParser(
        description="Get detailed information about a given word."
    )
    parser.add_argument("word", help="The word to analyze.")
    args = parser.parse_args()

    get_word_info(args.word)


if __name__ == "__main__":
    main()
