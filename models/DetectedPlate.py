from flask import Flask
import datetime
from stores.postgress import db

class DetectedPlate(db.Model):
  __tablename__ = 'detected_plates'
  id = db.Column(db.Integer, primary_key=True)
  camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'))
  frame_name = db.Column(db.String(80), nullable=False)
  license_number = db.Column(db.String(10), nullable=False)
  confidence = db.Column(db.Float(), nullable=True)
  full_alpr_json_result = db.Column(db.Text(), nullable=False)
  detected_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, camera_id):
    self.camera_id = camera_id

  def __repr__(self):
    return '<Camera %r>' % self.name

  @property
  def serialize(self):
      """Return object data in easily serializable format"""
      return {
        'id': self.id,
        'camera_id': self.camera_id,
        'frame_name': self.frame_name,
        'license_number': self.license_number,
        'confidence': self.confidence,
        'detected_at': self.detected_at,
      }