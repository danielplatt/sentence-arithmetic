import numpy as np
from sklearn.decomposition import PCA


def one_set_experiment():
    print('PCA toy experiment one:')
    print('Running PCA on two-dimensional vectors whose second component is all equal')
    vecs = np.array([
        [-4,1],
        [-3,1],
        [-1,1],
        [0,1],
        [2,1],
        [5,1]
    ])
    pca = PCA()
    pca.fit(vecs)
    print('PCA components: %s' % (pca.components_,))
    print('PCA explained variance ratio: %s' % (pca.explained_variance_ratio_,))
    print('Interpretation of results: all variance is contained in the first component of the input vectors. Hence, this is the first principal component.')

def two_sets_differences_experiment():
    print('PCA toy experiment one:')
    print('Running PCA on two sets vectors which roughly differ by one constant vector')
    A = np.array([
        [-10,10],
        [-10.1,10],
        [-10.1,10.1],
        [-10,10.1]
    ])
    B = np.array([
        [10.01,10],
        [9.91,10],
        [9.91,10.1],
        [10.01,10.1]
    ])
    diff = A-B
    pca = PCA(n_components=1)
    pca.fit(diff)
    print('PCA components of difference: %s' % (pca.components_,))
    print('PCA mean of difference: %s' % (pca.mean_,))
    pca.mean_ = None # this changes the behaviour of transform! None makes it so that mean is not subtracted before transforming
    print('We only computed one principal component. Here it is: %s' % (pca.components_,))
    print('Now projecting the two sets of vectors onto the principal component.')
    A_trans = pca.transform(A)
    B_trans = pca.transform(B)
    print('The results are the following sets of 1-dimensional vectors:')
    print('First set of vectors transformed is: %s' % (A_trans,))
    print('Second set of vectors transformed is: %s' % (B_trans,))
    print('Important notice: Normally, sklearn PCA subtracts the mean of the fitted vectors before doing the projection. Notice how the output changes when removing the line pca.mean_ = None from the code! Be aware what behaviour you want!')


def main():
    one_set_experiment()
    two_sets_differences_experiment()


if __name__ == '__main__':
    main()
