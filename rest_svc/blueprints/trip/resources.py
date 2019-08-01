from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
import datetime
from .model import Trips
from blueprints.event.model import Events
from blueprints.client.model import Clients
from blueprints.user.model import Users
from blueprints import db, app, internal_required
from sqlalchemy import desc

# 'client' penamaan (boleh diganti)
bp_trips = Blueprint('trips', __name__)
api = Api(bp_trips)

from blueprints import non_internal_required
from flask_jwt_extended import jwt_required

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
        args = parser.parse_args()

        Rent = Trips(args['client_id'],args['event_id'],date)

        db.session.add(Rent)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', Rent )

        return marshal(Rent, Trips.response_field), 200, {'Content-Type':'application/json'}
    
    @jwt_required
    @internal_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', location='json',type=int, required=True)
        parser.add_argument('event_id', location='json',type=int, required=True)
        args = parser.parse_args()

        qry = Trips.query.get(id)

        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        qry.client_id = args['client_id']
        qry.event_id = args['event_id']
        qry.status = args['status']
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
            result['user'] = marshal(Users.query.get(result["client_id"]), Users.response_field)
            result['book'] = marshal(Events.query.get(result["event_id"]), Events.response_field)
            result.append(marshal(result, Trips.response_field))
        
        results = {}
        results['page'] = args['p']
        results['total_page'] = len(result) // args['rp'] +1
        results['per_page'] = args['rp']
        results['client_id'] = claims['id']
        results['data'] = result
        
        return results, 200, {'Content-Type':'application/json'}

api.add_resource(InternalTripResource, '/internal/<id>')
api.add_resource(PublicTripList,'/public')