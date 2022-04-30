import json
from sentence_transformers import SentenceTransformer

from PCAetc.PCA_alternative import project


def projection(sentence: str) -> tuple:
    model_str = 'all-mpnet-base-v2'
    model = SentenceTransformer(model_str)
    embedding = model.encode(sentence).tolist()
    with open('preprocessed_data/PCA_basis.json') as f:
        basis_loaded = json.load(f)
    return project(embedding, basis_loaded)


if __name__ == '__main__':
    print(projection('In cases of dispute the matter shall be resolved by the judgement of the twenty-five barons referred to below in the clause for securing the peace.'))
