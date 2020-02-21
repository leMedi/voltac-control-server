from core.env import get_env
from core.server import startServer, getServer
from core.logger import get_logger
from core.router import load_controllers
from stores.postgress import connect
from platesReader.main import MASTER_ALPR
from models.Camera import Camera
from models.DetectedPlate import DetectedPlate
from flask_cors import CORS
import shutil
import time
from stores.postgress import db

logger = get_logger("app")


def copy_frame(camera_id, src):
    name = '{}_{}.jpg'.format(camera_id, time.time())
    dst = '{}/{}'.format(get_env('FRAMES_FOLDER'), name)
    shutil.copyfile(src, dst)
    return name

def alpr_callback(camera_id, frame_path, result, raw_result):
    server = getServer()
    frame_name = copy_frame(camera_id, frame_path)
    with server.app_context():
        plate = DetectedPlate(camera_id)
        plate.frame_name = frame_name
        plate.full_alpr_json_result = raw_result
        
        # plate.detected_at = result['epoch_time']

        plate.license_number = result['results'][0]['plate']

        
        plate.confidence = result['results'][0]['confidence']
 
        db.session.add(plate)
        db.session.commit()


def dfdf(camera_id, frame_path, result, raw_result):
    print('plate_found_callback', camera_id, frame_path, result, raw_result)

alpr = MASTER_ALPR(get_env('REAL_TIME_FRAMES_FOLDER'), alpr_callback)


def bootstrap():
    server = getServer()
    CORS(server)
    db = connect(server, get_env('DATBASE_URI'))
    load_controllers(server)

    db.create_all(app=server)
    server.debug = True

    # def dfdf():
    #     print('hello')
        
    # # with server.app_context():
    # #     cameras = Camera.query.all()
    # # #     for c in cameras:
    # # #         print(c.name)
    # #     alpr.set_cameras(cameras)
    # #     alpr.start()

    startServer()

if __name__ == "__main__":
    bootstrap()