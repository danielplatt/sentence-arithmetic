import json
from sentence_transformers import SentenceTransformer

from PCAetc.PCA_alternative import project


def projection(sentence: str) -> tuple:
    '''
    Transforms a sentence into a two-dimensional vector.
    First, a 768-dimensional embedding of the vector is computed, then this embedding
    is projected onto the two dimensional subspace of R^768 spanned by the following two vectors:
    (1) the mean of many vectors of the form A-B, where A and B are corresponding
    active voice and passive voice sentences;
    (2) the first principal component of the same vectors A-B

    :param sentence: A string containing a sentenc, such as 'The dog chases the car.'
    or 'the car is chases by The dog. ' Need not be grammatically correct or meaningful.
    :return: A two-dimensional vector
    '''
    model_str = 'all-mpnet-base-v2'
    model = SentenceTransformer(model_str)
    embedding = model.encode(sentence).tolist()
    with open('preprocessed_data/PCA_basis.json') as f:
        basis_loaded = json.load(f)
    return project(embedding, basis_loaded)


if __name__ == '__main__':
    print(projection('In cases of dispute the matter shall be resolved by the judgement of the twenty-five barons referred to below in the clause for securing the peace.'))
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.save('all-MiniLM-L6-v2_pretrained')
