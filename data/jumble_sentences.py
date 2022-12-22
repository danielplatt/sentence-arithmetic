import pandas as pd
import random


def read_data(csv='processed/active_passive_full_beautiful.tsv', csv_separator='\t'):
    try:
        return pd.read_csv(csv, sep=csv_separator, on_bad_lines='skip', header=None)
    except FileNotFoundError as e:
        print('Cannot find active passive from literature sentences .tsv file. Unzipping active_passive.tsv.zip should fix this problem.')
        raise(e)

def jumble_sentence(sent):
    words = str(sent).split()
    random.shuffle(words)
    jumbled_sentence = ' '.join(words)
    return jumbled_sentence

def add_by_at_start(sent):
    return f'by {sent}'

def save_data(df, csv='processed/active_passive_jumbled.tsv', csv_separator='\t'):
    df.to_csv(csv, header=False, index=False, sep=csv_separator)

def verify_jumbling(
        original_csv='processed/active_passive.tsv',
        original_csv_separator='\t',
        jumbled_csv='processed/active_passive_jumbled.tsv',
        jumbled_csv_separator='\t'):
    original_df = pd.read_csv(original_csv, sep=original_csv_separator, on_bad_lines='skip', header=None)
    jumbled_df = pd.read_csv(jumbled_csv, sep=jumbled_csv_separator, on_bad_lines='skip', header=None)
    assert(original_df.shape == jumbled_df.shape)

def jumble_file(source_csv, target_csv, csv_separator='\t'):
    df = read_data(csv=source_csv, csv_separator=csv_separator)
    new_df = df.applymap(jumble_sentence)
    save_data(new_df, csv=target_csv, csv_separator=csv_separator)
    verify_jumbling(
        original_csv=source_csv,
        original_csv_separator=csv_separator,
        jumbled_csv=target_csv,
        jumbled_csv_separator=csv_separator
    )

def add_by_at_start_of_sentences(source_csv, target_csv, csv_separator='\t'):
    df = read_data(csv=source_csv, csv_separator=csv_separator)
    new_df = df.applymap(add_by_at_start)
    save_data(new_df, csv=target_csv, csv_separator=csv_separator)
    verify_jumbling(
        original_csv=source_csv,
        original_csv_separator=csv_separator,
        jumbled_csv=target_csv,
        jumbled_csv_separator=csv_separator
    )



if __name__ == '__main__':
    jumble_file('processed/active_passive_full_beautiful.tsv', 'processed/active_passive_jumbled.tsv', csv_separator='\t')
    add_by_at_start_of_sentences('processed/active_passive_full_beautiful.tsv', 'processed/active_passive_by_added.tsv', csv_separator='\t')
    # jumble_file(
    #     '../PCAetc/data/simple_example_sentences.csv',
    #     '../PCAetc/data/simple_example_sentences_jumbled.csv',
    #     csv_separator=',')
