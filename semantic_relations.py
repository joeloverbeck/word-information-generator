
from nltk.corpus import wordnet as wn

from progress_reporter import progress_wrapper
from utils import replace_underscore_with_space


@progress_wrapper
def get_semantic_fields(word):
    synsets = wn.synsets(word)
    semantic_fields = []
    for synset in synsets:
        for hypernym in synset.hypernyms():
            semantic_fields.append(replace_underscore_with_space(hypernym.name().split('.')[0]))
    return semantic_fields

@progress_wrapper
def get_semantic_relations(word):
    synsets = wn.synsets(word)
    hyponyms = []
    hypernyms = []
    meronyms = []
    for synset in synsets:
        hyponyms.extend([replace_underscore_with_space(hypo.name()) for hypo in synset.hyponyms()])
        hypernyms.extend([replace_underscore_with_space(hyper.name()) for hyper in synset.hypernyms()])
        meronyms.extend([replace_underscore_with_space(mero.name()) for mero in synset.part_meronyms()])
        meronyms.extend([replace_underscore_with_space(mero.name()) for mero in synset.substance_meronyms()])
        meronyms.extend([replace_underscore_with_space(mero.name()) for mero in synset.member_meronyms()])
    return hyponyms, hypernyms, meronyms
