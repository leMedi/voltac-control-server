from flask import Blueprint, jsonify, request, abort, send_from_directory
from core.logger import get_logger
from core.env import get_env
from models.Camera import Camera
from stores.postgress import db
from models.Camera import Camera
from controllers.deamonController import run_alpr

logger = get_logger("CamerasController")

blueprint = Blueprint("cameras", __name__, url_prefix="/cameras")


@blueprint.route("/", methods = ['GET'])
def all():
    cameras = Camera.query.all()
    return jsonify([cam.serialize for cam in cameras])
    

@blueprint.route('/', methods = ['POST'])
def create():
    if not request.json or not 'name' in request.json:
        abort(400)

    name = request.json.get('name')
    rtsp = request.json.get('rtsp')

    print(name, rtsp)
    cam = Camera(name, rtsp)
    db.session.add(cam)
    db.session.commit()

    run_alpr()

    return jsonify({'cam': cam.serialize}), 201


@blueprint.route('/<int:id>', methods = ['GET'])
def get_by_id(id):
    camera = Camera.query.filter_by(id=id).first_or_404()
    return jsonify(camera.serialize)

@blueprint.route('/<string:name>', methods = ['GET'])
def get_by_name(id):
    camera = Camera.query.filter_by(name=name).first_or_404()
    return jsonify(camera.serialize)

@blueprint.route('/<int:id>', methods = ['DELETE'])
def delete_by_id(id):
    camera = Camera.query.filter_by(id=id).first_or_404()
    db.session.delete(camera)
    db.session.commit()

    run_alpr()

    return jsonify(camera.serialize)


@blueprint.route('/<int:id>/latest-frame', methods = ['GET'])
def latest_frame(id):
    camera = Camera.query.filter_by(id=id).first_or_404()
    directory = get_env('REAL_TIME_FRAMES_FOLDER')
    frame_name = '{}_0.jpg'.format(camera.id)
    return send_from_directory(directory, frame_name)

@blueprint.route('/<int:id>/plates', methods = ['GET'])
def plates_by_camera_id(id):
    camera = Camera.query.filter_by(id=id).first_or_404()
    return jsonify([plate.serialize for plate in camera.plates])

@blueprint.route('/frame/<string:frame_name>', methods = ['GET'])
def get_frame(frame_name):
    directory = get_env('FRAMES_FOLDER')
    return send_from_directory(directory, frame_name)


