import spacy
from lemminflect import getInflection, getLemma

from data.identify_inflection import detect_inflection, isolate_auxiliaries

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)


def get_roots(doc):
    return [token for token in doc if token.head == token]

def get_first_root(doc):
    try:
        return [token for token in doc if token.head == token][0]
    except IndexError:
        raise ValueError('Cannot identify root of the following sentence: %s' % (doc.text))

def get_first_root_id(doc):
    return list(doc).index(get_first_root(doc))

def find_passive_svo_sentences(root, verbose=1):
    """Return True if the sentence is in passive voice and has subject, verb, object. Otherwise return false.
    :param root: the root (as a SpaCy token) of the sentence to check
    :param verbose: choose 1 to print the sentence being checked
    :returns: True if the sentence is in passive voice and has subject, verb, object, otherwise False"""
    if root.tag_ == 'VBN':
        # does it have an auxiliary passive verb?
        aux_pass_verbs = [dependent for dependent in root.children if dependent.dep_ == 'auxpass']
        if len(aux_pass_verbs) == 1:
            # does it have an nsubjpass and agent>pobj?
            noun_subject_passives = [dependent for dependent in root.children if dependent.dep_ == 'nsubjpass']
            if len(noun_subject_passives) == 1:
                nounsubject = noun_subject_passives[0]
                agentparticles = [dependent for dependent in root.children if dependent.dep_ == 'agent']
                if len(agentparticles) == 1:
                    agentparticle = agentparticles[0]
                    passive_objects = [dependent for dependent in agentparticle.children if dependent.dep_ == 'pobj']
                    if len(passive_objects) == 1:
                        nounobject = passive_objects[0]
                        if verbose >= 1:
                            log.debug("Detected passive SVO sentence: %s" % (root.sent))
                        return True
    if verbose >= 1:
        log.debug("Detected NOT passive SVO sentence: %s" % (root.sent))
    return False
