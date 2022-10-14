from flask import jsonify
from flask_cors import cross_origin
import functions_framework
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os
from os import path


# TODO needs to be stricter once frontend URL is known
@cross_origin(allowed_methods=["POST"])
@functions_framework.http
def classify_http(request):
    request_json = request.get_json(silent=True)

    active = request_json["active"]
    active_position = classify(active)

    passive = request_json["passive"]
    passive_position = classify(passive)

    return jsonify({
        "active": active_position,
        "passive": passive_position
    })


def project_linear_algebra(vec, basis):
    '''
    :param vec: A vector of dimension n
    :param basis: Two vectos of dimension n
    :return: A 2-dimensional vector
    '''
    return np.inner(vec, basis[0]), np.inner(vec, basis[1])

def classify(sentence: str) -> dict:
    '''
    Transforms a sentence into a two-dimensional vector.
    First, a 768-dimensional embedding of the vector is computed, then this embedding
    is projected onto the two dimensional subspace of R^768 spanned by the following two vectors:
    (1) the mean of many vectors of the form A-B, where A and B are corresponding
    active voice and passive voice sentences;
    (2) the first principal component of the same vectors A-B

    :param sentence: A string containing a sentence, such as 'The dog chases the car.'
    or 'the car is chases by The dog. ' Need not be grammatically correct or meaningful.
    :return: A two-dimensional vector stored as a dictionary {"x": 0.562397, "y": -0.245144}.
    '''
    model_path = path.join(path.dirname(path.abspath(__file__)), 'all-MiniLM-L6-v2_pretrained')
    model = SentenceTransformer(model_path) # loading model from pretrained_model directory.
    # models can be saved using model.save(model_path)
    embedding = model.encode(sentence).tolist()

    json_basis_path = path.join(path.dirname(path.abspath(__file__)), 'preprocessed_data/PCA_basis_all-MiniLM-L6-v2.json')
    with open(json_basis_path) as f:
        basis_loaded = json.load(f)

    projected_vector = project_linear_algebra(embedding, basis_loaded)
    return {
        "x": projected_vector[0],
        "y": projected_vector[1],
    }


# if __name__ == '__main__':
#     print(classify('The dog chases the car.'))
