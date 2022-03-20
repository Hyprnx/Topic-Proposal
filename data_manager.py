from flasgger import Swagger
from flask import Flask, request
from bc import *

app = Flask(__name__)

app.config['SWAGGER'] = {
    'doc_dir': 'data_structure/apidocs'
}
swagger = Swagger(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def landing_page():
    return "Hello, welcome to our topic proposal"

@app.route('/status')
def system_status():
    return {'status': 'OK'}

@app.route('/test')
def demo():
    entry = request.json
    node = Node('0', entry, index=2)
    if len(node.hash()) == 64:
        return {
            "result": node.get_block(),
            "hash": node.hash()
            }


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
