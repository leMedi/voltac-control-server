from flask import Blueprint, jsonify, request, abort
from core.logger import get_logger
from models.Camera import Camera
from stores.postgress import db
from platesReader.main import MASTER_ALPR

logger = get_logger("DeamonController")

blueprint = Blueprint("deamon", __name__, url_prefix="/deamon")

@blueprint.route("/start", methods = ['GET'])
def start():
    run_alpr()
    return jsonify({'success': 'done'})

@blueprint.route("/stop", methods = ['GET'])
def stop():
    alpr = MASTER_ALPR.get_instance()
    alpr.stop()
    return jsonify({'success': 'done'})

def run_alpr():
    cameras = Camera.query.all()
    alpr = MASTER_ALPR.get_instance()
    alpr.reload_cameras(cameras)