import pandas as pd
import random


def read_data(csv='processed/active_passive.tsv', csv_separator='\t'):
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

def main():
    df = read_data()
    new_df = df.applymap(jumble_sentence)
    save_data(new_df)
    verify_jumbling()


if __name__ == '__main__':
    main()
