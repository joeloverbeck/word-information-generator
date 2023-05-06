"""This module provides a comprehensive analysis of a given word, including its meanings, synonyms, antonyms, etymology, and more. The analysis results are saved in an HTML file in the output directory.

Functions:
get_word_info(word)
main()
"""

import argparse
import os
import traceback

from html_writer import write_section_to_file
from nltk_helpers import (
    download_nltk_datasets,
)
from word_analysis import analyze_word


def get_word_info(word):
    """Generates detailed information about the given word and saves it in an HTML file in the output directory.
    Args:
        word (str): The word to analyze.

    Raises:
        ValueError: If the word is empty or None.
    """

    if not word:
        raise ValueError("Word cannot be empty or None")

    download_nltk_datasets()

    try:
        analysis_results = analyze_word(word)

        parts_of_speech_strings = set()
        for pos, transitivity in analysis_results["pos_and_transitivity"]:
            pos_string = pos
            if transitivity:
                pos_string += f" ({transitivity})"

            parts_of_speech_strings.add(pos_string)

        analysis_results["synonyms"].add(word)

        # Create the output directory if it doesn't exist
        output_directory = "output"
        os.makedirs(output_directory, exist_ok=True)

        # Write information to an HTML file
        html_filename = f"{word}_info.html"
        output_filepath = os.path.join(output_directory, html_filename)

        with open(output_filepath, "w", encoding="utf-8") as file:
            file.write(
                f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>Information about {word}</title>\n<link rel='stylesheet' href='styles.css'>\n</head>\n<body>\n"
            )
            file.write(f"<h1>Information about {word}</h1>\n")

            # Write the analysis results to the HTML file using the write_section_to_file function

            write_section_to_file(
                file, f"Meaning of {word}", analysis_results["meanings"]
            )
            write_section_to_file(
                file, f"Part of speech for {word}", parts_of_speech_strings
            )
            write_section_to_file(
                file,
                f"Etymology of {word}",
                [analysis_results["etymology"]]
                if analysis_results["etymology"]
                else [],
            )
            write_section_to_file(
                file,
                f"Synonyms of {word}",
                analysis_results["synonyms"],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Antonyms of {word}",
                analysis_results["antonyms"],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Word frequencies",
                [
                    f"{w}: {freq}"
                    for w, freq in analysis_results["word_frequencies"].items()
                ],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Collocations for {word} and its synonyms",
                [
                    f"{' '.join(bigram)} (Frequency: {freq})"
                    for bigram, freq in analysis_results["collocations"]
                ],
            )
            write_section_to_file(
                file, f"Phrasal verbs of {word}", analysis_results["phrasal_verbs"]
            )
            write_section_to_file(
                file,
                f"Idiomatic expressions with {word}",
                analysis_results["idiomatic_expressions"],
            )
            write_section_to_file(
                file,
                f"Related phrases and expressions with {word}",
                analysis_results["related_phrases_and_expressions"],
            )
            write_section_to_file(
                file,
                f"Semantic field(s) of {word}",
                analysis_results["semantic_fields"],
            )
            write_section_to_file(
                file,
                f"Hyponyms of {word}",
                [synset.split(".")[0] for synset in analysis_results["hyponyms"]],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Hypernyms of {word}",
                [synset.split(".")[0] for synset in analysis_results["hypernyms"]],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Meronyms of {word}",
                [synset.split(".")[0] for synset in analysis_results["meronyms"]],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Domain-specific words related to {word}",
                list(analysis_results["domain_words"]),
            )
            write_section_to_file(
                file,
                f"Alternative words for {word}",
                analysis_results["alternative_words"],
            )
            write_section_to_file(
                file,
                f"Associated nouns with {word}",
                analysis_results["associated_nouns"],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Associated verbs with {word}",
                analysis_results["associated_verbs"],
                use_table=True,
            )
            write_section_to_file(
                file,
                f"Morphological variations of {word}",
                analysis_results["morphological_variations"],
            )

            file.write("</body>\n</html>")
            print(f"Information about {word} has been saved to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


def main():
    """Parses command-line arguments and calls the get_word_info function with the provided word."""

    # Use argparse for handling command-line arguments
    parser = argparse.ArgumentParser(
        description="Get detailed information about a given word."
    )
    parser.add_argument("word", help="The word to analyze.")
    args = parser.parse_args()

    get_word_info(args.word)


if __name__ == "__main__":
    main()
