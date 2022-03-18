import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def get_sentence_embeddings(npy_location):
    emb = np.load(npy_location)
    try:
        assert emb.shape[2]==768
    except AssertionError:
        raise ValueError('File %s has dimension %s in second index. 768 expected.' % (npy_location, emb.shape[2]))
    emb = np.swapaxes(emb, 0, 1)
    return emb

def get_differences(emb):
    return emb[0]-emb[1]

def get_projection_vectors(vecs):
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


def main():
    emb = get_sentence_embeddings('data/simple_example_sentences_embedding.npy')#[:,:100,:]
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

    aplot = plt.scatter(*A_project, alpha=0.1)
    bplot = plt.scatter(*B_project, alpha=0.1)
    arrowplot = plt.arrow(x=0, y=0, dx=mean_diff_project[0], dy=mean_diff_project[1], width=.003, facecolor='red')

    plt.legend((aplot, bplot, arrowplot),
               ('Active sentences', 'Passive sentences', 'Average distance'),
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)
    plt.savefig('../results/img/active_passive_simple_sentences_visualisation.png')
    plt.show()

    # showing all difference vectors
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
            dx=vec_B[0]-vec_A[0],
            dy=vec_B[1]-vec_A[1],
            width=.003, facecolor='red',
        alpha=0.5)

    plt.legend((aplot, bplot, arrowplot),
               ('Active sentences', 'Passive sentences', 'Corresponding differences'),
               scatterpoints=1,
               loc='lower left',
               ncol=3,
               fontsize=8)
    plt.savefig('../results/img/active_passive_simple_sentences_individual_arrows_visualisation.png')
    plt.show()


if __name__ == '__main__':
    main()
