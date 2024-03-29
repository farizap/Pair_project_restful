
import json


app = Flask(__name__)

## initiate flask-restful instance
api = Api(app)

from blueprints.person.resources import bp_person

app.register_blueprint(bp_person, url_prefix='/person')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
