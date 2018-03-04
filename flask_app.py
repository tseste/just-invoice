"""Application routes."""
from flask import (Flask, request, json, render_template, redirect, url_for,
                   flash)
from flask_mysqldb import MySQLdb

from _forms import CustomerForm, ProductForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKey!'

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


# Landing page

@app.route("/", methods=['GET'])
def index():
    """Landing page."""
    return render_template('index.html')

# --------------------------------------------------------------------------- #


# Invoice related routes

@app.route("/invoice", methods=['GET'])
def invoice():
    """Create invoice."""
    return render_template('invoice.html')

# --------------------------------------------------------------------------- #


# Customer related routes

@app.route("/customer", methods=['GET', 'POST'])
def customer():
    """Create or update a customer."""
    form = CustomerForm()
    if form.validate_on_submit():
        cursor = mysql.cursor()
        cursor.callproc('sp_Customer', (form.FirstName.data,
                                        form.LastName.data, form.Company.data,
                                        form.Address.data, form.City.data,
                                        form.Country.data,
                                        form.PostalCode.data,
                                        form.Phone.data, form.Fax.data,
                                        form.Email.data, form.TRN.data,
                                        form.TaxOffice.data))
        mysql.commit()
        flash(message='success')
        return redirect(url_for('customer'))
    return render_template('customer.html', form=form)


@app.route("/customer_list", methods=['POST'])
def customer_list():
    """Fetch all customers SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select FirstName, LastName, TRN from Customer")
    data = cursor.fetchall()
    return json.jsonify({'message': data})


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

@app.route("/product", methods=['GET', 'POST'])
def product():
    """Create or update a product."""
    form = ProductForm()
    cursor = mysql.cursor()
    cursor.execute("""SELECT UnitTypeId, Name
                      FROM ProductUnitType""")
    form.UnitTypeId.choices = list(cursor.fetchall())
    if form.UnitTypeId.data not in ['', None, 'None']:
        form.UnitTypeId.data = int(form.UnitTypeId.data)
    if form.validate_on_submit():
        cursor.callproc('sp_Product', (form.Name.data, form.Description.data,
                                       form.UnitTypeId.data,
                                       form.UnitPrice.data))
        mysql.commit()
        flash('Success!')
        return redirect(url_for('product'))
    return render_template('product.html', form=form)


@app.route("/product_list", methods=['POST'])
def product_list():
    """Fetch all products SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select Name from Product")
    data = cursor.fetchall()
    data = [item[0] for item in data]
    return json.jsonify({'message': data})


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


@app.route("/product_types_list", methods=['POST'])
def product_types_list():
    """Fetch all product types SQL query."""
    cursor = mysql.cursor()
    cursor.execute("select UnitTypeId, Name from ProductUnitType")
    data = cursor.fetchall()
    return json.jsonify({'message': data})


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

# --------------------------------------------------------------------------- #


if __name__ == '__main__':
    app.run(debug=True)
