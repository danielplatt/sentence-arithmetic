import json
import numpy as np
import pandas as pd
from scipy.spatial import distance
from tqdm import tqdm

from util.data_loading import get_sentence_embeddings
from PCAetc.PCA_alternative import get_differences, get_projection_vectors, project

from log import get_logger
import logging


def main():
    NUMBER_OF_EXAMPLES = 1000
    embeddings = get_sentence_embeddings('../data/processed/active_passive_embedding_full.npy') # shape=(2, -1, 768)
    embeddings = np.transpose(embeddings, (1,0,2))
    num_embeddings = embeddings.shape[0]
    sentences = pd.read_csv('../data/processed/active_passive_full_cleaned.tsv', header=None, sep='\t', on_bad_lines='skip').truncate(after=num_embeddings-1)
    assert len(sentences) == embeddings.shape[0] # number of sentences should be same as number of embeddings

    differences = get_differences(embeddings)
    basis = get_projection_vectors(differences)

    with open('preprocessed_data/PCA_basis.json', 'w') as f:
        json.dump(np.array(basis).tolist(), f)
    with open('preprocessed_data/PCA_basis.json') as f:
        basis_loaded = json.load(f)
        assert np.array_equal(np.array(basis), np.array(basis_loaded))

    projected_embeddings = [
        [
            project(emb[0], basis),
            project(emb[1], basis)
        ] for emb in embeddings
    ]
    projected_embeddings = np.reshape(projected_embeddings, (-1, 4))
    new_df = pd.concat([sentences[:NUMBER_OF_EXAMPLES], pd.DataFrame(projected_embeddings[:NUMBER_OF_EXAMPLES])], axis=1)
    new_df.columns = [
        'passive_sentence',
        'active_sentence',
        'passive_x_coord',
        'passive_y_coord',
        'active_x_coord',
        'active_y_coord'
    ]
    new_df.to_csv('app/data/embeddings.csv', index=False, sep=',')


if __name__ == '__main__':
    main()
