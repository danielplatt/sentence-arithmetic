import pytest
import spacy

from sentence_manipulation.detect_passive_sentence import get_first_root, find_passive_svo_sentences


def test_get_first_root():
    nlp = spacy.load("en_core_web_sm")
    assert get_first_root(nlp('The car is chased by the dog.')).text == 'chased'

def test_find_passive_svo_sentences():
    nlp = spacy.load("en_core_web_sm")

    r1 = get_first_root(nlp('The car is chased by the dog.'))
    assert find_passive_svo_sentences(r1) == True

    r2 = get_first_root(nlp('The book is yellow.'))
    assert find_passive_svo_sentences(r2) == False


if __name__ == '__main__':
    test_get_first_root()
    test_find_passive_svo_sentences()
