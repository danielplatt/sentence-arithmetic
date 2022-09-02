from flask import jsonify
from flask_cors import cross_origin
import functions_framework


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


def classify(sentence):
    # TODO Daniel: Implement function
    return {
        "x": len(sentence),
        "y": len(sentence),
    }
