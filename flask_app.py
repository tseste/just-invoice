"""Application routes."""
from flask import Flask, request, json, render_template, redirect, url_for
from flask_mysqldb import MySQLdb


app = Flask(__name__)

# MySQL configurations
credentials = {
    'host': '',
    'user': '',
    'passwd': '',
    'port': 3306,
    'db': '',
    'use_unicode': True,
    'charset': 'utf8'
}
mysql = MySQLdb.connect(**credentials)


# Navigation

@app.route("/", methods=['GET'])
def index():
    """Landing page."""
    return render_template('index.html')


@app.route("/invoice", methods=['GET'])
def invoice():
    """Create invoice."""
    return render_template('invoice.html')


@app.route("/customer", methods=['GET'])
def customer():
    """Create or update a customer."""
    return render_template('customer.html')


@app.route("/product", methods=['GET'])
def product():
    """Create or update a product."""
    return render_template('product.html')


@app.route("/search", methods=['GET'])
def search():
    """Create or update a product."""
    return render_template('search.html')


# --------------------------------------------------------------------------- #

# Customer related routes

@app.route("/customer_list", methods=['POST'])
def customer_list():
    """Fetch all customers SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select FirstName, LastName, TRN from Customer")
    data = cursor.fetchall()
    return json.jsonify({'message': data})


@app.route('/add_customer', methods=['POST'])
def add_customer():
    """Call procedure to create or update a customer's info."""
    cursor = mysql.cursor()
    FirstName = request.form['FirstName']
    LastName = request.form['LastName']
    Company = request.form['Company']
    Address = request.form['Address']
    City = request.form['City']
    Country = request.form['Country']
    PostalCode = request.form['PostalCode']
    Phone = request.form['Phone']
    Fax = request.form['Fax']
    Email = request.form['Email']
    TRN = request.form['TRN']
    TaxOffice = request.form['TaxOffice']

    cursor.callproc('sp_Customer', (FirstName, LastName, Company, Address,
                                    City, Country, PostalCode, Phone, Fax,
                                    Email, TRN, TaxOffice))
    return redirect(url_for('customer'))


@app.route('/select_customer', methods=['POST'])
def select_customer():
    """Select customers from customer_name."""
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    TRN = request.form['TRN']
    cursor.execute("""SELECT *
                      FROM Customer
                      WHERE TRN LIKE '{}'""".format(TRN))
    data = cursor.fetchone()
    return json.jsonify(data)


# --------------------------------------------------------------------------- #

# Product related routes

@app.route("/product_list", methods=['POST'])
def product_list():
    """Fetch all products SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select Name from Product")
    data = cursor.fetchall()
    data = [item[0] for item in data]
    return json.jsonify({'message': data})


@app.route("/product_types_list", methods=['POST'])
def product_types_list():
    """Fetch all product types SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select UnitTypeId, Name from ProductUnitType")
    data = cursor.fetchall()
    return json.jsonify({'message': data})


@app.route('/add_product', methods=['POST'])
def add_product():
    """Call procedure to create or update a product's info."""
    cursor = mysql.cursor()
    Name = request.form['Name']
    Description = request.form['Description']
    UnitTypeId = request.form['UnitTypeId']
    UnitPrice = request.form['UnitPrice']
    cursor.callproc('sp_Product', (Name, Description, UnitTypeId,
                                   UnitPrice))
    mysql.commit()
    return redirect(url_for('product'))


@app.route("/unittype", methods=['GET'])
def unittype():
    """Create a new product unit type."""
    return render_template('unittype.html')


@app.route('/new_unittype', methods=['POST'])
def new_unittype():
    """Add new unit type."""
    cursor = mysql.cursor()
    Name = request.form['Name']
    cursor.execute("""SELECT Name
                      FROM ProductUnitType
                      WHERE Name LIKE '{}'""".format(Name))
    data = cursor.fetchall()
    if len(data) is 0:
        cursor.execute("""INSERT INTO ProductUnitType (Name)
                          VALUES ('{}')""".format(Name))
        mysql.commit()
    return redirect(url_for('unittype'))


@app.route('/select_product', methods=['POST'])
def select_product():
    """Select products from product_name."""
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    Name = request.form['Name']
    try:
        cursor.execute(r"""SELECT *
                           FROM Product
                           WHERE Name LIKE '{}'""".format(Name))
        data = cursor.fetchone()
        data['UnitPrice'] = '{0:f}'.format(data['UnitPrice'])
        return json.jsonify(data)
    except Exception as e:
        print(e)
        return json.jsonify({'Name': Name})


# --------------------------------------------------------------------------- #

# Final Invoice

@app.route("/print_invoice", methods=['GET', 'POST'])
def print_invoice():
    """Print invoice."""
    data = request.form
    print(data)
    return render_template('print_invoice.html')


if __name__ == '__main__':
    app.run(debug=True)
