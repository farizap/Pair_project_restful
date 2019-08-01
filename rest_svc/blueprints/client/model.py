from blueprints import db
from flask_restful import fields


class Clients(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(30), nullable=True)
    status = db.Column(db.Boolean, nullable=True, default=False)
    
    response_field = {
        'id': fields.Integer,
        'client_key': fields.String,
        'client_secret': fields.String,
        'status': fields.Boolean
    }

    def __init__(self, client_key,client_secret, status):
        self.client_key = client_key
        self.client_secret = client_secret
        self.status = status

    def __repr__(self):
        return '<Client %r>' % self.id