from blueprints import db
from flask_restful import fields

class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title, category, address, venue, start, end
    title = db.Column(db.String(30), nullable=False)
    event_id = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    venue = db.Column(db.String(30), nullable=True)
    start_time = db.Column(db.String(30), nullable=True)
    end_time = db.Column(db.String(30), nullable=True)

    # user_id, book_id, return_date
    response_field = {
        'id': fields.Integer,
        'title': fields.String,
        'event_id': fields.String,
        'address': fields.String,
        'venue': fields.String,
        'start_time': fields.String,
        'end_time': fields.String
    }

    def __init__(self, title, event_id, address, venue, start_time, end_time):
        self.title = title
        self.event_id = event_id
        self.address = address
        self.venue = venue
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Event %r>' % self.id