import pytest
import spacy

from sentence_manipulation.detect_passive_sentence import get_first_root, detect_passive_svo_sentence, detect_passive_svo_sentence_from_string


def test_get_first_root():
    nlp = spacy.load("en_core_web_sm")
    assert get_first_root(nlp('The car is chased by the dog.')).text == 'chased'

def test_detect_passive_svo_sentences():
    nlp = spacy.load("en_core_web_sm")

    r1 = get_first_root(nlp('The car is chased by the dog.'))
    assert detect_passive_svo_sentence(r1) == True

    r2 = get_first_root(nlp('The book is yellow.'))
    assert detect_passive_svo_sentence(r2) == False

def test_detect_passive_svo_sentence_from_string():
    nlp = spacy.load("en_core_web_sm")

    assert detect_passive_svo_sentence_from_string('The car is chased by the dog.', nlp) == True
    assert detect_passive_svo_sentence_from_string('The book is yellow.', nlp) == False


if __name__ == '__main__':
    test_get_first_root()
    test_detect_passive_svo_sentences()
    test_detect_passive_svo_sentence_from_string()
