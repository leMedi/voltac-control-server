from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# i'sqlite:////tmp/test.db'

def connect(server, db_uri):
  global db
  server.config['SQLALCHEMY_DATABASE_URI'] = db_uri
  db.init_app(server)
  return db

def get_db():
  global db
  return db