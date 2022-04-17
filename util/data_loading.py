import numpy as np


def get_sentence_embeddings(npy_location):
    emb = np.load(npy_location, allow_pickle=True)
    try:
        assert emb.shape[2]==768
    except AssertionError:
        raise ValueError('File %s has dimension %s in second index. 768 expected.' % (npy_location, emb.shape[2]))
    emb = np.swapaxes(emb, 0, 1)
    return emb