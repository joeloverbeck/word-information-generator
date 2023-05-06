

from nltk.corpus import wordnet as wn
from nltk.corpus import webtext
from progress_reporter import progress_wrapper

from utils import check_word_exists, replace_underscore_with_space

pos_map = {'n': 'noun', 'v': 'verb', 'a': 'adjective', 's': 'adjective', 'r': 'adverb'}


def process_word_info(word, callback):
    results = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            result = callback(synset, lemma)
            if result:
                results.update(result)
    return results


def get_pos(synset, pos_map):
    pos = pos_map.get(synset.pos(), synset.pos())
    return pos


def get_transitivity(synset, pos):
    if pos != 'verb':
        return None

    transitivity = 'intransitive'

    for lemma in synset.lemmas():
        for frame in lemma.frame_strings():
            if 'Something' in frame or 'somebody' in frame:
                transitivity = 'transitive'
                break
        else:
            continue
        break

    return transitivity


@progress_wrapper
@check_word_exists
def get_related_phrases_and_expressions(word):
    related_expressions = []
    word_lower = word.lower()
        
    for fileid in webtext.fileids():
        for sent in webtext.sents(fileid):
            lower_sent = [w.lower() for w in sent]
            if word_lower in lower_sent:
                index = lower_sent.index(word_lower)
                phrase = ' '.join(sent[max(0, index - 4):index + 6])
                related_expressions.append(phrase)
                    
                if len(related_expressions) >= 15:
                    return related_expressions

    return related_expressions


@progress_wrapper
@check_word_exists
def get_pos_and_transitivity(word):
    pos_and_transitivity = []
    
    for synset in wn.synsets(word):
        pos = get_pos(synset, pos_map)
        transitivity = get_transitivity(synset, pos)
        
        pos_and_transitivity.append((pos, transitivity))

    return pos_and_transitivity


def get_phrasal_verbs_callback(synset, lemma):
    if ' ' in lemma.name():
        return [replace_underscore_with_space(lemma.name())]

@progress_wrapper
@check_word_exists
def get_phrasal_verbs(word):
    return process_word_info(word, get_phrasal_verbs_callback)


def get_idiomatic_expressions_callback(synset, lemma):
    for frame in lemma.frame_strings():
        if "Idiom" in frame:
            return [replace_underscore_with_space(lemma.name())]
        
@progress_wrapper
@check_word_exists
def get_idiomatic_expressions(word):
    return process_word_info(word, get_idiomatic_expressions_callback)


def get_meanings_callback(synset, lemma):
    return {synset.definition()}


@progress_wrapper
@check_word_exists
def get_meanings(word):
    return set(process_word_info(word, get_meanings_callback))


@progress_wrapper
@check_word_exists
def get_synonyms_antonyms(word):

    def process_word_info_for_synonyms_and_antonyms(synset, lemma):
        synonyms = {replace_underscore_with_space(lemma.name())}
        antonyms = {replace_underscore_with_space(antonym.name()) for antonym in lemma.antonyms()}
        return synonyms, antonyms
    
    synonyms = set()
    antonyms = set()
    
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            syns, ants = process_word_info_for_synonyms_and_antonyms(synset, lemma)
            if syns:
                synonyms.update(syns)
            if ants:
                antonyms.update(ants)
                
    return synonyms, antonyms


def get_alternative_words_callback(synset, lemma):
    return [sim_lemma.name() for sim_synset in lemma.synset().similar_tos() for sim_lemma in sim_synset.lemmas()]


@progress_wrapper
@check_word_exists
def get_alternative_words(word):
    return process_word_info(word, get_alternative_words_callback)


def get_domain_words_callback(synset, lemma):
    return {replace_underscore_with_space(dom_lemma.name()) for domain in synset.topic_domains() for dom_lemma in domain.lemmas()}


@progress_wrapper
@check_word_exists
def get_domain_words(word):
    return process_word_info(word, get_domain_words_callback)


@progress_wrapper
@check_word_exists
def get_associated_nouns_verbs(word):
    nouns, verbs = set(), set()

    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            for related_lemma in lemma.derivationally_related_forms():
                related_synset = related_lemma.synset()
                if related_synset.pos() == 'n':
                    nouns.add(related_lemma.name())
                elif related_synset.pos() == 'v':
                    verbs.add(related_lemma.name())
                    
    return nouns, verbs
