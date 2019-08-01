from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from .model import Clients
from blueprints import db, app
from sqlalchemy import desc

from blueprints import internal_required
from flask_jwt_extended import jwt_required


# 'client' penamaan (boleh diganti)
bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    # @jwt_required
    def get(self, id):
        qry = Clients.query.get(id)
        if qry is not None:
            return marshal(qry, Clients.response_field), 200
        return {'status':'NOT_FOUND'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status',type=inputs.boolean, location='json')
        args = parser.parse_args()

        client = Clients(args['client_key'], args['client_secret'], args['status'])

        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', client )

        return marshal(client, Clients.response_field), 200, {'Content-Type':'application/json'}
    
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

class ClientList(Resource):

    def __init__(self):
        pass

    # @jwt_required
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('filterbyclientid',location='args', help='invalid client_id',type=int)
        parser.add_argument('filterbystatus',location='args', type=inputs.boolean, help='invalid status', choices=(True,False))

        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Clients.query

        if args['filterbystatus'] is not None:
            qry = qry.filter_by(status=args['filterbystatus'])

        if args['filterbyclientid'] is not None:
            qry = qry.filter_by(id=args['filterbyclientid'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Clients.response_field))
        
        return result, 200, {'Content-Type':'application/json'}


api.add_resource(ClientResource, '', '/<id>')
api.add_resource(ClientList,'','/list')