from flask import Flask
from flask.json import jsonify
from core.env import get_env
from core.logger import get_logger
from werkzeug.exceptions import HTTPException
import logging

flask_logger = logging.getLogger("werkzeug")
flask_logger.setLevel(logging.ERROR)

logger = get_logger("flask")

_server = False


def load_extensions(flask_server):
    pass


def appFactory():
    logger.debug("creating flask server")
    app = Flask(get_env("SERVICE_NAME"))
    if get_env("ENV") == "development":
        logger.debug("Debug mode is on")

    load_extensions(app)
    app.register_error_handler(Exception, exception_handler)
    return app


def startServer():
    server = getServer()
    port = get_env("PORT")
    logger.info("server is listening on port " + port)
    server.run(host="0.0.0.0", port=port, load_dotenv=False, threaded=True)
    logger.error("server shutdown")
    return server


def getServer():
    global _server
    if _server:
        return _server
    else:
        logger.warning("no server running, creating a new one")
        _server = appFactory()
        return _server


def stopServer():
    logger.error("stop server not implemented yet")


def exception_handler(e):
    """Return JSON instead of HTML for HTTP errors."""

    print(e)
    code = 500
    if hasattr(e, 'code'):
        code = e.code
    
    name = 'Server Error'
    if hasattr(e, 'name'):
        name = e.name

    description = 'Server Error'
    if hasattr(e, 'description'):
        description = e.description

    return jsonify({
        "code": code,
        "name": name,
        "message": description
    }), code