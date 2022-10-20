import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from util.data_loading import get_sentence_embeddings


def get_differences(emb):
    return emb[0]-emb[1]

def get_projection_vectors(vecs):
    print(vecs.shape)
    mean = np.mean(vecs, axis=0)
    pca = PCA()
    pca.fit(vecs)
    basis1 = mean
    basis2 = pca.components_[0]
    return basis1, basis2

def project(vec, basis):
    '''
    :param vec: A vector of dimension n
    :param basis: Two vectos of dimension n
    :return: A 2-dimensional vector
    '''
    return np.inner(vec, basis[0]), np.inner(vec, basis[1])

def plot_active_passive(A_project, B_project, mean_diff_project, filename='../results/img/active_passive_simple_sentences_visualisation.png'):
    aplot = plt.scatter(*A_project, alpha=0.1)
    bplot = plt.scatter(*B_project, alpha=0.1)
    arrowplot = plt.arrow(x=0, y=0, dx=mean_diff_project[0], dy=mean_diff_project[1], width=.003, facecolor='red')

    plt.legend((aplot, bplot, arrowplot),
               ('Active sentences', 'Passive sentences', 'Average distance'),
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)
    plt.savefig(filename)
    plt.show()

def plot_active_passive_with_difference_vectors(A_project, B_project, filename='../results/img/active_passive_simple_sentences_individual_arrows_visualisation.png'):
    max_number_of_difference_vectors = 40
    aplot = plt.scatter(*A_project, alpha=0.1)
    bplot = plt.scatter(*B_project, alpha=0.1)
    A_project = np.swapaxes(A_project, 0, 1)
    B_project = np.swapaxes(B_project, 0, 1)
    for k, (vec_A, vec_B) in enumerate(zip(A_project, B_project)):
        if k >= max_number_of_difference_vectors:
            break
        arrowplot = plt.arrow(
            x=vec_A[0],
            y=vec_A[1],
            dx=vec_B[0] - vec_A[0],
            dy=vec_B[1] - vec_A[1],
            width=.003, facecolor='red',
            alpha=0.5)

    plt.legend((aplot, bplot, arrowplot),
               ('Active sentences', 'Passive sentences', 'Corresponding differences'),
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)
    plt.savefig(filename)
    plt.show()

def main():
    # emb = get_sentence_embeddings('data/simple_example_sentences_embedding.npy')#[:,:10000,:]
    emb = get_sentence_embeddings('../data/processed/active_passive_embedding_full.npy')[:, :1000, :]

    diff = get_differences(emb)
    basis = get_projection_vectors(diff)
    A_project = np.swapaxes(np.array([
        project(vec, basis) for vec in emb[0]
    ]), 0, 1)
    B_project = np.swapaxes(np.array([
        project(vec, basis) for vec in emb[1]
    ]), 0, 1)
    mean_diff = np.mean(diff, axis=0)
    mean_diff_project = np.array(project(mean_diff, basis))

    plot_active_passive(A_project, B_project, mean_diff_project, filename='../results/img/active_passive_real_life_sentences_visualisation.png')
    plot_active_passive_with_difference_vectors(A_project, B_project, filename='../results/img/active_passive_real_life_sentences_individual_arrows_visualisation.png')


if __name__ == '__main__':
    main()
