import spacy
from lemminflect import getInflection, getLemma
import inflect

from sentence_manipulation.detect_inflection import detect_inflection, isolate_auxiliaries
from sentence_manipulation.detect_passive_sentence import get_first_root_id

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)

nlp = spacy.load("en_core_web_sm")


def replace_verb_and_change_singular_plural(aux, verb, to_third_pers_sing):
    inflection = detect_inflection(aux)
    if inflection == None:
        raise ValueError('Verb form cannot be determined.')
    if inflection[0] == 'simple present' and to_third_pers_sing:
        new_verb = getInflection(verb, 'VBZ')[0]
    if inflection[0] == 'simple present' and not to_third_pers_sing:
        new_verb = getInflection(verb, 'VBP')[0]
    if inflection[0] == 'simple past':
        new_verb = getInflection(verb, 'VBD')[0]
    if inflection[0] == 'present progressive' and to_third_pers_sing:
        new_verb = 'is ' + getInflection(verb, 'VBG')[0]
    if inflection[0] == 'present progressive' and not to_third_pers_sing:
        new_verb = 'are ' + getInflection(verb, 'VBG')[0]
    if inflection[0] == 'past progressive':
        new_verb = aux[0] + getInflection(verb, 'VBG')[0]
    if inflection[0] == 'present perfect' and to_third_pers_sing:
        new_verb = 'has ' + getInflection(verb, 'VBN')[0]
    if inflection[0] == 'present perfect' and not to_third_pers_sing:
        new_verb = 'have ' + getInflection(verb, 'VBN')[0]
    if inflection[0] == 'past perfect':
        new_verb = 'had ' + getInflection(verb, 'VBN')[0]
    if inflection[0] == 'simple future':
        new_verb = 'will ' + getInflection(verb, 'VB')[0]
    if inflection[0] == 'future perfect':
        new_verb = 'will have ' + getInflection(verb, 'VBN')[0]

    if inflection[0].split(' ')[0] == 'aux:':
        if inflection[0].split(' ')[-1] == 'be':
            new_verb = inflection[0].split(' ')[1] + ' ' + getInflection(verb, 'VB')[0]
        if inflection[0].split(' ')[-1] == 'been':
            new_verb = inflection[0].split(' ')[1] + ' have ' + getInflection(verb, 'VBN')[0]
    return new_verb

def replace_verb(aux, verb):
    """Return the active voice of a verb given its passive voice, leaving singular/plural unchanged.
    Example: input: (['will', 'have', 'been'], 'target')), output: 'will have targeted'.
    Raises ValueError if verb form cannot be determined.
    :param aux: a list of auxiliary verbs of a passive voice sentence
    :param verb: the lemma of a verb as a string
    :returns: the inflected form of the verb in active voice
    """
    inflection = detect_inflection(aux)
    if inflection == None:
        raise ValueError('Verb form cannot be determined.')
    if inflection[0] == 'simple present' and inflection[1] == '3rd person singular':
        new_verb = getInflection(verb, 'VBZ')[0]
    if inflection[0] == 'simple present' and inflection[1] == 'non-3rd person singular':
        new_verb = getInflection(verb, 'VBP')[0]
    if inflection[0] == 'simple past':
        new_verb = getInflection(verb, 'VBD')[0]
    if inflection[0] == 'present progressive' and inflection[1] == '3rd person singular':
        new_verb = 'is ' + getInflection(verb, 'VBG')[0]
    if inflection[0] == 'present progressive' and inflection[1] == 'non-3rd person singular':
        new_verb = 'are ' + getInflection(verb, 'VBG')[0]
    if inflection[0] == 'past progressive':
        new_verb = aux[0] + getInflection(verb, 'VBG')[0]
    if inflection[0] == 'present perfect' and inflection[1] == '3rd person singular':
        new_verb = 'has ' + getInflection(verb, 'VBN')[0]
    if inflection[0] == 'present perfect' and inflection[1] == 'non-3rd person singular':
        new_verb = 'have ' + getInflection(verb, 'VBN')[0]
    if inflection[0] == 'past perfect':
        new_verb = 'had ' + getInflection(verb, 'VBN')[0]
    if inflection[0] == 'simple future':
        new_verb = 'will ' + getInflection(verb, 'VB')[0]
    if inflection[0] == 'future perfect':
        new_verb = 'will have ' + getInflection(verb, 'VBN')[0]

    if inflection[0].split(' ')[0] == 'aux:':
        if inflection[0].split(' ')[-1] == 'be':
            new_verb = inflection[0].split(' ')[1] + ' ' + getInflection(verb, 'VB')[0]
        if inflection[0].split(' ')[-1] == 'been':
            new_verb = inflection[0].split(' ')[1] + ' have ' + getInflection(verb, 'VBN')[0]
    return new_verb

def is_pobj_third_pers_sing(doc):
    inflect_engine = inflect.engine()
    root_id = get_first_root_id(doc)
    agent_id = get_agent_id(doc, root_id)
    agent_token = doc[agent_id]
    for tok in agent_token.children:
        if tok.dep_ == "pobj":
            if tok.text.lower() in set(['i', 'you', 'we', 'they']):
                return False
            elif not inflect_engine.singular_noun(tok.text):
                return True
            else:
                return False

def inflect_sentence(doc, tokenid, swap, level=0):
    assert len(swap) == 3 or len(swap) == 2

    if len(swap) == 2:
    # swap[0] = agent
    # swap[1] = nsubjpass
        if tokenid == swap[0]:
            root = doc[swap[1]]
        elif tokenid == swap[1]:
            root = doc[swap[0]]
        else:
            root = doc[tokenid]

    if len(swap) == 3:
    # swap[0] = agent
    # swap[1] = nsubjpass
    # swap[2] = dobj
        if tokenid == swap[0]:
            root = doc[swap[2]]
        elif tokenid == swap[1]:
            print('swap0')
            print(swap[0])
            root = doc[swap[0]]
        elif tokenid == swap[2]:
            root = doc[swap[1]]
        else:
            root = doc[tokenid]

    inflected_sentence = ''

    #for left in list(root.lefts):
    #    print(left)

    for left in list(root.lefts):
        inflected_sentence += inflect_sentence(doc, list(doc).index(left), swap, level=level+1)

    if level<=1 and (root.dep_ == "auxpass" or root.dep_ == "agent" or root.dep_ == "aux"):
        pass
    elif root.dep_ == "ROOT":
        aux = isolate_auxiliaries(doc)
        inflected_sentence += replace_verb_and_change_singular_plural(aux, getLemma(root.text, upos='VERB')[0], is_pobj_third_pers_sing(doc))
        inflected_sentence += ' '
    else:
        if root.dep_ == "pobj" and 'by' in [tok.text for tok in root.ancestors]:
            inflected_sentence += accusative_to_nominative(root.text)
        elif root.dep_ == "nsubjpass":
            inflected_sentence += nominative_to_accusative(root.text)
        else:
            inflected_sentence += root.text
        inflected_sentence += ' '

    for right in list(root.rights):
        inflected_sentence += inflect_sentence(doc, list(doc).index(right), swap, level=level+1)
    return inflected_sentence

def get_agent_id(doc, root_id):
    root = doc[root_id]
    agent_id = None
    for tok in root.children:
        if tok.dep_ == "agent":
            agent_id = list(doc).index(tok)
    # if agent_id == None:
    #     for tok in root.children:
    #         for childtok in tok.children:
    #             print(childtok.text, childtok.dep_)
    #             if childtok.dep_ == "prep":
    #                 agent_id = list(doc).index(childtok)
    return agent_id
    # TODO: combine the two for loops


def get_nsubjpass_id(doc, root_id):
    root = doc[root_id]
    for tok in root.children:
        if tok.dep_ == "nsubjpass":
            return list(doc).index(tok)

def get_dobj_or_oprd(doc, root_id):
    root = doc[root_id]
    for tok in root.children:
        #print(tok.text, tok.dep_)
        if tok.dep_ == "dobj" or tok.dep_== "oprd":
            return list(doc).index(tok)

def passive_to_active(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    #for k in doc:
    #    print(k.text, k.dep_)
    first_root_id = get_first_root_id(doc)
    agent_id = get_agent_id(doc, first_root_id)
    print('agentid', agent_id)
    nsubjpass_id = get_nsubjpass_id(doc, first_root_id)
    dobj_id = get_dobj_or_oprd(doc, first_root_id)
    if dobj_id == None:
        swap = (agent_id, nsubjpass_id)
    else:
        swap = (agent_id, nsubjpass_id, dobj_id)
    #print(len(swap))
    root_id = get_first_root_id(doc)
    try:
        return inflect_sentence(doc, root_id, swap)
    except (IndexError, TypeError) as _:
        raise ValueError('Cannot make this sentence active voice (maybe already active voice?): %s' % (sentence, ))

def accusative_to_nominative(word):
    if word.lower() == 'me':
        return 'I'
    elif word.lower() == 'him':
        return 'he'
    elif word.lower() == 'her':
        return 'she'
    elif word.lower() == 'us':
        return 'we'
    elif word.lower() == 'them':
        return 'they'
    else:
        return word

def nominative_to_accusative(word):
    if word.lower() == 'i':
        return 'me'
    elif word.lower() == 'he':
        return 'him'
    elif word.lower() == 'she':
        return 'her'
    elif word.lower() == 'we':
        return 'us'
    elif word.lower() == 'they':
        return 'them'
    else:
        return word


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")
    sentences = [
        'He had been given the best of education by his father, and had early experience in public affairs as governor of a province.',
        #'He was made chancellor by her.',
        'Although Ligurians or Umbrians were probably at one time(5) settled there, the traces of them have been almost wholly effaced by the Etruscan occupation and civilization.'
    ]
    for sent in sentences:
        print(passive_to_active(sent))
