from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
import datetime
from .model import Trips
from blueprints.event.model import Events
from blueprints.client.model import Clients
from blueprints.user.model import Users
from blueprints.weather import PublicGetWeather
from blueprints import db, app, internal_required
from sqlalchemy import desc

# 'client' penamaan (boleh diganti)
bp_trips = Blueprint('trips', __name__)
api = Api(bp_trips)

from blueprints import non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

class InternalTripResource(Resource):

    @jwt_required
    @internal_required
    def get(self, id):
        qry = Trips.query.get(id)
        if qry is not None:
            result = marshal(qry, Trips.response_field)
            result['event'] = marshal(Events.query.get(result["event_id"]), Events.response_field)
            result['client'] = marshal(Clients.query.get(result["client_id"]), Clients.response_field)
            return result, 200
        return {'status':'NOT_FOUND'}, 404


    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', location='json',type=int, required=True)
        parser.add_argument('event_id', location='json',type=int, required=True)
        parser.add_argument('airport', location='json', required=True)
        args = parser.parse_args()

        trip = Trips(args['client_id'],args['event_id'],args['airport'])

        db.session.add(trip)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', trip )

        return marshal(trip, Trips.response_field), 200, {'Content-Type':'application/json'}
    
    @jwt_required
    @internal_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', location='json',type=int, required=True)
        parser.add_argument('event_id', location='json',type=int, required=True)
        parser.add_argument('airport', location='json', required=True)
        args = parser.parse_args()

        qry = Trips.query.get(id)

        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        qry.client_id = args['client_id']
        qry.event_id = args['event_id']
        qry.airport = args['airport']
        db.session.commit()
        return marshal(qry, Trips.response_field), 200, {'Content-Type':'application/json'}

    @jwt_required
    @internal_required
    def delete(self,id):
        qry = Trips.query.get(id)
        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status':'DELETED'}, 200


class InternalTripResourceList(Resource):

    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('filterbyclientid',location='args', help='invalid client_id',type=int)

        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Trips.query

        if args['filterbyclientid'] is not None:
            qry = qry.filter_by(id=args['filterbyclientid'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Trips.response_field))
        
        return result, 200, {'Content-Type':'application/json'}


class PublicTripList(Resource):

    def __init__(self):
        pass

    @jwt_required
    @non_internal_required
    def get(self):
        # client_id, event_id
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('filterbyid',type=int,location='args', help='invalid book id')
        parser.add_argument('filterbyclient_id',location='args', help='invalid client_id')
        parser.add_argument('filterbyevent_id',type=inputs.boolean, location='args', help='invalid event_id')

        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        qry = Trips.query

        if args['filterbyid'] is not None:
            qry = qry.filter_by(id=args['filterbyid'])

        if args['filterbyclient_id'] is not None:
            qry = qry.filter_by(client_id=args['filterbyclient_id'])

        if args['filterbyevent_id'] is not None:
            qry = qry.filter_by(event_id=args['filterbyevent_id'])


        claims = get_jwt_claims()
        
        qry = qry.filter_by(client_id=claims['id'])
        
        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            travel_id = marshal(row,Trips.response_field)['event_id']
            result.append(marshal(Events.query.get(travel_id), Events.response_field))
            # result.append(marshal(result, Trips.response_field))

            # weather_raw = PublicGetWeather().get(result[-1]['address'])
            weather_raw = PublicGetWeather().get()[0]
        
            weather_result = {}
            for weather_perday in weather_raw:
                if weather_perday["datetime"] == result[-1]['start_time']:
                    weather_result['max_temperature'] = weather_perday['max_temp']
                    weather_result['temperature'] = weather_perday['temp']
                    weather_result['min_temperature'] = weather_perday['min_temp']
                    weather_result['precipitation'] = str(weather_perday['precip']) + ' %'
                    weather_result['description'] = weather_perday['weather']['description']
                    break

            if weather_result == {}:
                weather_result = "No weather forecast"

            result[-1]['weather'] = weather_result

        
        user_qry = Users.query.filter_by(client_id = claims['id']).first()
        user_dict = marshal(user_qry, Users.response_field)

        results = {}
        results['page'] = args['p']
        results['total_page'] = len(result) // args['rp'] +1
        results['per_page'] = args['rp']
        results['client_data'] = user_dict
        results['data'] = result
        
        return results, 200, {'Content-Type':'application/json'}

api.add_resource(InternalTripResource,'/internal', '/internal/<id>')
api.add_resource(InternalTripResourceList,'/internal/list')

api.add_resource(PublicTripList,'/client')