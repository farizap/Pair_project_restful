from flask import Blueprint
import requests
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
import json

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)

class PublicGetWeather(Resource):
    host = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"
    token = "cdc65c0474mshfedc1ff39b67842p15df71jsn2975a55056a8"

    def get(self):
        
        param = {
            "lat" : -7.956,
            "lon" : 112.6187  
        }

        res = requests.get(self.host, params=param, headers={'X-RapidAPI-Key': self.token, 'X-RapidAPI-Host':'weatherbit-v1-mashape.p.rapidapi.com'})
        
        response = res.json()

        return response, 200, {'Content-Type':'application/json'}


api.add_resource(PublicGetWeather,'')