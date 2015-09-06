
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request

projects = [
    {'id': 1,
    'name': 'Project 1',
    'number': '12345'
    },
    {'id': 2,
    'name': 'Project 2',
    'number': '12346'
    }]
numerics = [
    {'id': 1
        'value': 1254,
        'name': 'h1',
        'link': 'D1@Sketch2@part1.sldprt',
        'unit': 'mm'
    },
    {'id': 2
        'value': 125456.3,
        'name': 'b1',
        'link': 'D2@Sketch2@part1.sldprt',
        'unit': 'mm'
    }]

app = Flask(__name__)

@app.route('/cad/api/v1.0/variables/')
def get_customers():
    return jsonify({'customers':customers})

@app.route('/shop/api/v1.0/customers/<int:customer_id>', methods = ['GET'])
def get_customer(customer_id):
    customer = [customer for customer in customers if customer['id'] == customer_id]
    return jsonify({'customer':customer[0]})

@app.route('/shop/api/v1.0/customers/', methods = ['POST'])
def create_customer():
    customer = {
        'id': customers[-1]['id']+1,
        'name': request.json['name'],
        'email': request.json['email']}
    customers.append(customer)
    return jsonify({'customer':customer}), 201

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

