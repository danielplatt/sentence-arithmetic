import csv
import numpy as np
from numpy import linalg as LA
import pandas as pd
import matplotlib as plt
import os

import typing
from tqdm import tqdm

## Various embedding functions for sentences.

# Choose a default model here.
from sentence_transformers import SentenceTransformer

default_model_str = 'all-MiniLM-L6-v2' # 'all-mpnet-base-v2'


# Sentence (or list of sentences) to embedding(s)
def sentence_to_embedding(sentence: str,
                          model_str: str = default_model_str):
    model = SentenceTransformer(model_str)
    return model.encode(sentence).tolist()


# Converts a pandas file of sentences (no index) to a np.array of embeddings
# Returns a np.array
def sentences_pd_to_embedding(sentences: pd.DataFrame,
                              model_str: str = default_model_str,
                              csv_has_line_numbers: bool = True,
                              return_clean_sentence_list: bool = False) -> np.array:
    # Coverts to a list of lists, then applies the sentence transformer to each item.
    if csv_has_line_numbers:
        first_column_index = 1
    else:
        first_column_index = 0
    print(f"Using model {model_str}")
    model = SentenceTransformer(model_str)

    sentences_list = sentences.values.tolist()
    clean_sentences = []
    embeddings_list = []
    for sublist in tqdm(sentences_list):
        try:
            embeddings_sublist = []
            # sublist has length 2 for active/passive
            for sentence in sublist[first_column_index:]:
                embeddings_sublist.append(model.encode(sentence).tolist())
            embeddings_list.append(embeddings_sublist)
            clean_sentences.append(sublist)
        except TypeError as e:
            print('A sentence cannot be embedded. Sentence: %s. Error: %s.' % (sentence, e,))
            continue
    if return_clean_sentence_list:
        return np.array(embeddings_list), clean_sentences
    else:
        return np.array(embeddings_list)


# Converts a .csv of sentences to a np.array of embeddings.

# The .csv can either have one column or many columns in the x-direction.
# csv should be entered as a string giving the csv location eg 'data/sentences.csv'

# Optionally can truncate after a certain y-value in the .csv,
# helpful if the list of sentences is too long, or just for testing purposes.
# For a list of eg 100 sentences, set truncate to 100.

# Optionally, you can choose to save the output as a .npy by providing a directory location.

# The output array is a 3-dimensional array. The dimensions are as follows:
# The first index of the array is the y-direction of the csv.
# The second index of the array is the x-direction of the csv.
# The third index of the array is the embedding, for instance a 768-dimensional vector
# In the case that the input csv only has 1 column of sentences, a 3-dim array is still returned.

def sentences_csv_to_embedding(csvfile: str,
                               model_str: str = default_model_str,
                               truncate: int = None,
                               save_npy: str = None,
                               csv_separator: str = ',',
                               csv_has_line_numbers: bool = True,
                               header = 'infer',
                               save_cleaned_sentence_list: bool = False) -> np.array:
    # Read in the csv and do pre-processing
    print(f"Reading {csvfile}")
    sentences = pd.read_csv(csvfile, sep=csv_separator, on_bad_lines='skip', header=header)
    try:
        sentences = sentences.drop(columns=['index'])
    except KeyError:
        pass
    if truncate is not None:
        sentences = sentences.truncate(after=truncate - 1)

    if save_cleaned_sentence_list:
        embeddings_array, clean_sentences_list = sentences_pd_to_embedding(sentences, model_str, csv_has_line_numbers=csv_has_line_numbers, return_clean_sentence_list=True)
    else:
        embeddings_array = sentences_pd_to_embedding(sentences, model_str, csv_has_line_numbers=csv_has_line_numbers)

    if save_npy is not None:
        try:
            np.save(save_npy, embeddings_array)
        except:
            print(f"Please enter save_npy in the format location/filename.npy")

    if save_cleaned_sentence_list:
        dirpath = os.path.dirname(os.path.realpath(__file__))
        write_to_path = os.path.join(dirpath, '../data/processed/active_passive_full_cleaned.tsv')
        with open(write_to_path, 'w', newline='') as f:
            for sentencepair in clean_sentences_list:
                f.write(sentencepair[0] + '\t' + sentencepair[1] + '\n')

    return embeddings_array


# Computes the difference between two columns of sentences
# Returns a np.array as in sentences_csv_to_embedding
# But with 3 columns: the embedding of column1, the embedding of column2 and the vector difference emb(column1) - emb(column2)
# NB if column1 > column2, the resulting array is reordered so that column1 is the first column and column2 is the second column
def sentences_csv_embeddings_difference(csv: str,
                                        column1: str,
                                        column2: str,
                                        model_str: str = default_model_str,
                                        truncate: int = None,
                                        save_npy: str = None) -> np.array:
    # Read in the csv and do pre-processing
    print(f"Reading {csv}")
    sentences = pd.read_csv(csv)
    try:
        sentences = sentences.drop(columns=['index'])
    except KeyError:
        pass
    if truncate is not None:
        sentences = sentences.truncate(after=truncate - 1)

    # Drop all but column1 and column2, also reorders so column1 is first.
    sentences = sentences[[column1, column2]]

    # Convert to np.array of embeddings
    embeddings_array = sentences_pd_to_embedding(sentences, model_str)

    # Create array of differences
    # Note that np.diff calculates the difference col2 - col1, so need to take np.negative after.
    print(f"Calculating the difference: emb(col({column1})) - emb(col({column2})).")
    difference = np.negative(np.diff(embeddings_array, axis=1))

    embeddings_and_diff = np.concatenate([embeddings_array, difference], axis=1)

    if save_npy is not None:
        try:
            np.save(save_npy, embeddings_and_diff)
        except:
            print(f"Please enter save_npy in the format location/filename.npy")

    return embeddings_and_diff


## Mean difference functions

## Given a np.array or .npy as outputted from sentences_csv_embeddings_difference,
# (ie 3 columns: col1, col2 and col1 - col2)
# calculates the mean difference vector (mdv)

# If the elements of col1 are A_j and col2 are B_i, we then compute the norms
# |A_j - (B_i + mdv)|
# We then sort the distances by argument using np.argsort
# For each i, we then return the location of |A_i - (B_i + mdv)| in the sorted list.
# i.e. if A_i is closer to B_i + mdv than A_j for any other j, we return 0 in the ith position.
# if A_i is 3rd closest to B_i + mdv, we return 2 in the ith position.

def mean_difference_fn(array_in: typing.Union[str, np.array],
                       truncate=None):
    try:
        arr = np.load(array_in)
        print(f"Loading {array_in}")
    except TypeError:
        arr = array_in

    if truncate is not None:
        col_length = min(arr.shape[0], truncate - 1)

    col1 = arr[:, 0]
    col2 = arr[:, 1]
    difference = arr[:, 2]
    mdv = np.reshape(np.mean(difference, axis=0), (1, 768))
    col2_plus_mdv = np.add(col2, mdv)

    lst = []
    for i in tqdm(range(col_length)):
        sublst = []
        for j in range(col_length):
            sublst.append(LA.norm(col1[j, :] - col2_plus_mdv[i, :]))
        argsorted = np.argsort(np.array(sublst))
        lst.append(np.where(argsorted == i))
    return np.array(lst).flatten()


def mean_of_mean_difference(argsorted_list: list) -> float:
    return np.mean(argsorted_list)

def count_nonzero_mean_difference(argsorted_list: list) -> int:
    return np.count_nonzero(argsorted_list)

def compute_simple_example_embeddings():
    try:
        sentences_csv_to_embedding(csvfile='data/simple_example_sentences.csv',
                                   save_npy='data/simple_example_sentences_embedding.npy', truncate=50000)
    except FileNotFoundError as e:
        print('Cannot find simple example sentences .csv file. Running generator.py should generate this file.')
        print(e)

def compute_simple_example_jumbled_embeddings():
    try:
        sentences_csv_to_embedding(csvfile='data/simple_example_sentences_jumbled.csv',
                                   save_npy='data/simple_example_sentences_jumbled_embedding.npy', truncate=50000)
    except FileNotFoundError as e:
        print('Cannot find active passive jumbled from literature sentences .tsv file. Running jumble_sentences.py should fix this problem.')
        print(e)

def compute_active_passive_literature_embeddings():
    try:
        sentences_csv_to_embedding(csvfile='../data/processed/active_passive_full_beautiful.tsv',
                                   save_npy='../data/processed/active_passive_embedding_full.npy', truncate=None, csv_separator='\t', csv_has_line_numbers=False, header=None, save_cleaned_sentence_list=True)
    except FileNotFoundError as e:
        print('Cannot find active passive from literature sentences .tsv file. Unzipping active_passive.tsv.zip should fix this problem.')
        print(e)

def compute_active_passive_literature_jumbled_embeddings():
    try:
        sentences_csv_to_embedding(csvfile='../data/processed/active_passive_jumbled.tsv',
                                   save_npy='../data/processed/active_passive_jumbled_embedding.npy', truncate=None, csv_separator='\t', csv_has_line_numbers=False, header=None)
    except FileNotFoundError as e:
        print('Cannot find active passive jumbled from literature sentences .tsv file. Running jumble_sentences.py should fix this problem.')
        print(e)

def compute_active_passive_literature_jumbled_embeddings():
    try:
        sentences_csv_to_embedding(csvfile='../data/processed/active_passive_jumbled.tsv',
                                   save_npy='../data/processed/active_passive_jumbled_embedding.npy', truncate=None, csv_separator='\t', csv_has_line_numbers=False, header=None)
    except FileNotFoundError as e:
        print('Cannot find active passive jumbled from literature sentences .tsv file. Running jumble_sentences.py should fix this problem.')
        print(e)

def compute_active_passive_literature_by_added_embeddings():
    try:
        sentences_csv_to_embedding(csvfile='../data/processed/active_passive_by_added.tsv',
                                   save_npy='../data/processed/active_passive_jumbled_embedding.npy', truncate=None, csv_separator='\t', csv_has_line_numbers=False, header=None)
    except FileNotFoundError as e:
        print('Cannot find active passive jumbled from literature sentences .tsv file. Running jumble_sentences.py should fix this problem.')
        print(e)


if __name__ == '__main__':
    # compute_simple_example_embeddings()
    # compute_simple_example_jumbled_embeddings()
    # compute_active_passive_literature_embeddings()
    # compute_active_passive_literature_jumbled_embeddings()
    compute_active_passive_literature_by_added_embeddings()
