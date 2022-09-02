from flask import jsonify
import functions_framework


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
