from flask import Blueprint
from flask_restful import Resource, reqparse, Api
import requests, json
from flask_jwt_extended import jwt_required

bp_airport = Blueprint('airport', __name__)
api = Api(bp_airport)

class GetNearestAirport(Resource):
    geo_host = 'https://maps.googleapis.com/maps/api/geocode'
    geo_apikey = 'AIzaSyAWTZoMYFhUhy-g1et0QZiD4JQAAqYsoXY'

    air_rapid = 'default-application_3852324'
    air_host = 'https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/by-radius'
    air_apikey = 'd9590fce09mshc40938b919d0b1dp177c42jsndc25170e133b'

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', location='args', default=None)
        args = parser.parse_args()

        rq_geo = requests.get(self.geo_host + '/json?', params={'address': args['address'], 'key': self.geo_apikey})
        geo = rq_geo.json()
        lat = geo['results'][0]['geometry']['location']['lat']
        lon = geo['results'][0]['geometry']['location']['lng']

        radius = 50
        rq_air = []
        while rq_air == []:
            rq_air = requests.get(self.air_host, params={'radius':radius, 'lng': lon, 'lat': lat}, headers={"x-rapidapi-host": "cometari-airportsfinder-v1.p.rapidapi.com", "x-rapidapi-key": "d9590fce09mshc40938b919d0b1dp177c42jsndc25170e133b"}).json()
            radius += 10

        return {
            'airport_code': rq_air[0]['code'],
            'airport_name': rq_air[0]['name'],
            'radius': radius
        }

api.add_resource(GetNearestAirport, '')


