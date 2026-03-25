import pymysql
from flask import Blueprint, flash, json, redirect, render_template, request, url_for

from app.db import get_db_connection
from app.forms import CustomerForm

bp = Blueprint("customer", __name__)


@bp.route("/customer", methods=["GET", "POST"])
def customer():
    """Create or update a customer."""
    form = CustomerForm()
    if form.validate_on_submit():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.callproc(
            "sp_Customer",
            (
                form.FirstName.data,
                form.LastName.data,
                form.Company.data,
                form.Address.data,
                form.City.data,
                form.Country.data,
                form.PostalCode.data,
                form.Phone.data,
                form.Fax.data,
                form.Email.data,
                form.TRN.data,
                form.TaxOffice.data,
            ),
        )
        connection.commit()
        flash(message="success")
        return redirect(url_for("customer.customer"))
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}")
    return render_template("customer.html", form=form)


@bp.route("/customer_list", methods=["POST"])
def customer_list():
    """Fetch all customers SQL query."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """SELECT CONCAT(FirstName, ' ', LastName) AS Full_Name,
                         TRN
                  FROM Customer"""
    )
    data = cursor.fetchall()
    return json.jsonify({"message": data})


@bp.route("/select_customer", methods=["POST"])
def select_customer():
    """Select customer by TRN."""
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    trn = request.form["TRN"]
    cursor.execute(
        """SELECT *
           FROM Customer
           WHERE TRN=%s""",
        (trn,),
    )
    data = cursor.fetchone()
    if data:
        return json.jsonify(data)
    return json.jsonify({})
