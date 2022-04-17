import numpy as np
from scipy.spatial import distance
from tqdm import tqdm

from util.data_loading import get_sentence_embeddings

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)


def find_nearest_embedded_sentence_experiment(embeddings_A, embeddings_B, number_of_sentences=0):
    # emb = get_sentence_embeddings(source)[:, :number_of_sentences, :]
    assert len(embeddings_A) == len(embeddings_B)
    embeddings_A = embeddings_A[:number_of_sentences]
    embeddings_B = embeddings_B[:number_of_sentences]
    diff = embeddings_A-embeddings_B
    average_diff = np.average(diff, axis=0)
    nearest_count = 0
    print('Now computing for how many sentences A_i+avgerage_diff is closest to B_i:')
    for k, sentence_A in tqdm(enumerate(embeddings_A), total=len(embeddings_A)):
        distances = [distance.cosine(sentence_A, sentence_B) for sentence_B in embeddings_B]
        nearest_indices = np.argsort(distances)
        if k == nearest_indices[0]:
            nearest_count += 1
    print('For %s/%s (%s%%) sentences A_i+avgerage_diff is closest to B_i.' % (nearest_count, len(embeddings_A), round(nearest_count/len(embeddings_A)*100, 2)))
    return nearest_count, len(embeddings_A)

def main():
    original_embeddings = get_sentence_embeddings('../data/processed/active_passive_embedding.npy')[:,:100,:]
    jumbled_embeddings = get_sentence_embeddings('../data/processed/active_passive_jumbled_embedding.npy')[:,:100,:]

    find_nearest_embedded_sentence_experiment(original_embeddings[0], original_embeddings[1], number_of_sentences=100)
    print('------------------')
    find_nearest_embedded_sentence_experiment(original_embeddings[0], jumbled_embeddings[1], number_of_sentences=100)
    print('------------------')
    find_nearest_embedded_sentence_experiment(original_embeddings[0], jumbled_embeddings[0], number_of_sentences=100)



if __name__ == '__main__':
    main()