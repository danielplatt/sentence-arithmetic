import json
import numpy as np
import os
import pandas as pd
import random
from scipy.spatial import distance
from tqdm import tqdm

from util.data_loading import get_sentence_embeddings
from PCAetc.PCA_alternative import get_differences, get_projection_vectors, project

from log import get_logger
import logging


def main():
    NUMBER_OF_EXAMPLES = 200
    embeddings = get_sentence_embeddings('../data/processed/active_passive_embedding_full.npy') # shape=(2, -1, 768)
    embeddings = np.transpose(embeddings, (0,2,1))
    transposed_embeddings = np.transpose(embeddings, (2, 0, 1))
    num_embeddings = embeddings.shape[1]
    sentences = pd.read_csv('../data/processed/active_passive_full_cleaned.tsv', header=None, sep='\t', on_bad_lines='skip').truncate(after=num_embeddings-1)
    assert len(sentences) == embeddings.shape[1] # number of sentences should be same as number of embeddings

    differences = get_differences(embeddings)
    print(f'Embeddings shape: {embeddings.shape}')
    transposed_differences = np.transpose(differences, (1,0))

    # truncate
    new_indices = random.sample(range(len(transposed_differences)), NUMBER_OF_EXAMPLES)
    transposed_differences = [transposed_differences[index] for index in new_indices]
    transposed_embeddings = [transposed_embeddings[index] for index in new_indices]
    sentences = [sentences[index] for index in new_indices]

    basis = get_projection_vectors(transposed_differences)

    test_vec = np.zeros(384)
    test_vec[0] = 1

    with open('preprocessed_data/PCA_basis.json', 'w') as f:
        json.dump(np.array(basis).tolist(), f)
    with open('preprocessed_data/PCA_basis.json') as f:
        basis_loaded = json.load(f)
        assert np.array_equal(np.array(basis), np.array(basis_loaded))


    projected_embeddings = [
        [
            project(emb[0], basis),
            project(emb[1], basis)
        ] for emb in transposed_embeddings
    ]
    projected_embeddings = np.reshape(projected_embeddings, (-1, 4))
    new_df = pd.concat([sentences, pd.DataFrame(projected_embeddings)], axis=1)
    new_df.columns = [
        'passive_sentence',
        'active_sentence',
        'passive_x_coord',
        'passive_y_coord',
        'active_x_coord',
        'active_y_coord'
    ]
    dirpath = os.path.dirname(os.path.realpath(__file__))
    out_path = os.path.join(dirpath, '../docs/data/embeddings.csv')
    new_df.to_csv(out_path, index=False, sep=',')


if __name__ == '__main__':
    main()
