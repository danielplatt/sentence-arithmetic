import spacy
from lemminflect import getInflection, getLemma

from sentence_manipulation.detect_inflection import detect_inflection, isolate_auxiliaries

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

def detect_passive_svo_sentence(root):
    """Return True if the sentence is in passive voice and has subject, verb, object and is not a question.
     Otherwise return false.
    :param root: the root (as a SpaCy token) of the sentence to check
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
                        log.debug("Detected passive SVO sentence: %s" % (root.sent))
                        return True
    log.debug("Detected NOT passive SVO sentence: %s" % (root.sent))
    return False

def detect_passive_svo_sentence_from_string(sent, nlp):
    root = get_first_root(nlp(sent))
    return detect_passive_svo_sentence(root)
