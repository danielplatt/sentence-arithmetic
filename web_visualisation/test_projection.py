import numpy as np
import pandas as pd

from web_visualisation.projection import projection


def test_projection():
    preprocessed_embeddings = pd.read_csv('preprocessed_data/preprocessed_embeddings.csv', sep=',', on_bad_lines='skip').truncate(after=3)
    passive_embeddings_recomputed = preprocessed_embeddings[['passive_sentence']].truncate(after=3).apply(projection, axis=1, result_type='expand').astype('float32')

    assert np.allclose(preprocessed_embeddings[['passive_x_coord', 'passive_y_coord']].to_numpy(), passive_embeddings_recomputed.to_numpy())