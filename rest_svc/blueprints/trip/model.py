from blueprints import db
from flask_restful import fields

class Trips(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    # client_id, event_id
    response_field = {
        'id': fields.Integer,
        'client_id': fields.Integer,
        'event_id': fields.Integer,
    }

    def __init__(self, client_id, event_id):
        self.client_id = client_id
        self.event_id = event_id

    def __repr__(self):
        return '<Trips %r>' % self.id

