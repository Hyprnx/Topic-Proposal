from flasgger import Swagger
from flask import Flask, request, make_response, jsonify, render_template, redirect, session
from forms import *
import pandas
import re
import json

from database_manager.database_manager import *
from database_manager.customers_db_manager import CustomerDatabaseManager
from database_manager.employee_manager import EmployeeDatabaseManager
from database_manager.product_manager import ProductDatabaseManager

from credentials.secret_keys import key

transaction_database_manager = TransactionBlockChainManager()
demo_database_manager = DemoBlockChainManager()
customer_database_manager = CustomerDatabaseManager()
employee_database_manager = EmployeeDatabaseManager()
product_database_manager = ProductDatabaseManager()

app = Flask(__name__, template_folder='templates')
app.secret_key = key

app.config['SWAGGER'] = {
    'doc_dir': 'common/data_structure/apidocs'
}
swagger = Swagger(app)

@app.before_first_request
def initialize():
    session['loggedin'] = False
    session['username'] = 'Not logged in'


@app.errorhandler(404)
def not_found():
    return render_template("errors/404.html",
                           mess='Oops, we think you made mistake somewhere, please check the web path .·´¯`(>▂<)´¯`·. ')

@app.errorhandler(500)
def not_found():
    return render_template("errors/500.html",
                           mess='Oops, we think we have made mistake somewhere, please submit issue to our github at https://github.com/Hyprnx/Topic-Proposal. Thank you!')



@app.route('/status')
def system_status():
    return {'status': 'OK',
            'session': session}


@app.route('/')
def landing_page():
    return redirect('/about', code=302)


@app.route('/home')
def home():
    return render_template('pages/home.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'address' in request.form:
        username = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        address_confirmation = request.form['confirm']
        app.logger.info(f'{username}, {phone}, {address}')

        if address_confirmation != address:
            return render_template('failed/failed_registering.html',
                                   mess='Your credential does not match, please try again!')

        if not re.match(r'', phone):
            return render_template('failed/failed_registering.html', mess='Invalid phone number, please try again!')

        if customer_database_manager.check_customer_exist(phone):
            return render_template('failed/failed_registering.html', mess='Customer exited, please try again!')

        res = customer_database_manager.register_customers(name=username, phone=phone, address=address)
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
            return render_template('failed/failed_login.html', mess='Wrong Credential')
    return render_template('forms/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect('/home', code=302)


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    form = TransactionForm(request.form)
    if request.method == 'POST':
        if session['loggedin'] and 'customer_phone' in request.form and 'employee_phone' in request.form and 'product_id' in request.form and 'amount' in request.form:

            app.logger.info('Getting employee info')
            employee_info = employee_database_manager.get_employee_info(request.form['employee_phone'])
            app.logger.info(employee_info)

            app.logger.info('Getting customer info')
            customer_info = customer_database_manager.get_customer_info(request.form['customer_phone'])
            app.logger.info(customer_info)

            app.logger.info('Getting product info')
            product_info = product_database_manager.get_product_info(request.form['product_id'])
            app.logger.info(product_info)
            amount = request.form['amount']

            # conditions checking
            if not employee_info:
                return render_template('failed/failed_transaction.html', mess='Not employee')

            if not customer_info:
                return render_template('failed/failed_transaction.html', mess='Not customer yet')

            if not product_info:
                return render_template('failed/failed_transaction.html', mess='No product found')

            if not int(amount) < product_info['stock']:
                return render_template('failed/failed_transaction.html', mess='Not enough stock for this good')

            # block data creating
            transaction_info = {
                'employee_info': employee_info,
                'customer_info': customer_info,
                'product_info': product_info,
                'amount': int(amount),
                'total_bill': int(amount) * product_info['price']
            }
            signer = employee_info['Name']

            try:
                respond = transaction_database_manager.insert_block(data=transaction_info, signer=signer)
                if respond:
                    update = product_database_manager.sell_product(product_id=product_info['product_id'], current_amount=product_info['stock'], amount_sell=amount)
                    if update:
                        return render_template('success/success_transaction.html', mess='Success validate blockchain and added block to blockchain')
                    return render_template('failed/failed_transaction.html', mess='Database refused to insert block')
                else:
                    return render_template('failed/failed_transaction.html', mess='Database refused to insert block')
            except pymongo.errors.OperationFailure as e:
                return render_template('failed/failed_transaction.html', mess=f'Database refused to insert block, error: {e}')

    return render_template('forms/transaction.html', form=form)


@app.route('/import_product', methods=['POST', 'GET'])
def import_product():
    form = AddProductForm(request.form)
    if request.method == 'POST':
        if session['loggedin'] and 'product_name' in request.form and 'product_id' in request.form and 'product_amount'\
                in request.form and 'product_price' in request.form and 'employee_phone' in request.form:

            product_id = int(request.form['product_id'])
            product_name = request.form['product_name']
            add_amount = int(request.form['product_amount'])
            price = float(request.form['product_price'])

            app.logger.info('Getting employee info')
            employee_info = employee_database_manager.get_employee_info(request.form['employee_phone'])
            app.logger.info(employee_info)


            app.logger.info('Getting product info')
            product_info = product_database_manager.get_product_info(request.form['product_id'])
            app.logger.info(f'Product info from database: {product_info}')

            # conditions checking
            if not employee_info:
                return render_template('failed/failed_import_product.html', mess='No employee logged in')

            if not product_info:
                respond = product_database_manager.import_product(new_product=True, product_id=product_id, product_name=product_name, price=price, new_stock=add_amount)
                if respond:
                    return render_template('success/success_importing.html', mess='Successfully added new product')
                else:
                    return render_template('failed/failed_import_product.html', mess='Error while updating product stock')
            # update
            else:
                respond = product_database_manager.import_product(new_product=False, product_id=product_id, old_amount=product_info['stock'], new_amount=add_amount)
                if respond:
                    return render_template('success/success_importing.html', mess='Successfully added new product, the mistyped name, price will not be modified in database')
                else:
                    return render_template('failed/failed_import_product.html', mess='Error while updating product stock')

    return render_template('forms/import_product.html', form=form)

@app.route('/demo', methods=['POST'])
def demo():
    signer = request.args.get('signer', 'To Duc Anh')
    data = request.args.get('data', 'This is a blank block')
    try:
        respond = demo_database_manager.insert_block(data, signer)
        return make_response(jsonify(respond), 200)
    except pymongo.errors.OperationFailure as e:
        return make_response(jsonify(e), 500)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryForm(request.form)
    if request.method == 'POST':
        query = json.loads(request.form['query'])
        app.logger.info(query)
        if request.form['field'] == 'customer' or 'Customer':
            respond = customer_database_manager.query(query)
        elif request.form['field'] == 'product' or 'Product':
            respond = product_database_manager.query(query)
        elif request.form['field'] == 'employee' or 'Employee':
            respond = employee_database_manager.query(query)

        app.logger.info(type(respond))
        app.logger.info(respond)
        if respond:
            return_value = {}
            for i, data in enumerate(respond):
                app.logger.info(data)
                return_value[i] = data

            return return_value
        else:
            return {"Mess": "No respond"}

    return render_template('forms/query.html', form=form)


@app.route('/validation')
def validation():
    res = transaction_database_manager.validate()
    if res:
        mess = 'Successfully validated transaction Blockchain'
    else:
        mess = 'Failed to validate blockchain, proceed with caution'
    return render_template('success/success_validate.html', mess=mess)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9200, debug=True)  # Everyone within the same network can use
    # app.run(port=13030) # Run on local machine only
