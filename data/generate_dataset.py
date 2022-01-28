import chardet
from csv import DictReader
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

def generate_from_all_txt():
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

def generate_from_recent_authors():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    metadata_path = os.path.join(dirpath, 'metadata/metadata.csv')

    write_to_path = os.path.join(dirpath, 'processed/active_passive.tsv')

    with open(metadata_path, 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        csv_dict_reader = DictReader(read_obj)
        # iterate over each line as a ordered dictionary
        for k, row in enumerate(csv_dict_reader):
            try:
                if row['language'] == "['en']" and int(row['authoryearofdeath']) >= 1900:
                    pass
                else:
                    continue
            except ValueError as e:
                pass
            # now trying to locate the corresponding file
            file_path = os.path.join(dirpath, 'text/' + row['id'] + '_text.txt')
            print('Trying file %s of around 60000' % (k,))
            try:
                with open(file_path, 'r') as read_obj:
                    textdoc = read_obj.read().replace('\n', ' ')
                    process_single_string(textdoc, write_to_path)
            except FileNotFoundError as e:
                print(e)
            except ValueError as e:
                print(e)

if __name__ == '__main__':
    generate_from_recent_authors()