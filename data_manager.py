import flask
from flasgger import Swagger
from flask import Flask, request, make_response, jsonify

from bc import *
from database_manager import *

demo_database_manager = DemoDatabaseManager()

app = Flask(__name__)

app.config['SWAGGER'] = {
    'doc_dir': 'common/data_structure/apidocs'
}
swagger = Swagger(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def landing_page():
    return "Hello, welcome to our topic proposal"

@app.route('/status')
def system_status():
    return {'status': 'OK'}

@app.route('/demo', methods=['POST'])
def demo():
    signer = request.args.get('signer', 'To Duc Anh')
    data = request.args.get('data', 'This is a blank block')
    try:
        respond = demo_database_manager.insert_data(data, signer)
        return make_response(jsonify(respond), 200)
    except pymongo.errors.OperationFailure as e:
        return make_response(jsonify(e), 500)


@app.route('/add_employee', methods=['POST'])
def add_employee():
    entry = request.json
    # Adding method goes here
    return {'result': 'Successfully added employee to the database'}


@app.route('/add_customer', methods=['POST'])
def add_customer():
    entry = request.json
    # Adding method goes here
    return {'result': 'Successfully added customer to the database'}


@app.route('/add_good', methods=['POST'])
def add_good():
    entry = request.json
    # Adding method goes here
    return {'result': 'Successfully added good to the database'}


@app.route('/get_good', methods=['GET'])
def get_good():
    entry = request.json
    # Adding method goes here
    return {'result': 'Successfully got good information from databases'}

if __name__ == '__main__':
    app.run(port=8088)
