import csv
import os
import truecase
from tqdm import tqdm


def detect_colon(sent):
    return ';' in sent

def detect_parentheses(sent):
    return ('(' in sent) or (')' in sent)

def detect_quotation_marks(sent):
    return ('"' in sent) or ("'" in sent) or ('`' in sent)

def detect_banned_characters(sent):
    return detect_colon(sent) or detect_parentheses(sent) or detect_quotation_marks(sent) or ('_' in sent) or ('--' in sent) or ('|' in sent) or ('#' in sent) or ('*' in sent) or ('+' in sent) or ('=' in sent) or ('~' in sent) or ('[' in sent) or (']' in sent) or (':' in sent) or ('<' in sent) or ('>' in sent) or ('/' in sent) or ('\\' in sent)

def process_sentence(sent):
    if detect_colon(sent) or detect_parentheses(sent):
        return ''
    else:
        return truecase.get_true_case(sent)

def beautify_dataset(filename_in='active_passive_full.tsv', filename_out='active_passive_full_beautiful.tsv'):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(dirpath, f'processed/{filename_in}')
    output_path = os.path.join(dirpath, f'processed/{filename_out}')

    with open(input_path, 'r') as in_f:
        datareader = csv.reader(in_f, delimiter='\t')
        row_count = sum(1 for _ in datareader)

    with open(input_path, 'r') as in_f:
        datareader = csv.reader(in_f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in tqdm(datareader, total=row_count):
                if not detect_banned_characters(row[0]) and not detect_banned_characters(row[1]):
                    try:
                        with open(output_path, 'a') as out_f:
                            out_f.write(process_sentence(row[0]) + '\t' + process_sentence(row[1]) + '\n')
                    except IndexError as _:
                        print(f'Cannot beautify sentence pair {row}. Maybe no active sentence there? Skipping to next.')
                        input('')


if __name__ == '__main__':
    # sent = 'Although Ligurians or Umbrians were probably at one time settled there , the Etruscan occupation and civilization almost wholly has effaced the traces of they .'
    # print(process_sentence(sent))
    beautify_dataset()
