from flask import jsonify, make_response


def json_response(response, status_code=200, headers={}):
    response = jsonify(response)
    resp = make_response(
        response, status_code
    )  # here you could use make_response(render_template(...)) too
    resp.headers["Content-Type"] = "application/json"
    return resp
