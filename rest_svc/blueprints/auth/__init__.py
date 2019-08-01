from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.client.model import Clients

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        
        args = parser.parse_args()

        ###### from database #######
        qry = Clients.query

        qry = qry.filter_by(client_key=args['client_key'])
        qry = qry.filter_by(client_secret=args['client_secret']).first()

        claim = marshal(qry, Clients.response_field)
        claim.pop("client_secret")

        if qry is not None:
            token = create_access_token(identity=args['client_key'], user_claims=claim)
        else:
            return {'status':'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        ######### for testing #####
        # if args['client_key'] == 'altarest' and args['client_secret'] == '10opwAPk3Q2D':
        #     token = create_access_token(identity=args['client_key'])
        # else:
        #     return {'status':'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        return {'token': token},200



    @jwt_required   # method need auth to run 
    def post(self):
        claims = get_jwt_claims()
        return {'claims':claims}, 200


class RefreshTokenResource(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token':token}, 200







api.add_resource(CreateTokenResource,'')
api.add_resource(RefreshTokenResource,'/refresh')