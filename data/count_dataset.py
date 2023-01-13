import numpy as np
import pandas as pd

from util.data_loading import get_sentence_embeddings

def count_dataset():
    original_embeddings = get_sentence_embeddings('../data/processed/active_passive_embedding_full.npy')
    print(original_embeddings.shape)

    results = pd.read_csv('processed/active_passive_full_cleaned.tsv', sep='\t')
    print(len(results))


if __name__ == '__main__':
    count_dataset()