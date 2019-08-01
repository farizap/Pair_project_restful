from blueprints import db
from flask_restful import fields

class Trips(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    airport = db.Column(db.String(100), nullable=True)

    # client_id, event_id
    response_field = {
        'id': fields.Integer,
        'client_id': fields.Integer,
        'event_id': fields.Integer,
        'airport':fields.String
    }

    def __init__(self, client_id, event_id, airport):
        self.client_id = client_id
        self.event_id = event_id
        self.airport = airport

    def __repr__(self):
        return '<Trips %r>' % self.id

