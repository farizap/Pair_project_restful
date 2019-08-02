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

    geo_host = 'https://maps.googleapis.com/maps/api/geocode'
    geo_apikey = 'AIzaSyAWTZoMYFhUhy-g1et0QZiD4JQAAqYsoXY'


    # def get(self, address):
    def get(self):

        # rq_geo = requests.get(self.geo_host + '/json?', params={'address': address, 'key': self.geo_apikey})
        # geo = rq_geo.json()
        # lat = geo['results'][0]['geometry']['location']['lat']
        # lon = geo['results'][0]['geometry']['location']['lng']

        # param = {
        #     "lat" : lat,
        #     "lon" : lon  
        # }

        param = {
            "lat" : -7,
            "lon" : 122  
        }

        res = requests.get(self.host, params=param, headers={'X-RapidAPI-Key': self.token, 'X-RapidAPI-Host':'weatherbit-v1-mashape.p.rapidapi.com'})
        
        response = res.json()['data']



        return response, 200, {'Content-Type':'application/json'}


# api.add_resource(PublicGetWeather,'/<address>')
api.add_resource(PublicGetWeather,'')