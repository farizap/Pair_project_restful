from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
import datetime
from .model import Trips
from blueprints.event.model import Events
from blueprints.client.model import Clients
from blueprints import db, app, internal_required
from sqlalchemy import desc
# 'client' penamaan (boleh diganti)
bp_trips = Blueprint('trips', __name__)
api = Api(bp_trips)

from blueprints import non_internal_required
from flask_jwt_extended import jwt_required

class TripResource(Resource):

    @jwt_required
    @internal_required
    def get(self, id):
        qry = Trips.query.get(id)
        if qry is not None:
            result = marshal(qry, Trips.response_field)
            result['event'] = marshal(Events.query.get(result["event_id"]), Events.response_field)
            result['client'] = marshal(Books.query.get(result["client_id"]), Books.response_field)
            return result, 200
        return {'status':'NOT_FOUND'}, 404

    # user_id, book_id, return_date
    # @jwt_required
    # @non_internal_required
    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('user_id', location='json',type=int, required=True)
    #     parser.add_argument('book_id', location='json',type=int, required=True)
    #     args = parser.parse_args()

    #     date = datetime.date.today() + datetime.timedelta(days=3)

    #     Rent = Trips(args['user_id'],args['book_id'],date)

    #     db.session.add(Rent)
    #     db.session.commit()

    #     app.logger.debug('DEBUG : %s ', Rent )

    #     return marshal(Rent, Trips.response_field), 200, {'Content-Type':'application/json'}
    

class TripList(Resource):

    def __init__(self):
        pass

    # @jwt_required
    # @non_internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('event_id','client_id'))
        parser.add_argument('sort',location='args',help='invalid sort', choices=('desc','asc'))

        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Trips.query

        if args['orderby'] is not None:
            if args['orderby'] == 'event_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Trips.event_id))
                else:
                    qry = qry.order_by(Trips.event_id)
            elif args['orderby'] == 'client_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Trips.client_id))
                else:
                    qry = qry.order_by(Trips.client_id)

        results = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result = marshal(row, Trips.response_field)
            result['event'] = marshal(Events.query.get(result["event_id"]), Events.response_field)
            result['client'] = marshal(Clients.query.get(result["client_id"]), Clients.response_field)
            results.append(result)

        return results, 200, {'Content-Type':'application/json'}

api.add_resource(TripResource, '', '/<id>')
api.add_resource(TripList,'','/list')