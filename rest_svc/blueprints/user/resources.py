from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import internal_required
from flask_jwt_extended import jwt_required


from .model import Users
from blueprints import db, app
from sqlalchemy import desc
# 'client' penamaan (boleh diganti)
bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResource(Resource):

    @jwt_required
    @internal_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_field), 200
        return {'status':'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id',type=int, location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json',type=int, required=True)
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        user = Users(args['client_id'], args['name'], args['age'], args['sex'])

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', user )

        return marshal(user, Users.response_field), 200, {'Content-Type':'application/json'}
    
    @jwt_required
    @internal_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id',type=int, location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json',type=int, required=True)
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        qry = Users.query.get(id)

        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        qry.client_id = args['client_id']
        qry.name = args['name']
        qry.age = args['age']
        qry.sex = args['sex']
        db.session.commit()
        return marshal(qry, Users.response_field), 200, {'Content-Type':'application/json'}

    @jwt_required
    @internal_required
    def delete(self,id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status':'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status':'DELETED'}, 200

class UserList(Resource):

    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('sex',location='args', help='invalid status', choices=('male','female'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('age','sex'))
        parser.add_argument('sort',location='args',help='invalid sort', choices=('desc','asc'))

        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Users.query

        if args['sex'] is not None:
            qry = qry.filter_by(sex=args['sex'])

        if args['orderby'] is not None:
            if args['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.age))
                else:
                    qry = qry.order_by(Users.age)
            elif args['orderby'] == 'sex':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.sex))
                else:
                    qry = qry.order_by(Users.sex)

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Users.response_field))

        return result, 200, {'Content-Type':'application/json'}

api.add_resource(UserResource,'','/<id>')
api.add_resource(UserList,'/list')