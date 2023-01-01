import numpy as np
import random
from scipy.spatial import distance
from tqdm import tqdm

from util.data_loading import get_sentence_embeddings

from log import get_logger
import logging

log = get_logger(__name__, with_logfile=False, level=logging.INFO)


def find_nearest_embedded_sentence_experiment(embeddings_A, embeddings_B, number_of_sentences=0, start_computation=0, end_computation=-1, zero_translation_test=False):
    # emb = get_sentence_embeddings(source)[:, :number_of_sentences, :]
    assert len(embeddings_A) == len(embeddings_B)

    # compute average diff before truncating
    n = min(len(embeddings_A), len(embeddings_B))
    diff = embeddings_B[:n]-embeddings_A[:n]
    print(f'Computing average difference vector for {len(diff)} sentence pairs')
    average_diff = np.average(diff, axis=0)
    print(f'Diff length average: {np.linalg.norm(average_diff)}')

    print(f'Average diff length: {np.average(np.linalg.norm(diff, axis=1))}')

    if zero_translation_test:
        average_diff = np.zeros(average_diff.shape)

    # now truncate
    random.seed(1)
    new_indices = random.sample(range(len(embeddings_A)), number_of_sentences)
    embeddings_A = [embeddings_A[index] for index in new_indices]
    embeddings_B = [embeddings_B[index] for index in new_indices]
    nearest_count = 0
    print(f'Now computing for how many of {len(embeddings_A)} sentences A_i+avgerage_diff is closest to B_i:')
    for k, sentence_A in tqdm(enumerate(embeddings_A), total=len(embeddings_A)):
        if k < start_computation:
            continue
        distances = [distance.cosine(sentence_A+average_diff, sentence_B) for sentence_B in embeddings_B]
        nearest_indices = np.argsort(distances)
        if k == nearest_indices[0]:
            nearest_count += 1
            print(f'{nearest_count}/{k+1} (total: {len(embeddings_A)})')
        if k == end_computation:
            break
    print('For %s/%s (%s%%) sentences A_i+avgerage_diff is closest to B_i.' % (nearest_count, len(embeddings_A), round(nearest_count/len(embeddings_A)*100, 2)))
    return nearest_count, len(embeddings_A)

def run_experiment_suite(original_sentences_npy, jumbled_sentences_npy, by_added_sentences_npy, truncate=10000):
    original_embeddings = get_sentence_embeddings(original_sentences_npy)#[:, :truncate, :]
    jumbled_embeddings = get_sentence_embeddings(jumbled_sentences_npy)#[:, :truncate, :]
    by_added_embeddings = get_sentence_embeddings(by_added_sentences_npy)  # [:, :truncate, :]

    #print('Experiment 1: Original passive-Original active')
    #find_nearest_embedded_sentence_experiment(original_embeddings[0], original_embeddings[1], number_of_sentences=truncate, zero_translation_test=False)
    #print('------------------')
    #print('Experiment 2: Original passive-Jumbled active')
    #find_nearest_embedded_sentence_experiment(original_embeddings[0], jumbled_embeddings[1], number_of_sentences=truncate)
    #print('------------------')
    #print('Experiment 3: Original passive-Jumbled passive')
    #find_nearest_embedded_sentence_experiment(original_embeddings[0], jumbled_embeddings[0], number_of_sentences=truncate)
    #print('------------------')
    print('Experiment 4: Original active-by added to active')
    find_nearest_embedded_sentence_experiment(by_added_embeddings[0], by_added_embeddings[1], number_of_sentences=truncate)
    print('------------------')
    #print('Experiment 5: Original active-by added to active... Zero translation vector')
    #find_nearest_embedded_sentence_experiment(by_added_embeddings[0], by_added_embeddings[1], number_of_sentences=truncate, zero_translation_test=True)


if __name__ == '__main__':
    run_experiment_suite(
        '../data/processed/active_passive_embedding_full.npy',
        '../data/processed/active_passive_jumbled_embedding.npy',
        #'../data/processed/active_passive_by_added_embedding.npy',
        '../data/processed/active_passive_by_added_embedding.npy',
        truncate=100000
    )

 # 1...1000: 999/1000