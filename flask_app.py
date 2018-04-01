"""Application routes."""
import os
import pdfkit
from flask import (Flask, request, json, render_template, redirect, url_for,
                   flash, make_response)
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
    class CompanyInfo(object):
        """
        Temporary hardcoded params until flask login is implemented.

        Then user info will contain these attributes.
        """

        name = ""
        logo = url_for('static', filename="images/logo.png")
        job = ""
        TRN = ""
        TaxOffice = ""
        address = ""
        city = ""
        postal_code = ""
        country = ""
        phone = []
        fax = []
        email = ""
        website = ""
    company = CompanyInfo()

    return render_template('invoice.html', company=company)


@app.route("/invoice/create_pdf", methods=['POST'])
def invoice_pdf():
    """Create invoice."""
    class CompanyInfo(object):
        """
        Temporary hardcoded params until flask login is implemented.

        Then user info will contain these attributes.
        """

        name = ""
        logo = ("file://" + os.path.abspath('.') +
                url_for('static', filename="images/logo.png"))
        job = ""
        TRN = ""
        TaxOffice = ""
        address = ""
        city = ""
        postal_code = ""
        country = ""
        phone = []
        fax = []
        email = ""
        website = ""
    company = CompanyInfo()
    params = request.json
    pdfkit.from_string(input=render_template('print_invoice.html',
                                             company=company, **params),
                       output_path=('assets/invoices/' + params['InvoiceId'] +
                                    '.pdf'),
                       css=['static/css/invoice.css'])
    return redirect(url_for('view_pdf', invoice_id=params['InvoiceId']))


@app.route('/invoice/<invoice_id>' + '.pdf', methods=['GET'])
def view_pdf(invoice_id):
    """Show pdf with the given invoice_id."""
    with open('assets/invoices/' + invoice_id + '.pdf', 'rb') as pdf:
        response = make_response(pdf.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = ('inline;'
                                                   ' filename=%s.pdf' %
                                                   invoice_id)
    return response


# --------------------------------------------------------------------------- #


# Customer related routes

@app.route("/customer", methods=['GET', 'POST'])
def customer():
    """Create or update a customer."""
    form = CustomerForm()
    if form.validate_on_submit():
        cursor = mysql.cursor()
        cursor.callproc('sp_Customer', (form.Full_Name.data,
                                        form.Company.data,
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
    cursor.execute("select Full_Name, TRN from Customer")
    data = cursor.fetchall()
    return json.jsonify({'message': data})


@app.route('/select_customer', methods=['POST'])
def select_customer():
    """Select customers from customer_name."""
    cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
    TRN = request.form['TRN']
    cursor.execute('''SELECT *
                      FROM Customer
                      WHERE TRN=%s''', (TRN,))
    data = cursor.fetchone()
    if data:
        return json.jsonify(data)
    return json.jsonify({})

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
    ProductId = request.json['ProductId']
    cursor.execute("""SELECT *
                       FROM Product
                       WHERE Name=%s""", (ProductId,))
    data = cursor.fetchone()
    if data:
        data['UnitPrice'] = '{0:f}'.format(data['UnitPrice'])
        return json.jsonify(data)
    return json.jsonify({})


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
                      WHERE Name LIKE %s""", (Name,))
    data = cursor.fetchall()
    if len(data) is 0:
        cursor.execute("""INSERT INTO ProductUnitType (Name)
                          VALUES (%s)""", (Name,))
        mysql.commit()
    return redirect(url_for('unittype'))

# --------------------------------------------------------------------------- #


# Search related routes

@app.route("/search", methods=['GET'])
def search():
    """Create or update a product."""
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
