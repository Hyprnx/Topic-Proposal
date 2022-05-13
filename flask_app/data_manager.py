import flask
from flasgger import Swagger
from flask import Flask, request, make_response, jsonify, render_template, redirect, session
from forms import *

import re

from bc import *
from database_manager import *
from customers_db_manager import CustomerDatabaseManager
from employee_manager import EmployeeDatabaseManager

from credentials.secret_keys import key


demo_database_manager = DemoBlockChainManager()
customer_database_manager = CustomerDatabaseManager()
employee_database_manager = EmployeeDatabaseManager()

app = Flask(__name__, template_folder='templates')
app.secret_key = key

app.config['SWAGGER'] = {
    'doc_dir': 'common/data_structure/apidocs'
}
swagger = Swagger(app)


@app.route('/')
def landing_page():
    return redirect('/home', code=302)


@app.route('/home')
def home():
    return render_template('pages/home.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['confirm']
        app.logger.info(f'{username}, {password}, {email}')

        if password_confirmation != password:
            return render_template('errors/400.html', mess='Your credential does not match, please try again!')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return render_template('errors/400.html', mess='Invalid email address, please try again!')

        if customer_database_manager.check_customer_exist(email):
            return render_template('errors/400.html', mess='Customer exited, please try again!')

        res = customer_database_manager.register_customers(name=username, email=email, password=password)
        if res:
            return render_template('success/success_register.html')

    return render_template('forms/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        employee_info = employee_database_manager.check_employee_exist(email, password)
        if employee_info:
            app.logger.info(employee_info)
            session['email'] = employee_info['email']
            session['username'] = employee_info['username']
            app.logger.info('Logged in successfully !')
            session['loggedin'] = True
            return render_template('success/success_login.html', mess=f'Welcome back, {employee_info["username"]}')
        else:
            return render_template('errors/400.html', mess='Wrong Credential')
    return render_template('forms/login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect('/home', code=302)


@app.route('/forgot', methods=['POST'])
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/validation')
def validation():
    return {'status': 'OK'}


@app.route('/status')
def system_status():
    return {'status': 'OK'}


@app.route('/demo', methods=['POST'])
def demo():
    signer = request.args.get('signer', 'To Duc Anh')
    data = request.args.get('data', 'This is a blank block')
    try:
        respond = demo_database_manager.insert_block(data, signer)
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
    app.run(host='0.0.0.0', port=13030, debug=True) # Everyone within the same network can use
    # app.run(port=13030) # Run on local machine only
