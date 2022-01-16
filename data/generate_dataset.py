import chardet
import glob
import os
import spacy

from sentence_manipulation.detect_passive_sentence import detect_passive_svo_sentence_from_string
from sentence_manipulation.passive_to_active import passive_to_active

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)


def get_raw_file_list():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    return glob.glob(dirpath + '/**/*.txt', recursive=True)

def process_single_string(textdoc, write_to_absolute_path):
    log.info('Using Spacy to parse document')
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(textdoc)
    log.info('Document successfully parsed. Beginning scanning for passive sentences.')

    with open(write_to_absolute_path, 'a') as f:
        found_passive_sentences = 0
        for k, sent in enumerate(doc.sents):
            if k % 100 == 0:
                log.info('Processing sentence %s of document' % (k,))
            try:
                if detect_passive_svo_sentence_from_string(sent.text, nlp):
                    found_passive_sentences += 1
                    log.info('Found passive sentence number %s. Sentence: %s' % (found_passive_sentences, sent.text))
                    f.write(sent.text + '\t' + passive_to_active(sent.text) + '\n')
            except ValueError as e:
                log.error('Error: %s. Offending sentence: %s. Skipping to next sentence.' % (e, sent))

def main():
    file_list = get_raw_file_list()
    dirpath = os.path.dirname(os.path.realpath(__file__))
    write_to_path = os.path.join(dirpath, 'processed/active_passive.tsv')
    for k, file_path in enumerate(file_list):
        log.info('Processing file %s/%s' % (k, len(file_list)))
        rawdata = open(file_path, 'rb').read()
        detected_encoding = chardet.detect(rawdata)['encoding']
        with open(file_path, encoding=detected_encoding) as f:
            try:
                log.info('Reading file %s as encoding %s' % (file_path, detected_encoding))
                textdoc = f.read().replace('\n', ' ')
            except Exception as e:
                log.error('Error when opening %s: %s' % (file_path, e))
                log.error('Skipping to next file...')
                continue
            process_single_string(textdoc, write_to_path)


if __name__ == '__main__':
    main()