from core.env import get_env
from core.server import startServer, getServer
from core.logger import get_logger
from core.router import load_controllers
from stores.postgress import connect
logger = get_logger("app")

def bootstrap():
    server = getServer()

    db = connect(server, get_env('DATBASE_URI'))
    load_controllers(server)

    db.create_all(app=server)
    server.debug = True
    startServer()

if __name__ == "__main__":
    bootstrap()