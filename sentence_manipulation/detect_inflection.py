import spacy

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)

nlp = spacy.load("en_core_web_sm")


def isolate_auxiliaries(doc):
    """Return the auxiliary verbs directly depending on the first root in a document.
    Example: input: 'The cars will have been chased by the dog.' output: ['will', 'have', 'been']
    Example: input: 'The lunch was eaten by the kid who walked to school.' output: ['was']
    :param doc: a spacy parsed document. Can contain arbitrarily many sentences, only the first one is considered.
    :returns: a list of auxiliary verbs directly depending on the first root in the document
    """
    root = [token for token in doc if token.head == token][0]
    auxiliaries = [tok.text for tok in root.children if tok.dep_ == 'aux' or tok.dep_ == 'auxpass']
    return auxiliaries

def detect_inflection(auxiliaries):
    """Return the inflection of a given list of auxiliary verbs used in a passive voice sentence. May return wrong information or None for active voice sentences.
    Example: input: ['got'] output: ('simple past', 'unknown')
    Example: input: ['should', 'have', 'been'] output: ('aux: should plus have been', 'unknown')
    :param auxiliaries: a list of auxiliary verbs
    :returns: depending on the inflection of the verbs, one of the following: (tense and modifier, person) such as ('simple present', '3rd person singular') or for auxiliary verbs different from "be" a tuple such as ('aux: must plus be', 'unknown')
    """
    auxiliaries = ' '.join(auxiliaries)
    if auxiliaries == 'is' or auxiliaries == 'gets':
        return ('simple present', '3rd person singular')
    if auxiliaries == 'am' or auxiliaries == 'are' or auxiliaries == 'get':
        return ('simple present', 'non-3rd person singular')
    if auxiliaries == 'was':
        return ('simple past', '1st or 3rd person singular')
    if auxiliaries == 'were':
        return ('simple past', 'not 3rd person singular (could be 1st)')
    if auxiliaries == 'got':
        return ('simple past', 'unknown')
    if auxiliaries == 'is being' or auxiliaries == 'is getting':
        return ('present progressive', '3rd person singular')
    if auxiliaries == 'are being' or auxiliaries == 'are getting' or auxiliaries == 'am being' or auxiliaries == 'am getting':
        return ('present progressive', 'non-3rd person singular')
    if auxiliaries == 'was being' or auxiliaries == 'was getting':
        return ('past progressive', '1st or 3rd person singular')
    if auxiliaries == 'were being' or auxiliaries == 'were getting':
        return ('past progressive', 'not 3rd person singular (could be 1st)')
    if auxiliaries == 'has been' or auxiliaries == 'has got':
        return ('present perfect', '3rd person singular')
    if auxiliaries == 'have been' or auxiliaries == 'have got':
        return ('present perfect', 'non-3rd person singular')
    if auxiliaries == 'had been' or auxiliaries == 'had got':
        return ('past perfect', 'unknown')
    if auxiliaries == 'will be' or auxiliaries == 'will get':
        return ('simple future', 'unknown')
    if auxiliaries == 'will have been' or auxiliaries == 'will have got':
        return ('future perfect', 'unknown')

    if len(auxiliaries.split(' ')) == 2 and (auxiliaries.split(' ')[1] == 'be' or auxiliaries.split(' ')[1] == 'get'):
        return 'aux: ' + auxiliaries.split(' ')[0] + ' plus be', 'unknown'
    if len(auxiliaries.split(' ')) == 3 and auxiliaries.split(' ')[1] == 'have' and (auxiliaries.split(' ')[2] == 'been' or auxiliaries.split(' ')[2] == 'got'):
        return 'aux: ' + auxiliaries.split(' ')[0] + ' plus have been', 'unknown'
