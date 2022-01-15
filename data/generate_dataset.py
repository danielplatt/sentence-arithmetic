import os
import spacy

from sentence_manipulation.detect_passive_sentence import detect_passive_svo_sentence_from_string
from sentence_manipulation.passive_to_active import passive_to_active

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)


nlp = spacy.load("en_core_web_sm")

dirpath = os.path.dirname(os.path.realpath(__file__))
newpath = os.path.join(dirpath, 'raw/1-0.txt')

with open(newpath) as f:
    textdoc = f.read().replace('\n', ' ')

doc = nlp(textdoc)

newpath = os.path.join(dirpath, 'processed/active_passive.tsv')

with open(newpath, 'a') as f:
    for sent in doc.sents:
        try:
            if detect_passive_svo_sentence_from_string(sent.text, nlp):
                f.write(sent.text + '\t' + passive_to_active(sent.text) + '\n')
        except ValueError as e:
            log.error('Error: %s. Offending sentence: %s. Skipping to next sentence.' % (e, sent))
