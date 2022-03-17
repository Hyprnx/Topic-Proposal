from flasgger import Swagger
from flask import Flask, request


app = Flask(__name__)
app.config['SWAGGER'] = {
    'doc_dir': 'data_structure/apidocs'
}
swagger = Swagger(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/status')
def system_status():
    return {'status': 'OK'}

@app.route('/test')
def test():
    entry = request.json
    return {'result': entry}



if __name__ == '__main__':
    app.run(port=8088)
