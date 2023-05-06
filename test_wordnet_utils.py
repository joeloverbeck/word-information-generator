import unittest

from wordnet_utils import get_associated_nouns_verbs, get_synonyms_antonyms


class TestWordnetUtils(unittest.TestCase):

    def test_get_synonyms_antonyms_white(self):
        synonyms, antonyms = get_synonyms_antonyms("white")
        
        expected_synonyms = {"ovalbumin", "gabardine", "clean"}
        expected_antonyms = {"black", "blacken"}
        
        self.assertTrue(expected_synonyms.issubset(synonyms), f"Expected synonyms not found: {expected_synonyms - synonyms}")
        self.assertTrue(expected_antonyms.issubset(antonyms), f"Expected antonyms not found: {expected_antonyms - antonyms}")


    def test_get_associated_nouns_verbs(self):
        nouns, verbs = get_associated_nouns_verbs("white")

        expected_nouns = {"lividity", "snow", "white", "whitening", "whiteness", "whitener", "lividness", "White", "blankness"}
        expected_verbs = {"white"}

        self.assertTrue(expected_nouns.issubset(nouns), f"Expected nouns not found: {expected_nouns - nouns}")
        self.assertTrue(expected_verbs.issubset(verbs), f"Expected verbs not found: {expected_verbs - verbs}")
    

if __name__ == "__main__":
    unittest.main()
