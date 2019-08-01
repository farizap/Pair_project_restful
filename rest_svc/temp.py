# app.py
from flask import Flask, request
import json
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

## initiate flask-restful instance
api = Api(app)


## person class

class Person():
    def __init__(self):
        self.name = None
        self.age = 0
        self.sex = None

    def reset(self):
        self.name = None
        self.age = 0
        self.sex = None



@app.route('/')
def index():
    return "<h1> Hello : This main route </h1>"

@app.route('/name', methods = [ 'GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def name_controller():
    person = Person()
    if request.method == 'POST':
        data = request.get_json()
        person.name = data['name']
        person.age = data['age']
        person.sex = data['sex']
        return json.dumps(person.__dict__), 200, {'Content-Type':'application/json'}
    elif request.method == 'GET':
        return json.dumps(person.__dict__), 200, {'Content-Type':'application/json'}
    elif request.method == 'PUT':
        data = request.get_json()
        person.name = data['name']
        person.age = data['age']
        person.sex = data['sex']
        return json.dumps(person.__dict__), 200, { 'Content-Type':'application/json'}
    elif request.method == 'DELETE':
        return 'Deleted',200
    else:
        return 'Not yet implement', 501
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


