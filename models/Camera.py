from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from stores.postgress import db

class Camera(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  rtsp = db.Column(db.String(500), nullable=False)
  is_active = db.Column(db.Boolean(), unique=False, default=True)

  def __init__(self, name, rtsp):
    self.name = name
    self.rtsp = rtsp

  def __repr__(self):
    return '<Camera %r>' % self.name

  @property
  def serialize(self):
      """Return object data in easily serializable format"""
      return {
          'id': self.id,
          'name': self.name,
          'rtsp': self.rtsp,
          'is_active': self.is_active,
      }