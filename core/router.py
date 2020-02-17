import pkgutil
import controllers
from core.logger import get_logger

logger = get_logger("router")


def get_controllers():
    _controllers = []
    for importer, modname, ispkg in pkgutil.iter_modules(controllers.__path__):
        controller = __import__("controllers." + modname, fromlist=".")
        _controllers.append(controller)
    return _controllers


def register_blueprints(flask_server, controllers):
    for controller in controllers:
        flask_server.register_blueprint(controller.blueprint)
        logger.debug("{} loaded".format(controller.__name__))


def load_controllers(flask_server):
    controllers = get_controllers()
    register_blueprints(flask_server, controllers)
