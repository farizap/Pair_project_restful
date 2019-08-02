from flask import Flask, request
import json

##database import###
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import Manager

##JWT import
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta

#wrap
from functools import wraps


app = Flask(__name__)
app.config['APP_DEBUG'] = True

#################
# JWT
###############

app.config['JWT_SECRET_KEY'] = 'Sfasdlah8xPnS73nS3dhb'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# jwt custom decorator
# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     ## sebelum return get client
#     return identity
    
def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:
            return {'status':'FORBIDDEN', 'message':'Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def non_internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status']:
            return {'status':'FORBIDDEN', 'message':'Non Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


####Database####


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://alta123:h@localhost:3306/pair_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fikriamri:threecheers@localhost:3306/pair_project'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # command 'db' dapat menjalankan semua command MigrateCommand

###########Middleware#############
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    app.logger.warning("REQUEST_LOG\t%s", 
        json.dumps({
            'uri':request.full_path,
            'code':response.status,
            'method':request.method,
            'request':requestData,
            'response':json.loads(response.data.decode('utf-8'))}))

    return response

###############################
# Import blueprints
###############################
# from blueprints.person.resources import bp_person
from blueprints.client.resources import bp_client
from blueprints.user.resources import bp_user
# from blueprints.book.resources import bp_books
from blueprints.auth import bp_auth
# from blueprints.weather.resources import bp_weather
# from blueprints.rent.resources import bp_rent
from blueprints.hqpredict.resources import bp_hqpredict
from blueprints.trip.resources import bp_trips
from blueprints.airport.resources import bp_airport
from blueprints.event.resources import bp_event
from blueprints.weather import bp_weather

# app.register_blueprint(bp_person, url_prefix='/person')
app.register_blueprint(bp_client, url_prefix='/client' )
# app.register_blueprint(bp_books, url_prefix='/books' )
app.register_blueprint(bp_user, url_prefix='/user' )
app.register_blueprint(bp_auth, url_prefix='/token')
app.register_blueprint(bp_weather, url_prefix='/weather')
# app.register_blueprint(bp_rent, url_prefix='/rent')
app.register_blueprint(bp_hqpredict, url_prefix='')
app.register_blueprint(bp_trips, url_prefix='/trip')
app.register_blueprint(bp_airport, url_prefix='/airport')
app.register_blueprint(bp_event, url_prefix='')

db.create_all()