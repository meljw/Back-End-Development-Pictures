import json
import os

from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

from . import app

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


def find_picture_by_id(id):
    return next((p for p in data if p.get("id") == id), None)


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = find_picture_by_id(id)
    if picture is None:
        return {"message": f"picture with id {id} not found"}, 404
    else:
        return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    body = request.get_json()
    picture_id = body.get("id")
    picture = find_picture_by_id(picture_id)
    if picture is not None:
        return {"Message": f"picture with id {picture_id} already present"}, 302

    data.append(body)
    return jsonify(body), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    body = request.get_json()
    picture = find_picture_by_id(id)
    if picture is None:
        return {"message": f"picture with id {id} not found"}, 404
    else:
        data[data.index(picture)] = body
        return jsonify(body), 200


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = find_picture_by_id(id)
    if picture is None:
        return {"message": f"picture with id {id} not found"}, 404
    else:
        data.remove(picture)
        return "", 204
