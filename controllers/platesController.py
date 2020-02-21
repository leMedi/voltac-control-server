from flask import Blueprint, jsonify, request, abort
from core.logger import get_logger
from core.env import get_env
from models.DetectedPlate import DetectedPlate
from stores.postgress import db

logger = get_logger("PlatesController")

blueprint = Blueprint("plates", __name__, url_prefix="/plates")


@blueprint.route("/", methods = ['GET'])
def all():
    plates = DetectedPlate.query.all()
    return jsonify([plate.serialize for plate in plates])
    
@blueprint.route('/<int:id>', methods = ['GET'])
def get_by_id(id):
    plate = DetectedPlate.query.filter_by(id=id).first_or_404()
    return jsonify(plate.serialize)