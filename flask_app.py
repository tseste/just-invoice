"""Application routes."""
from flask import Flask, request, json, render_template, Response
from flask_mysqldb import MySQLdb


app = Flask(__name__)

# MySQL configurations
credentials = {
    'host': '',
    'user': '',
    'passwd': '',
    'port': ,
    'db': '',
    'use_unicode': True,
    'charset': 'utf8'
}
mysql = MySQLdb.connect(**credentials)


@app.route("/", methods=['GET'])
def index():
    """Landing page."""
    return render_template('index.html')


@app.route("/invoice", methods=['GET'])
def invoice():
    """Invoice fill."""
    return render_template('invoice.html')


@app.route("/print_invoice", methods=['GET', 'POST'])
def print_invoice():
    """Invoice print."""
    data = request.form
    print(data)
    return render_template('print_invoice.html')


@app.route("/customers", methods=['GET'])
def customers():
    """Customers list."""
    return render_template('customers.html')


@app.route("/customer_list", methods=['POST'])
def customer_list():
    """Fetch all customers SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select customer_name from Customer")
    data = cursor.fetchall()
    data = [item[0] for item in data]
    return json.jsonify({'message': data})


@app.route("/customers_info", methods=['GET'])
def customers_info():
    return render_template('customers_info_table.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    cursor = mysql.cursor()
    customer_name = request.form['customer_name']
    customer_mail = request.form['customer_mail']
    customer_address = request.form['customer_address']
    customer_job = request.form['customer_job']
    customer_afm = request.form['customer_afm']
    customer_doy = request.form['customer_doy']
    cursor.callproc('sp_createUser', (customer_name, customer_mail,
                                      customer_address, customer_job,
                                      customer_afm, customer_doy))
    data = cursor.fetchall()

    if len(data) is 0:
        mysql.commit()
        return 'Επιτυχής Εισαγωγή'
    else:
        return ('Το ιδιο Ονοματεπώνυμο και ο αριθμος Α.Φ.Μ. '
                'δεν μπορουν να υπαρχουν σε δευτερο πελάτη')


@app.route('/select_user', methods=['POST'])
def select_user():
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    customer_name = request.form['customer_name']
    cursor.execute("select * from Customer where customer_name LIKE '{}'".format(customer_name))
    data = cursor.fetchone()
    return json.jsonify(data)


@app.route('/fetch_users', methods=['POST'])
def fetch_users():
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Customer")
    data = cursor.fetchall()
    return Response(response=json.dumps(data),
                    status=200,
                    mimetype='application/json')


@app.route('/add_product', methods=['POST'])
def add_product():
    cursor = mysql.cursor()
    product_name = request.form['product_name']
    product_mu = request.form['product_mu']
    product_up = request.form['product_up']
    cursor.callproc('sp_createProduct', (product_name,
                                         product_mu, product_up))
    data = cursor.fetchall()

    if len(data) is 0:
        mysql.commit()
        return 'Επιτυχής Εισαγωγή'
    else:
        return 'Αποτυχία Εισαγωγής Προϊόντος'


@app.route('/select_product', methods=['POST'])
def select_product():
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    product_name = next(request.form.values())
    cursor.execute("select * from Product where product_name LIKE '{}'".format(product_name))
    data = cursor.fetchone()
    print(data)
    return json.jsonify(data)


@app.route('/fetch_products', methods=['POST'])
def fetch_products():
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from Product")
    data = cursor.fetchall()
    return Response(response=json.dumps(data),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
