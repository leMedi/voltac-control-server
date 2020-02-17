from flask import Blueprint, jsonify, request, abort
from core.logger import get_logger
from models.Camera import Camera
from stores.postgress import db

logger = get_logger("TodosController")

blueprint = Blueprint("cameras", __name__, url_prefix="/cameras")


@blueprint.route("/", methods = ['GET'])
def alli():
    cameras = Camera.query.all()
    return jsonify([cam.serialize for cam in cameras])
    

@blueprint.route('/', methods = ['POST'])
def create_dev():
    if not request.json or not 'name' in request.json:
        abort(400)

    name = request.json.get('name')
    rtsp = request.json.get('rtsp')

    print(name, rtsp)
    cam = Camera(name, rtsp)
    db.session.add(cam)
    db.session.commit()
    return jsonify({'cam': cam.serialize}), 201