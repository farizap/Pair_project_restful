from flask import Blueprint
import requests
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
import json

bp_hqpredict = Blueprint('hqpredict', __name__)
api = Api(bp_hqpredict)

class PublicGetHQPredict(Resource):
    host = "https://api.predicthq.com/v1/events/"
    token = "e6KsG50OLWLBog4ZyTXTpu1OMKCUgS"

    def get(self):
        # country = "ID"
        # startdate = "2019-08-01"
        # enddate = "2019-09- 15"
        # activetimezone = "Asia/Jakarta"

        parser = reqparse.RequestParser()
        parser.add_argument('startdate', location='args',default="2019-08-01")
        parser.add_argument('enddate', location='args',default='2019-09-15')
        parser.add_argument('category', location='args',default=None)
        parser.add_argument('search', location='args', default=None)
        args = parser.parse_args()

        # airport-delays, community, concerts, conferences, daylight-savings, disasters, expos, festivals,
        # observances, performing-arts, politics, public-holidays, school-holidays, severe-weather, 
        # sports, terror 


        param = {
            "country" : "ID",
            "active.gte" : args['startdate'],
            "active.lte" : args['enddate'],
            "active.tz" : "Asia/Jakarta",
            "sort" : "rank"  
        }

        if args['category'] is not None:
            param['category'] = args['category']

        if args['search'] is not None:
            param['search'] = args['search']

        res = requests.get(self.host, params=param, headers={'Authorization': 'Bearer ' + self.token})
        
        response = res.json()

        return response, 200, {'Content-Type':'application/json'}

class UserGetHQPredict(Resource):
    host = "https://api.predicthq.com/v1/events/"
    token = "e6KsG50OLWLBog4ZyTXTpu1OMKCUgS"

    def get(self):
        # country = "ID"
        # startdate = "2019-08-01"
        # enddate = "2019-09- 15"
        # activetimezone = "Asia/Jakarta"

        parser = reqparse.RequestParser()
        parser.add_argument('startdate', location='args',default="2019-08-01")
        parser.add_argument('enddate', location='args',default='2019-09-15')
        parser.add_argument('category', location='args',default='concerts')
        parser.add_argument('search', location='args', default=None, required=True)
        args = parser.parse_args()

        # airport-delays, community, concerts, conferences, daylight-savings, disasters, expos, festivals,
        # observances, performing-arts, politics, public-holidays, school-holidays, severe-weather, 
        # sports, terror 


        param = {
            "country" : "ID",
            "active.gte" : args['startdate'],
            "active.lte" : args['enddate'],
            "active.tz" : "Asia/Jakarta",
            "sort" : "rank"  
        }

        if args['category'] is not None:
            param['category'] = args['category']

        if args['search'] is not None:
            param['search'] = args['search']

        res = requests.get(self.host, params=param, headers={'Authorization': 'Bearer ' + self.token})
        
        response = res.json()

        return response, 200, {'Content-Type':'application/json'}


api.add_resource(PublicGetHQPredict,'','')