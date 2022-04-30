import spacy

from sentence_manipulation.detect_passive_sentence import detect_passive_svo_sentence_from_string
from sentence_manipulation.passive_to_active import passive_to_active


def activify(sentence: str) -> str:
    '''
    Transforms an active voice sentence into a passive voice sentence. The function
    changes word order, inflection, and removes the word "by". Capitalisation and
    punctuation remains unchanged.

    Examples:
    Input: 'The car is chased by the dog.' -> Output: 'the dog chases The car . '
    Input: 'The dog chases the car.' -> Raises ValueError, because the input
    is not a passive voice sentence.

    :param sentence: A string containing a passive voice sentence.
    :return: A string containing the same sentence but inflected to active voice.
    :raises: ValueError, if the sentence cannot be inflected. This is for example
    the case if activify is applied to an active voice sentence.
    '''
    nlp = spacy.load("en_core_web_sm")
    detect_passive_svo_sentence_from_string(sentence, nlp)
    return passive_to_active(sentence)
