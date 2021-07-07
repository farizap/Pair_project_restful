from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from .model import Events
from blueprints import db, app
from sqlalchemy import desc

from blueprints import internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

from blueprints.hqpredict.resources import UserGetHQPredict
from blueprints.trip.resources import Trips
from blueprints.airport.resources import GetNearestAirport
from blueprints.weather import PublicGetWeather

# 'client' penamaan (boleh diganti)
bp_event = Blueprint('event', __name__)
api = Api(bp_event)

class EventUserResource(Resource):
    host = "https://api.predicthq.com/v1/events/"
    token = "e6KsG50OLWLBog4ZyTXTpu1OMKCUgS"
    
    @jwt_required
    # @non_internal_required
    def get(self):

        raw = UserGetHQPredict().get()
        # return raw
        title = raw[0]['results'][0]['title']
        event_id = raw[0]['results'][0]['id']
        address = raw[0]['results'][0]['entities'][0]["formatted_address"]
        venue = raw[0]['results'][0]['entities'][0]["name"]
        start_time = raw[0]['results'][0]['start'][:10]
        end_time = raw[0]['results'][0]['end'][:10]

        event = Events.query.filter_by(event_id=event_id).first()
        claim = get_jwt_claims()
        if event is None:
            event = Events(title, event_id, address, venue, start_time, end_time)
            db.session.add(event)
            db.session.commit()
        event = marshal(event, Events.response_field)

        air = GetNearestAirport().get(address)


        trip = Trips(claim['id'], event['id'], air['airport_name'])
        db.session.add(trip)
        db.session.commit()

        return event, 200, {'Content-Type':'application/json'}
    
    # @jwt_required
    # @internal_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status',type=inputs.boolean, location='json')
        args = parser.parse_args()

        qry = Clients.query.get(id)

        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        qry.client_key = args['client_key']
        qry.client_secret = args['client_secret']
        qry.status = args['status']
        db.session.commit()
        return marshal(qry, Clients.response_field), 200, {'Content-Type':'application/json'}

    # @jwt_required
    # @internal_required
    def delete(self,id):
        qry = Clients.query.get(id)
        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status':'DELETED'}, 200




api.add_resource(EventUserResource, '/user/event')

# api.add_resource(ClientList,'','/list')