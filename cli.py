"""This module provides a comprehensive analysis of a given word, including its meanings, synonyms, antonyms, etymology, and more. The analysis results are saved in an HTML file in the output directory.

Functions:
get_word_info(word)
main()
"""

import argparse
import os
import logging
import webbrowser

from jinja2 import Environment, FileSystemLoader

from nltk_helpers import (
    download_nltk_datasets,
)
from word_analysis import analyze_word, WordAnalysisError


def save_html_to_file(word, html_content):
    """Saves to a file the html content provided. A file gets created inside the 'output' folder
    of the working directory.
    Args:
        word (str): The word to analyze
        html_content (str): The markup in HTML that will get saved to a file

    """

    # Create the output directory if it doesn't exist
    output_directory = "output"
    os.makedirs(output_directory, exist_ok=True)

    # Save the generated HTML content to the output file
    html_filename = f"{word}_info.html"
    output_filepath = os.path.join(output_directory, html_filename)

    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Information about {word} has been saved to {output_filepath}")

    # Open the file in the default web browser
    webbrowser.open("file://" + os.path.realpath(output_filepath))


def prepare_html_content(word, analysis_results):
    """Given a word and the useful information already gathered regarding
    that word, this function prepares the HTML content that will eventually
    get saved to a file, then returns the HTML content.
    Args:
        word (str): The word to analyze
        analysis_results (dict): A large dictionary with plenty of entries for each
        category of analysis
    """

    parts_of_speech_strings = set()
    for pos, transitivity in analysis_results["pos_and_transitivity"]:
        pos_string = pos
        if transitivity:
            pos_string += f" ({transitivity})"

        parts_of_speech_strings.add(pos_string)

    analysis_results["synonyms"].add(word)

    # Configure Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("word_info_template.html")

    # Prepare data for the template
    sections = []

    if analysis_results["meanings"]:
        sections.append((f"Meaning of {word}", analysis_results["meanings"], False))

    if parts_of_speech_strings:
        sections.append((f"Part of speech for {word}", parts_of_speech_strings, False))

    if analysis_results["etymology"]:
        sections.append(
            (f"Etymology of {word}", [analysis_results["etymology"]], False)
        )

    if analysis_results["synonyms"]:
        sections.append((f"Synonyms of {word}", analysis_results["synonyms"], True))

    if analysis_results["antonyms"]:
        sections.append((f"Antonyms of {word}", analysis_results["antonyms"], True))

    if analysis_results["word_frequencies"]:
        sections.append(
            (
                "Word frequencies",
                [
                    f"{w}: {freq}"
                    for w, freq in analysis_results["word_frequencies"].items()
                ],
                True,
            )
        )

    if analysis_results["collocations"]:
        sections.append(
            (
                f"Collocations for {word} and its synonyms",
                [
                    f"{' '.join(bigram)} (Frequency: {freq})"
                    for bigram, freq in analysis_results["collocations"]
                ],
                False,
            )
        )

    if analysis_results["phrasal_verbs"]:
        sections.append(
            (f"Phrasal verbs of {word}", analysis_results["phrasal_verbs"], True)
        )

    if analysis_results["idiomatic_expressions"]:
        sections.append(
            (
                f"Idiomatic expressions with {word}",
                analysis_results["idiomatic_expressions"],
                False,
            )
        )

    if analysis_results["related_phrases_and_expressions"]:
        sections.append(
            (
                f"Related phrases and expressions with {word}",
                analysis_results["related_phrases_and_expressions"],
                False,
            )
        )

    if analysis_results["semantic_fields"]:
        sections.append(
            (f"Semantic field(s) of {word}", analysis_results["semantic_fields"], True)
        )

    if analysis_results["hyponyms"]:
        sections.append(
            (
                f"Hyponyms of {word}",
                [synset.split(".")[0] for synset in analysis_results["hyponyms"]],
                True,
            )
        )

    if analysis_results["hypernyms"]:
        sections.append(
            (
                f"Hypernyms of {word}",
                [synset.split(".")[0] for synset in analysis_results["hypernyms"]],
                True,
            )
        )

    if analysis_results["meronyms"]:
        sections.append(
            (
                f"Meronyms of {word}",
                [synset.split(".")[0] for synset in analysis_results["meronyms"]],
                True,
            )
        )

    if analysis_results["domain_words"]:
        sections.append(
            (
                f"Domain-specific words related to {word}",
                list(analysis_results["domain_words"]),
                True,
            )
        )

    if analysis_results["alternative_words"]:
        sections.append(
            (
                f"Alternative words for {word}",
                analysis_results["alternative_words"],
                True,
            )
        )

    if analysis_results["associated_nouns"]:
        sections.append(
            (
                f"Associated nouns with {word}",
                analysis_results["associated_nouns"],
                True,
            )
        )

    if analysis_results["associated_verbs"]:
        sections.append(
            (
                f"Associated verbs with {word}",
                analysis_results["associated_verbs"],
                True,
            )
        )

    if analysis_results["morphological_variations"]:
        sections.append(
            (
                f"Morphological variations of {word}",
                analysis_results["morphological_variations"],
                True,
            )
        )

    # Render the HTML content using Jinja2
    return template.render(word=word, sections=sections)


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

    save_html_to_file(word, prepare_html_content(word, analyze_word(word)))


def main():
    """Parses command-line arguments and calls the get_word_info function with the provided word."""

    # Configure logging
    logging.basicConfig(
        level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Use argparse for handling command-line arguments
    parser = argparse.ArgumentParser(
        description="Get detailed information about a given word."
    )
    parser.add_argument("word", help="The word to analyze.")
    args = parser.parse_args()

    try:
        get_word_info(args.word)
    except WordAnalysisError as exception:
        print(exception)
        logging.error(
            f"An error occurred during word analysis: {exception}", exc_info=True
        )
    except ValueError as exception:
        print(exception)
        logging.error(
            f"An error occurred during value processing: {exception}", exc_info=True
        )


if __name__ == "__main__":
    main()
